import builtins
import logging
import os
import time
from pathlib import Path
from threading import Lock
from typing import IO, Any, Callable, Optional, cast
from unittest.mock import patch

from modelaudit.scanners import (
    SCANNER_REGISTRY,
    GgufScanner,
    KerasH5Scanner,
    NumPyScanner,
    OnnxScanner,
    PickleScanner,
    PyTorchBinaryScanner,
    PyTorchZipScanner,
    SafeTensorsScanner,
    TensorFlowSavedModelScanner,
    ZipScanner,
)
from modelaudit.scanners.base import IssueSeverity, ScanResult
from modelaudit.utils import is_within_directory
from modelaudit.utils.filetype import detect_file_format, detect_format_from_extension

logger = logging.getLogger("modelaudit.core")

# Lock to ensure thread-safe monkey patching of builtins.open
_OPEN_PATCH_LOCK = Lock()


def validate_scan_config(config: dict[str, Any]) -> None:
    """Validate configuration parameters for scanning."""
    timeout = config.get("timeout")
    if timeout is not None:
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("timeout must be a positive integer")

    max_file_size = config.get("max_file_size")
    if max_file_size is not None:
        if not isinstance(max_file_size, int) or max_file_size < 0:
            raise ValueError("max_file_size must be a non-negative integer")

    chunk_size = config.get("chunk_size")
    if chunk_size is not None:
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer")


def scan_model_directory_or_file(
    path: str,
    blacklist_patterns: Optional[list[str]] = None,
    timeout: int = 300,
    max_file_size: int = 0,
    max_total_size: int = 0,
    progress_callback: Optional[Callable[[str, float], None]] = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Scan a model file or directory for malicious content.

    Args:
        path: Path to the model file or directory
        blacklist_patterns: Additional blacklist patterns to check against model names
        timeout: Scan timeout in seconds
        max_file_size: Maximum file size to scan in bytes
        max_total_size: Maximum total bytes to scan across all files
        progress_callback: Optional callback function to report progress
                          (message, percentage)
        **kwargs: Additional arguments to pass to scanners

    Returns:
        Dictionary with scan results
    """
    # Start timer for timeout
    start_time = time.time()

    # Initialize results with proper type hints
    results: dict[str, Any] = {
        "start_time": start_time,
        "path": path,
        "bytes_scanned": 0,
        "issues": [],
        "success": True,
        "files_scanned": 0,
        "scanners": [],  # Track the scanners used
    }

    # Configure scan options
    config = {
        "blacklist_patterns": blacklist_patterns,
        "max_file_size": max_file_size,
        "max_total_size": max_total_size,
        "timeout": timeout,
        **kwargs,
    }

    validate_scan_config(config)

    try:
        # Check if path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")

        # Check if path is readable
        if not os.access(path, os.R_OK):
            raise PermissionError(f"Path is not readable: {path}")

        # Check if path is a directory
        if os.path.isdir(path):
            if progress_callback:
                progress_callback(f"Scanning directory: {path}", 0.0)

            # Scan all files in the directory
            total_files = sum(1 for _ in Path(path).rglob("*") if _.is_file())
            processed_files = 0
            limit_reached = False

            base_dir = Path(path).resolve()
            for root, _, files in os.walk(path, followlinks=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    resolved_file = Path(file_path).resolve()
                    if not is_within_directory(str(base_dir), str(resolved_file)):
                        issues_list = cast(list[dict[str, Any]], results["issues"])
                        issues_list.append(
                            {
                                "message": "Path traversal outside scanned directory",
                                "severity": IssueSeverity.CRITICAL.value,
                                "location": file_path,
                                "details": {"resolved_path": str(resolved_file)},
                            }
                        )
                        continue

                    # Check timeout
                    if time.time() - start_time > timeout:
                        raise TimeoutError(f"Scan timeout after {timeout} seconds")

                    # Update progress
                    if progress_callback and total_files > 0:
                        processed_files += 1
                        progress_callback(
                            f"Scanning file {processed_files}/{total_files}: {file}",
                            processed_files / total_files * 100,
                        )

                    # Scan the file
                    try:
                        file_result = scan_file(file_path, config)
                        # Use cast to help mypy understand the types
                        results["bytes_scanned"] = (
                            cast(int, results["bytes_scanned"])
                            + file_result.bytes_scanned
                        )
                        results["files_scanned"] = (
                            cast(int, results["files_scanned"]) + 1
                        )  # Increment file count

                        # Track scanner name
                        scanner_name = file_result.scanner_name
                        scanners_list = cast(list[str], results["scanners"])
                        if scanner_name and scanner_name not in scanners_list:
                            scanners_list.append(scanner_name)

                        # Add issues from file scan
                        issues_list = cast(list[dict[str, Any]], results["issues"])
                        for issue in file_result.issues:
                            issues_list.append(issue.to_dict())

                        if (
                            max_total_size > 0
                            and cast(int, results["bytes_scanned"]) > max_total_size
                        ):
                            issues_list.append(
                                {
                                    "message": f"Total scan size limit exceeded: {results['bytes_scanned']} bytes (max: {max_total_size})",
                                    "severity": IssueSeverity.WARNING.value,
                                    "location": file_path,
                                    "details": {"max_total_size": max_total_size},
                                }
                            )
                            limit_reached = True
                            break
                    except Exception as e:
                        logger.warning(f"Error scanning file {file_path}: {str(e)}")
                        # Add as an issue
                        issues_list = cast(list[dict[str, Any]], results["issues"])
                        issues_list.append(
                            {
                                "message": f"Error scanning file: {str(e)}",
                                "severity": IssueSeverity.WARNING.value,
                                "location": file_path,
                                "details": {"exception_type": type(e).__name__},
                            },
                        )
                if limit_reached:
                    break
            # Stop scanning if size limit reached
            if limit_reached:
                pass
        else:
            # Scan a single file
            if progress_callback:
                progress_callback(f"Scanning file: {path}", 0.0)

            # Get file size for progress reporting
            file_size = os.path.getsize(path)
            results["files_scanned"] = 1  # Single file scan

            # Create a wrapper for the file to report progress
            if progress_callback is not None and file_size > 0:
                original_builtins_open = builtins.open

                def progress_open(
                    file_path: str,
                    mode: str = "r",
                    *args: Any,
                    **kwargs: Any,
                ) -> IO[Any]:
                    file = original_builtins_open(file_path, mode, *args, **kwargs)
                    file_pos = 0

                    # Override read method to report progress
                    original_read = file.read

                    def progress_read(size: int = -1) -> Any:
                        nonlocal file_pos
                        data = original_read(size)
                        if isinstance(data, (str, bytes)):
                            file_pos += len(data)
                        if progress_callback is not None:
                            progress_callback(
                                f"Reading file: {os.path.basename(file_path)}",
                                min(file_pos / file_size * 100, 100),
                            )
                        return data

                    file.read = progress_read  # type: ignore[method-assign]
                    return file

                with _OPEN_PATCH_LOCK, patch("builtins.open", progress_open):
                    file_result = scan_file(path, config)
            else:
                file_result = scan_file(path, config)

            results["bytes_scanned"] = (
                cast(int, results["bytes_scanned"]) + file_result.bytes_scanned
            )

            # Track scanner name
            scanner_name = file_result.scanner_name
            scanners_list = cast(list[str], results["scanners"])
            if scanner_name and scanner_name not in scanners_list:
                scanners_list.append(scanner_name)

            # Add issues from file scan
            issues_list = cast(list[dict[str, Any]], results["issues"])
            for issue in file_result.issues:
                issues_list.append(issue.to_dict())

            if (
                max_total_size > 0
                and cast(int, results["bytes_scanned"]) > max_total_size
            ):
                issues_list.append(
                    {
                        "message": f"Total scan size limit exceeded: {results['bytes_scanned']} bytes (max: {max_total_size})",
                        "severity": IssueSeverity.WARNING.value,
                        "location": path,
                        "details": {"max_total_size": max_total_size},
                    }
                )

            if progress_callback:
                progress_callback(f"Completed scanning: {path}", 100.0)

    except Exception as e:
        logger.exception(f"Error during scan: {str(e)}")
        results["success"] = False
        issue_dict = {
            "message": f"Error during scan: {str(e)}",
            "severity": IssueSeverity.CRITICAL.value,
            "details": {"exception_type": type(e).__name__},
        }
        issues_list = cast(list[dict[str, Any]], results["issues"])
        issues_list.append(issue_dict)

    # Add final timing information
    results["finish_time"] = time.time()
    results["duration"] = cast(float, results["finish_time"]) - cast(
        float,
        results["start_time"],
    )

    # Determine if there were operational scan errors vs security findings
    # has_errors should only be True for operational errors (scanner crashes,
    # file not found, etc.) not for security findings detected in models
    operational_error_indicators = [
        # Scanner execution errors
        "Error during scan",
        "Error checking file size",
        "Error scanning file",
        "Scanner crashed",
        "Scan timeout",
        # File system errors
        "Path does not exist",
        "Path is not readable",
        "Permission denied",
        "File not found",
        # Dependency/environment errors
        "not installed, cannot scan",
        "Missing dependency",
        "Import error",
        "Module not found",
        # File format/corruption errors
        "not a valid",
        "Invalid file format",
        "Corrupted file",
        "Bad file signature",
        "Unable to parse",
        # Resource/system errors
        "Out of memory",
        "Disk space",
        "Too many open files",
    ]

    issues_list = cast(list[dict[str, Any]], results["issues"])
    results["has_errors"] = (
        any(
            any(
                indicator in issue.get("message", "")
                for indicator in operational_error_indicators
            )
            for issue in issues_list
            if isinstance(issue, dict)
            and issue.get("severity") == IssueSeverity.CRITICAL.value
        )
        or not results["success"]
    )

    return results


def determine_exit_code(results: dict[str, Any]) -> int:
    """
    Determine the appropriate exit code based on scan results.

    Exit codes:
    - 0: Success, no security issues found
    - 1: Security issues found (scan completed successfully)
    - 2: Operational errors occurred during scanning

    Args:
        results: Dictionary with scan results

    Returns:
        Exit code (0, 1, or 2)
    """
    # Check for operational errors first (highest priority)
    if results.get("has_errors", False):
        return 2

    # Check for any security findings (warnings, errors, or info issues)
    issues = results.get("issues", [])
    if issues:
        # Filter out DEBUG level issues for exit code determination
        non_debug_issues = [
            issue
            for issue in issues
            if isinstance(issue, dict) and issue.get("severity") != "debug"
        ]
        if non_debug_issues:
            return 1

    # No issues found
    return 0


def scan_file(path: str, config: dict[str, Any] = None) -> ScanResult:
    """
    Scan a single file with the appropriate scanner.

    Args:
        path: Path to the file to scan
        config: Optional scanner configuration

    Returns:
        ScanResult object with the scan results
    """
    if config is None:
        config = {}
    validate_scan_config(config)

    # Check file size first
    max_file_size = config.get("max_file_size", 0)  # Default unlimited
    try:
        file_size = os.path.getsize(path)
        if max_file_size > 0 and file_size > max_file_size:
            sr = ScanResult(scanner_name="size_check")
            sr.add_issue(
                f"File too large to scan: {file_size} bytes (max: {max_file_size})",
                severity=IssueSeverity.WARNING,
                details={
                    "file_size": file_size,
                    "max_file_size": max_file_size,
                    "path": path,
                },
            )
            return sr
    except OSError as e:
        sr = ScanResult(scanner_name="error")
        sr.add_issue(
            f"Error checking file size: {e}",
            severity=IssueSeverity.CRITICAL,
            details={"error": str(e), "path": path},
        )
        return sr

    logger.info(f"Scanning file: {path}")

    header_format = detect_file_format(path)
    ext_format = detect_format_from_extension(path)
    ext = os.path.splitext(path)[1].lower()

    discrepancy_msg = None
    if (
        header_format != ext_format
        and header_format != "unknown"
        and ext_format != "unknown"
    ):
        # Don't warn about common PyTorch .bin files that are ZIP format internally
        # This is expected behavior for torch.save()
        if not (
            ext_format == "pytorch_binary" and header_format == "zip" and ext == ".bin"
        ):
            discrepancy_msg = f"File extension indicates {ext_format} but header indicates {header_format}."
            logger.warning(discrepancy_msg)

    # Prefer scanner based on header format
    preferred_scanner: Optional[type] = None

    # Special handling for PyTorch files that are ZIP-based
    if header_format == "zip" and ext in [".pt", ".pth"]:
        preferred_scanner = PyTorchZipScanner
    elif header_format == "zip" and ext == ".bin":
        # PyTorch .bin files saved with torch.save() are ZIP format internally
        # Use PickleScanner which can handle both pickle and ZIP-based PyTorch files
        preferred_scanner = PickleScanner
    else:
        preferred_scanner = {
            "pickle": PickleScanner,
            "pytorch_binary": PyTorchBinaryScanner,
            "hdf5": KerasH5Scanner,
            "safetensors": SafeTensorsScanner,
            "tensorflow_directory": TensorFlowSavedModelScanner,
            "protobuf": TensorFlowSavedModelScanner,
            "zip": ZipScanner,
            "onnx": OnnxScanner,
            "gguf": GgufScanner,
            "ggml": GgufScanner,
            "numpy": NumPyScanner,
        }.get(header_format)

    result: Optional[ScanResult]
    if preferred_scanner and preferred_scanner.can_handle(path):
        logger.debug(
            f"Using {preferred_scanner.name} scanner for {path} based on header"
        )
        scanner = preferred_scanner(config=config)  # type: ignore[abstract]
        result = scanner.scan(path)
    else:
        result = None
        for scanner_class in SCANNER_REGISTRY:
            if scanner_class.can_handle(path):
                logger.debug(f"Using {scanner_class.name} scanner for {path}")
                scanner = scanner_class(config=config)  # type: ignore[abstract]
                result = scanner.scan(path)
                break

        if result is None:
            format_ = header_format
            sr = ScanResult(scanner_name="unknown")
            sr.add_issue(
                f"Unknown or unhandled format: {format_}",
                severity=IssueSeverity.DEBUG,
                details={"format": format_, "path": path},
            )
            result = sr

    if discrepancy_msg:
        result.add_issue(
            discrepancy_msg + " Using header-based detection.",
            severity=IssueSeverity.WARNING,
            location=path,
            details={
                "extension_format": ext_format,
                "header_format": header_format,
            },
        )

    return result


def merge_scan_result(
    results: dict[str, Any],
    scan_result: ScanResult,
) -> dict[str, Any]:
    """
    Merge a ScanResult object into the results dictionary.

    Args:
        results: The existing results dictionary
        scan_result: The ScanResult object to merge

    Returns:
        The updated results dictionary
    """
    # Convert scan_result to dict if it's a ScanResult object
    if isinstance(scan_result, ScanResult):
        scan_dict = scan_result.to_dict()
    else:
        scan_dict = scan_result

    # Merge issues
    issues_list = cast(list[dict[str, Any]], results["issues"])
    for issue in scan_dict.get("issues", []):
        issues_list.append(issue)

    # Update bytes scanned
    results["bytes_scanned"] = cast(int, results["bytes_scanned"]) + scan_dict.get(
        "bytes_scanned",
        0,
    )

    # Update scanner info if not already set
    if "scanner_name" not in results and "scanner" in scan_dict:
        results["scanner_name"] = scan_dict["scanner"]

    # Set success to False if any scan failed
    if not scan_dict.get("success", True):
        results["success"] = False

    return results
