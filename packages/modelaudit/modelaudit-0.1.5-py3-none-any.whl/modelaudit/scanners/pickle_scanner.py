import logging
import os
import pickletools
import struct
import time
from typing import Any, BinaryIO, Dict, List, Optional, Union

from modelaudit.suspicious_symbols import (
    SUSPICIOUS_GLOBALS,
    SUSPICIOUS_STRING_PATTERNS,
)

from ..explanations import (
    get_import_explanation,
    get_opcode_explanation,
    get_pattern_explanation,
)
from ..suspicious_symbols import DANGEROUS_OPCODES
from .base import BaseScanner, IssueSeverity, ScanResult

logger = logging.getLogger(__name__)
# ============================================================================
# SMART DETECTION SYSTEM - ML Context Awareness
# ============================================================================

# ML Framework Detection Patterns
ML_FRAMEWORK_PATTERNS: Dict[str, Dict[str, Union[List[str], float]]] = {
    "pytorch": {
        "modules": [
            "torch",
            "torchvision",
            "torch.nn",
            "torch.optim",
            "torch.utils",
            "_pickle",
        ],
        "classes": [
            "OrderedDict",
            "Parameter",
            "Module",
            "Linear",
            "Conv2d",
            "BatchNorm2d",
            "ReLU",
            "MaxPool2d",
            "AdaptiveAvgPool2d",
            "Sequential",
            "ModuleList",
        ],
        "patterns": [r"torch\..*", r"_pickle\..*", r"collections\.OrderedDict"],
        "confidence_boost": 0.8,
    },
    "yolo": {
        "modules": ["ultralytics", "yolo", "models"],
        "classes": ["YOLO", "YOLOv8", "Detect", "C2f", "Conv", "Bottleneck", "SPPF"],
        "patterns": [
            r"yolo.*",
            r"ultralytics\..*",
            r".*\.detect",
            r".*\.backbone",
            r".*\.head",
        ],
        "confidence_boost": 0.9,
    },
    "tensorflow": {
        "modules": ["tensorflow", "keras", "tf"],
        "classes": ["Model", "Layer", "Dense", "Conv2D", "Flatten"],
        "patterns": [r"tensorflow\..*", r"keras\..*"],
        "confidence_boost": 0.8,
    },
    "sklearn": {
        "modules": ["sklearn", "joblib"],
        "classes": ["Pipeline", "StandardScaler", "PCA"],
        "patterns": [r"sklearn\..*", r"joblib\..*"],
        "confidence_boost": 0.7,
    },
    "huggingface": {
        "modules": ["transformers", "tokenizers"],
        "classes": ["AutoModel", "AutoTokenizer", "BertModel", "GPT2Model"],
        "patterns": [r"transformers\..*", r"tokenizers\..*"],
        "confidence_boost": 0.8,
    },
}

# Safe ML-specific global patterns
ML_SAFE_GLOBALS: Dict[str, List[str]] = {
    # PyTorch safe patterns
    "torch": ["*"],  # All torch functions are generally safe
    "torch.nn": ["*"],
    "torch.optim": ["*"],
    "torch.utils": ["*"],
    "_pickle": ["*"],  # PyTorch uses _pickle internally
    "collections": ["OrderedDict", "defaultdict", "namedtuple"],
    "typing": ["*"],
    "numpy": ["*"],  # NumPy operations are safe
    "math": ["*"],  # Math operations are safe
    # YOLO/Ultralytics safe patterns
    "ultralytics": ["*"],
    "yolo": ["*"],
    # Standard ML libraries
    "sklearn": ["*"],
    "transformers": ["*"],
    "tokenizers": ["*"],
    "joblib": [
        "dump",
        "load",
        "Parallel",
        "delayed",
        "Memory",
        "hash",
        "_pickle_dump",
        "_pickle_load",
    ],
    "dill": ["dump", "dumps", "load", "loads", "copy"],
    "tensorflow": ["*"],
    "keras": ["*"],
}

# Dangerous actual code execution patterns in strings
ACTUAL_DANGEROUS_STRING_PATTERNS = [
    r"os\.system\s*\(",
    r"subprocess\.",
    r"exec\s*\(",
    r"eval\s*\(",
    r"__import__\s*\(",
    r"compile\s*\(",
    r"open\s*\(['\"].*['\"],\s*['\"]w",  # File write operations
    r"\.popen\s*\(",
    r"\.spawn\s*\(",
]


def _detect_ml_context(opcodes: list[tuple]) -> dict[str, Any]:
    """
    Detect ML framework context from opcodes with confidence scoring.
    Uses improved scoring that focuses on presence and diversity of ML patterns
    rather than their proportion of total opcodes.
    """
    context: dict[str, Any] = {
        "frameworks": {},
        "overall_confidence": 0.0,
        "is_ml_content": False,
        "detected_patterns": [],
    }

    total_opcodes = len(opcodes)
    if total_opcodes == 0:
        return context

    # Analyze GLOBAL opcodes for ML patterns
    global_refs: dict[str, int] = {}
    total_global_opcodes = 0

    for opcode, arg, pos in opcodes:
        if opcode.name == "GLOBAL" and isinstance(arg, str):
            total_global_opcodes += 1
            # Extract module name from global reference
            if "." in arg:
                module = arg.split(".")[0]
            elif " " in arg:
                module = arg.split(" ")[0]
            else:
                module = arg

            global_refs[module] = global_refs.get(module, 0) + 1

    # Check each framework with improved scoring
    for framework, patterns in ML_FRAMEWORK_PATTERNS.items():
        framework_score = 0.0
        matches: list[str] = []

        # Check module matches with improved scoring
        modules = patterns["modules"]
        if isinstance(modules, list):
            for module in modules:
                if module in global_refs:
                    # Score based on presence and frequency,
                    # not proportion of total opcodes
                    ref_count = global_refs[module]

                    # Base score for presence
                    module_score = 10.0  # Base score for any ML module presence

                    # Bonus for frequency (up to 20 more points)
                    if ref_count >= 5:
                        module_score += 20.0
                    elif ref_count >= 2:
                        module_score += 10.0
                    elif ref_count >= 1:
                        module_score += 5.0

                    framework_score += module_score
                    matches.append(f"module:{module}({ref_count})")

        # Store framework detection with much lower threshold
        if framework_score > 5.0:  # Much lower threshold - any ML module presence
            # Normalize confidence to 0-1 range
            confidence_boost = patterns["confidence_boost"]
            if isinstance(confidence_boost, (int, float)):
                confidence = min(framework_score / 100.0 * confidence_boost, 1.0)
                context["frameworks"][framework] = {
                    "confidence": confidence,
                    "matches": matches,
                    "raw_score": framework_score,
                }
                context["detected_patterns"].extend(matches)

    # Calculate overall ML confidence - highest framework confidence
    if context["frameworks"]:
        context["overall_confidence"] = max(
            fw["confidence"] for fw in context["frameworks"].values()
        )
        # Much more lenient threshold - any significant ML pattern detection
        context["is_ml_content"] = context["overall_confidence"] > 0.15  # Was 0.3

    return context


def _is_actually_dangerous_global(mod: str, func: str, ml_context: dict) -> bool:
    """
    Smart global reference analysis - distinguishes between legitimate ML operations
    and actual dangerous operations.
    """
    # If we have high ML confidence, be more lenient with "suspicious" globals
    if (
        ml_context.get("is_ml_content")
        and ml_context.get("overall_confidence", 0) > 0.5
    ):
        # Check if this is a known safe ML global
        if mod in ML_SAFE_GLOBALS:
            safe_funcs = ML_SAFE_GLOBALS[mod]
            if safe_funcs == ["*"] or func in safe_funcs:
                return False

    # Use original suspicious global check for genuinely suspicious patterns
    return is_suspicious_global(mod, func)


def _is_actually_dangerous_string(s: str, ml_context: dict) -> Optional[str]:
    """
    Smart string analysis - looks for actual executable code rather than ML patterns.
    """
    import re

    if not isinstance(s, str):
        return None

    # Check for ACTUAL dangerous patterns (not just ML magic methods)
    for pattern in ACTUAL_DANGEROUS_STRING_PATTERNS:
        if re.search(pattern, s, re.IGNORECASE):
            return pattern

    # If we have strong ML context, ignore common ML patterns
    if (
        ml_context.get("is_ml_content")
        and ml_context.get("overall_confidence", 0) > 0.6
    ):
        # Skip common ML magic method patterns
        if re.match(r"^__\w+__$", s):  # Simple magic methods like __call__, __init__
            return None

        # Skip tensor/layer names
        if any(
            term in s.lower()
            for term in ["layer", "conv", "batch", "norm", "relu", "pool", "linear"]
        ):
            return None

    # Check for base64-like strings (still suspicious)
    if len(s) > 100 and re.match(r"^[A-Za-z0-9+/=]+$", s):
        return "potential_base64"

    return None


def _should_ignore_opcode_sequence(opcodes: list[tuple], ml_context: dict) -> bool:
    """
    Determine if an opcode sequence should be ignored based on ML context.
    """
    if not ml_context.get("is_ml_content"):
        return False

    # High confidence ML content - be very permissive with opcode sequences
    if ml_context.get("overall_confidence", 0) > 0.7:
        return True

    # Medium confidence - check for specific ML patterns
    if ml_context.get("overall_confidence", 0) > 0.4:
        # Look for legitimate ML construction patterns
        reduce_count = sum(1 for opcode, _, _ in opcodes if opcode.name == "REDUCE")
        global_count = sum(1 for opcode, _, _ in opcodes if opcode.name == "GLOBAL")

        # High REDUCE/GLOBAL ratio suggests ML object construction
        if global_count > 0 and reduce_count / global_count > 0.5:
            return True

    return False


def _get_context_aware_severity(
    base_severity: IssueSeverity, ml_context: dict
) -> IssueSeverity:
    """
    Adjust severity based on ML context confidence.
    """
    if not ml_context.get("is_ml_content"):
        return base_severity

    confidence = ml_context.get("overall_confidence", 0)

    # High confidence ML content - downgrade severity
    if confidence > 0.8:
        if base_severity == IssueSeverity.CRITICAL:
            return IssueSeverity.WARNING
        elif base_severity == IssueSeverity.WARNING:
            return IssueSeverity.INFO
    elif confidence > 0.5:
        if base_severity == IssueSeverity.CRITICAL:
            return IssueSeverity.WARNING

    return base_severity


# ============================================================================
# END SMART DETECTION SYSTEM
# ============================================================================


def _is_legitimate_serialization_file(path: str) -> bool:
    """
    Validate that a file is a legitimate joblib or dill serialization file.
    This helps prevent security bypass by simply renaming malicious files.
    """
    try:
        with open(path, "rb") as f:
            # Read first few bytes to check for pickle magic
            header = f.read(10)
            if not header:
                return False

            # Check for standard pickle protocols (0-5)
            # Protocol 0: starts with '(' or other opcodes
            # Protocol 1: starts with ']' or other opcodes
            # Protocol 2+: starts with '\x80' followed by protocol number
            first_byte = header[0:1]
            if first_byte == b"\x80":
                # Protocols 2-5 start with \x80 followed by protocol number
                if len(header) < 2 or header[1] not in (2, 3, 4, 5):
                    return False
            elif first_byte not in (b"(", b"]", b"}", b"c", b"l", b"d", b"t", b"p"):
                # Common pickle opcode starts for protocols 0-1
                return False

            # For joblib files, look for joblib-specific patterns
            if path.lower().endswith(".joblib"):
                f.seek(0)
                # Try to find joblib-specific markers in first 2KB
                sample = f.read(2048)
                # Look for joblib-specific indicators
                joblib_indicators = [
                    b"joblib",
                    b"sklearn",
                    b"numpy",
                    b"_joblib",
                    b"__main__",
                    b"_pickle",
                    b"NumpyArrayWrapper",
                ]
                return any(marker in sample for marker in joblib_indicators)

            # For dill files, they're usually just enhanced pickle
            elif path.lower().endswith(".dill"):
                # Dill files should contain standard pickle format
                # Additional validation could check for dill-specific patterns
                return True

        return False
    except (OSError, IOError):
        # File doesn't exist or can't be read
        return False
    except Exception:
        # Other errors (e.g., permissions) - be conservative
        return False


def is_suspicious_global(mod: str, func: str) -> bool:
    """Check if a module.function reference is suspicious"""
    if mod in SUSPICIOUS_GLOBALS:
        val = SUSPICIOUS_GLOBALS[mod]
        if val == "*":
            return True
        if isinstance(val, list) and func in val:
            return True
    return False


def is_suspicious_string(s: str) -> Optional[str]:
    """Check if a string contains suspicious patterns"""
    import re

    if not isinstance(s, str):
        return None

    for pattern in SUSPICIOUS_STRING_PATTERNS:
        match = re.search(pattern, s)
        if match:
            return pattern

    # Check for base64-like strings (long strings with base64 charset)
    if len(s) > 40 and re.match(r"^[A-Za-z0-9+/=]+$", s):
        return "potential_base64"

    return None


def is_dangerous_reduce_pattern(opcodes: list[tuple]) -> Optional[dict[str, Any]]:
    """
    Check for patterns that indicate a dangerous __reduce__ method
    Returns details about the dangerous pattern if found, None otherwise
    """
    # Look for common patterns in __reduce__ exploits
    for i, (opcode, arg, pos) in enumerate(opcodes):
        # Check for GLOBAL followed by REDUCE - common in exploits
        if (
            opcode.name == "GLOBAL"
            and i + 1 < len(opcodes)
            and opcodes[i + 1][0].name == "REDUCE"
        ):
            if isinstance(arg, str):
                parts = (
                    arg.split(" ", 1)
                    if " " in arg
                    else arg.rsplit(".", 1)
                    if "." in arg
                    else [arg, ""]
                )
                if len(parts) == 2:
                    mod, func = parts
                    return {
                        "pattern": "GLOBAL+REDUCE",
                        "module": mod,
                        "function": func,
                        "position": pos,
                        "opcode": opcode.name,
                    }

        # Check for INST or OBJ opcodes which can also be used for code execution
        if opcode.name in ["INST", "OBJ", "NEWOBJ"] and isinstance(arg, str):
            return {
                "pattern": f"{opcode.name}_EXECUTION",
                "argument": arg,
                "position": pos,
                "opcode": opcode.name,
            }

        # Check for suspicious attribute access patterns (GETATTR followed by CALL)
        if (
            opcode.name == "GETATTR"
            and i + 1 < len(opcodes)
            and opcodes[i + 1][0].name == "CALL"
        ):
            return {
                "pattern": "GETATTR+CALL",
                "attribute": arg,
                "position": pos,
                "opcode": opcode.name,
            }

        # Check for suspicious strings in STRING or BINSTRING opcodes
        if opcode.name in [
            "STRING",
            "BINSTRING",
            "SHORT_BINSTRING",
            "UNICODE",
        ] and isinstance(arg, str):
            suspicious_pattern = is_suspicious_string(arg)
            if suspicious_pattern:
                return {
                    "pattern": "SUSPICIOUS_STRING",
                    "string_pattern": suspicious_pattern,
                    "string_preview": arg[:50] + ("..." if len(arg) > 50 else ""),
                    "position": pos,
                    "opcode": opcode.name,
                }

    return None


def check_opcode_sequence(
    opcodes: list[tuple], ml_context: dict
) -> list[dict[str, Any]]:
    """
    Analyze the full sequence of opcodes for suspicious patterns
    with ML context awareness.
    Returns a list of suspicious patterns found.
    """
    suspicious_patterns: list[dict[str, Any]] = []

    # SMART DETECTION: Check if we should ignore this sequence based on ML context
    if _should_ignore_opcode_sequence(opcodes, ml_context):
        return suspicious_patterns  # Return empty list for legitimate ML content

    # Count dangerous opcodes with ML context awareness
    dangerous_opcode_count = 0
    consecutive_dangerous = 0
    max_consecutive = 0

    for i, (opcode, arg, pos) in enumerate(opcodes):
        # Track dangerous opcodes
        if opcode.name in DANGEROUS_OPCODES:
            dangerous_opcode_count += 1
            consecutive_dangerous += 1
            max_consecutive = max(max_consecutive, consecutive_dangerous)
        else:
            consecutive_dangerous = 0

        # SMART DETECTION: Much higher threshold for ML content
        ml_confidence = ml_context.get("overall_confidence", 0)
        if ml_confidence > 0.7:
            threshold = 100  # Very high threshold for high-confidence ML
        elif ml_confidence > 0.4:
            threshold = 50  # Higher threshold for medium-confidence ML
        else:
            threshold = 20  # Still higher than original 5 for unknown content

        # If we see too many dangerous opcodes AND it's not clearly ML content
        if dangerous_opcode_count > threshold:
            suspicious_patterns.append(
                {
                    "pattern": "MANY_DANGEROUS_OPCODES",
                    "count": dangerous_opcode_count,
                    "max_consecutive": max_consecutive,
                    "ml_confidence": ml_confidence,
                    "position": pos,
                    "opcode": opcode.name,
                },
            )
            # Reset counter to avoid multiple alerts
            dangerous_opcode_count = 0
            max_consecutive = 0

    return suspicious_patterns


class PickleScanner(BaseScanner):
    """Scanner for Python Pickle files"""

    name = "pickle"
    description = "Scans Python pickle files for suspicious code references"
    supported_extensions = [
        ".pkl",
        ".pickle",
        ".dill",
        ".joblib",
        ".bin",
        ".pt",
        ".pth",
        ".ckpt",
    ]

    def __init__(self, config: Optional[dict[str, Any]] = None):
        super().__init__(config)
        # Additional pickle-specific configuration
        self.max_opcodes = self.config.get("max_opcodes", 1000000)

    @classmethod
    def can_handle(cls, path: str) -> bool:
        """Check if the file is a pickle based on extension and content"""
        file_ext = os.path.splitext(path)[1].lower()

        # For known pickle extensions, always handle
        if file_ext in [".pkl", ".pickle", ".dill", ".joblib"]:
            return True

        # For ambiguous extensions, check the actual file format
        if file_ext in [".bin", ".pt", ".pth", ".ckpt"]:
            try:
                # Import here to avoid circular dependency
                from modelaudit.utils.filetype import detect_file_format

                file_format = detect_file_format(path)
                return file_format == "pickle"
            except Exception:
                # If detection fails, fall back to extension check
                return file_ext in cls.supported_extensions

        return False

    def scan(self, path: str) -> ScanResult:
        """Scan a pickle file for suspicious content"""
        # Check if path is valid
        path_check_result = self._check_path(path)
        if path_check_result:
            return path_check_result

        result = self._create_result()
        file_size = self.get_file_size(path)
        result.metadata["file_size"] = file_size

        # Check if this is a .bin file that might be a PyTorch file
        is_bin_file = os.path.splitext(path)[1].lower() == ".bin"

        try:
            with open(path, "rb") as f:
                # Store the file path for use in issue locations
                self.current_file_path = path
                scan_result = self._scan_pickle_bytes(f, file_size)
                result.merge(scan_result)

                # For .bin files, also scan the remaining binary content
                # PyTorch files have pickle header followed by tensor data
                if is_bin_file and scan_result.success:
                    pickle_end_pos = f.tell()
                    remaining_bytes = file_size - pickle_end_pos

                    if remaining_bytes > 0:
                        # Check if this is likely a PyTorch model based on ML context
                        ml_context = scan_result.metadata.get("ml_context", {})
                        is_pytorch = "pytorch" in ml_context.get("frameworks", {})
                        ml_confidence = ml_context.get("overall_confidence", 0)

                        # Skip binary scanning for high-confidence ML model files
                        # as they contain tensor data that can trigger false positives
                        if is_pytorch and ml_confidence > 0.7:
                            result.metadata["binary_scan_skipped"] = True
                            result.metadata["skip_reason"] = (
                                "High-confidence PyTorch model detected"
                            )
                            result.bytes_scanned = file_size
                            result.metadata["pickle_bytes"] = pickle_end_pos
                            result.metadata["binary_bytes"] = remaining_bytes
                        else:
                            # Scan the binary content after pickle
                            binary_result = self._scan_binary_content(
                                f, pickle_end_pos, file_size
                            )

                            # Add binary scanning results
                            for issue in binary_result.issues:
                                result.add_issue(
                                    message=issue.message,
                                    severity=issue.severity,
                                    location=issue.location,
                                    details=issue.details,
                                    why=issue.why,
                                )

                            # Update total bytes scanned
                            result.bytes_scanned = file_size
                            result.metadata["pickle_bytes"] = pickle_end_pos
                            result.metadata["binary_bytes"] = remaining_bytes

        except Exception as e:
            result.add_issue(
                f"Error opening pickle file: {str(e)}",
                severity=IssueSeverity.CRITICAL,
                location=path,
                details={"exception": str(e), "exception_type": type(e).__name__},
            )
            result.finish(success=False)
            return result

        result.finish(success=True)
        return result

    def _scan_pickle_bytes(self, file_obj: BinaryIO, file_size: int) -> ScanResult:
        """Scan pickle file content for suspicious opcodes"""
        result = self._create_result()
        opcode_count = 0
        suspicious_count = 0

        try:
            # Process the pickle
            start_pos = file_obj.tell()

            # Store opcodes for pattern analysis
            opcodes = []
            # Track strings on the stack for STACK_GLOBAL opcode analysis
            string_stack = []

            for opcode, arg, pos in pickletools.genops(file_obj):
                opcodes.append((opcode, arg, pos))
                opcode_count += 1

                # Track strings for STACK_GLOBAL analysis
                if opcode.name in [
                    "STRING",
                    "BINSTRING",
                    "SHORT_BINSTRING",
                    "SHORT_BINUNICODE",
                    "UNICODE",
                ] and isinstance(arg, str):
                    string_stack.append(arg)
                    # Keep only the last 10 strings to avoid memory issues
                    if len(string_stack) > 10:
                        string_stack.pop(0)

                # Check for too many opcodes
                if opcode_count > self.max_opcodes:
                    result.add_issue(
                        f"Too many opcodes in pickle (> {self.max_opcodes})",
                        severity=IssueSeverity.INFO,
                        location=self.current_file_path,
                        details={
                            "opcode_count": opcode_count,
                            "max_opcodes": self.max_opcodes,
                        },
                        why=get_pattern_explanation("pickle_size_limit"),
                    )
                    break

                # Check for timeout
                if time.time() - result.start_time > self.timeout:
                    result.add_issue(
                        f"Scanning timed out after {self.timeout} seconds",
                        severity=IssueSeverity.INFO,
                        location=self.current_file_path,
                        details={"opcode_count": opcode_count, "timeout": self.timeout},
                        why="The scan exceeded the configured time limit. Large or complex pickle files may take longer to analyze due to the number of opcodes that need to be processed.",
                    )
                    break

            # SMART DETECTION: Analyze ML context once for the entire pickle
            ml_context = _detect_ml_context(opcodes)

            # Add ML context to metadata for debugging
            result.metadata.update(
                {
                    "ml_context": ml_context,
                    "opcode_count": opcode_count,
                    "suspicious_count": suspicious_count,
                }
            )

            # Now analyze the collected opcodes with ML context awareness
            for opcode, arg, pos in opcodes:
                # Check for GLOBAL opcodes that might reference suspicious modules
                if opcode.name == "GLOBAL":
                    if isinstance(arg, str):
                        # Handle both "module function" and "module.function" formats
                        parts = (
                            arg.split(" ", 1)
                            if " " in arg
                            else arg.rsplit(".", 1)
                            if "." in arg
                            else [arg, ""]
                        )

                        if len(parts) == 2:
                            mod, func = parts
                            if _is_actually_dangerous_global(mod, func, ml_context):
                                suspicious_count += 1
                                severity = _get_context_aware_severity(
                                    IssueSeverity.CRITICAL, ml_context
                                )
                                result.add_issue(
                                    f"Suspicious reference {mod}.{func}",
                                    severity=severity,
                                    location=f"{self.current_file_path} (pos {pos})",
                                    details={
                                        "module": mod,
                                        "function": func,
                                        "position": pos,
                                        "opcode": opcode.name,
                                        "ml_context_confidence": ml_context.get(
                                            "overall_confidence", 0
                                        ),
                                    },
                                    why=get_import_explanation(mod),
                                )

                # SMART DETECTION: Only flag REDUCE opcodes if not clearly ML content
                if opcode.name == "REDUCE" and not ml_context.get(
                    "is_ml_content", False
                ):
                    severity = _get_context_aware_severity(
                        IssueSeverity.WARNING, ml_context
                    )
                    result.add_issue(
                        "Found REDUCE opcode - potential __reduce__ method execution",
                        severity=severity,
                        location=f"{self.current_file_path} (pos {pos})",
                        details={
                            "position": pos,
                            "opcode": opcode.name,
                            "ml_context_confidence": ml_context.get(
                                "overall_confidence", 0
                            ),
                        },
                        why=get_opcode_explanation("REDUCE"),
                    )

                # SMART DETECTION: Only flag other dangerous opcodes
                # if not clearly ML content
                if opcode.name in ["INST", "OBJ", "NEWOBJ"] and not ml_context.get(
                    "is_ml_content", False
                ):
                    severity = _get_context_aware_severity(
                        IssueSeverity.WARNING, ml_context
                    )
                    result.add_issue(
                        f"Found {opcode.name} opcode - potential code execution",
                        severity=severity,
                        location=f"{self.current_file_path} (pos {pos})",
                        details={
                            "position": pos,
                            "opcode": opcode.name,
                            "argument": str(arg),
                            "ml_context_confidence": ml_context.get(
                                "overall_confidence", 0
                            ),
                        },
                        why=get_opcode_explanation(opcode.name),
                    )

                # Check for suspicious strings
                if opcode.name in [
                    "STRING",
                    "BINSTRING",
                    "SHORT_BINSTRING",
                    "UNICODE",
                ] and isinstance(arg, str):
                    suspicious_pattern = _is_actually_dangerous_string(arg, ml_context)
                    if suspicious_pattern:
                        severity = _get_context_aware_severity(
                            IssueSeverity.WARNING, ml_context
                        )
                        result.add_issue(
                            f"Suspicious string pattern: {suspicious_pattern}",
                            severity=severity,
                            location=f"{self.current_file_path} (pos {pos})",
                            details={
                                "position": pos,
                                "opcode": opcode.name,
                                "pattern": suspicious_pattern,
                                "string_preview": arg[:50]
                                + ("..." if len(arg) > 50 else ""),
                                "ml_context_confidence": ml_context.get(
                                    "overall_confidence", 0
                                ),
                            },
                            why=get_pattern_explanation("encoded_strings")
                            if suspicious_pattern == "potential_base64"
                            else "This string contains patterns that match known security risks such as shell commands, code execution functions, or encoded data.",
                        )

            # Check for STACK_GLOBAL patterns
            # (rebuild from opcodes to get proper context)
            for i, (opcode, arg, pos) in enumerate(opcodes):
                if opcode.name == "STACK_GLOBAL":
                    # Find the two immediately preceding STRING-like opcodes
                    # STACK_GLOBAL expects exactly two strings on the stack:
                    # module and function
                    recent_strings: list[str] = []
                    for j in range(
                        i - 1, max(0, i - 10), -1
                    ):  # Look back at most 10 opcodes
                        prev_opcode, prev_arg, prev_pos = opcodes[j]
                        if prev_opcode.name in [
                            "STRING",
                            "BINSTRING",
                            "SHORT_BINSTRING",
                            "SHORT_BINUNICODE",
                            "UNICODE",
                        ] and isinstance(prev_arg, str):
                            recent_strings.insert(
                                0, prev_arg
                            )  # Insert at beginning to maintain order
                            if len(recent_strings) >= 2:
                                break

                    if len(recent_strings) >= 2:
                        # The two strings are module and function in that order
                        mod = recent_strings[0]  # First string pushed (module)
                        func = recent_strings[1]  # Second string pushed (function)
                        if _is_actually_dangerous_global(mod, func, ml_context):
                            suspicious_count += 1
                            severity = _get_context_aware_severity(
                                IssueSeverity.CRITICAL, ml_context
                            )
                            result.add_issue(
                                f"Suspicious module reference found: {mod}.{func}",
                                severity=severity,
                                location=f"{self.current_file_path} (pos {pos})",
                                details={
                                    "module": mod,
                                    "function": func,
                                    "position": pos,
                                    "opcode": opcode.name,
                                    "ml_context_confidence": ml_context.get(
                                        "overall_confidence", 0
                                    ),
                                },
                                why=get_import_explanation(mod),
                            )
                    else:
                        # Only warn about insufficient context if not ML content
                        if not ml_context.get("is_ml_content", False):
                            result.add_issue(
                                "STACK_GLOBAL opcode found without "
                                "sufficient string context",
                                severity=IssueSeverity.INFO,
                                location=f"{self.current_file_path} (pos {pos})",
                                details={
                                    "position": pos,
                                    "opcode": opcode.name,
                                    "stack_size": len(recent_strings),
                                    "ml_context_confidence": ml_context.get(
                                        "overall_confidence", 0
                                    ),
                                },
                                why="STACK_GLOBAL requires two strings on the stack (module and function name) to import and access module attributes. Insufficient context prevents determining which module is being accessed.",
                            )

            # Check for dangerous patterns in the opcodes
            dangerous_pattern = is_dangerous_reduce_pattern(opcodes)
            if dangerous_pattern and not ml_context.get("is_ml_content", False):
                suspicious_count += 1
                severity = _get_context_aware_severity(
                    IssueSeverity.CRITICAL, ml_context
                )
                module_name = dangerous_pattern.get("module", "")
                result.add_issue(
                    f"Detected dangerous __reduce__ pattern with "
                    f"{dangerous_pattern.get('module', '')}."
                    f"{dangerous_pattern.get('function', '')}",
                    severity=severity,
                    location=f"{self.current_file_path} "
                    f"(pos {dangerous_pattern.get('position', 0)})",
                    details={
                        **dangerous_pattern,
                        "ml_context_confidence": ml_context.get(
                            "overall_confidence", 0
                        ),
                    },
                    why=get_import_explanation(module_name)
                    if module_name
                    else "A dangerous pattern was detected that could execute arbitrary code during unpickling.",
                )

            # Check for suspicious opcode sequences with ML context
            suspicious_sequences = check_opcode_sequence(opcodes, ml_context)
            for sequence in suspicious_sequences:
                suspicious_count += 1
                severity = _get_context_aware_severity(
                    IssueSeverity.WARNING, ml_context
                )
                result.add_issue(
                    f"Suspicious opcode sequence: {sequence.get('pattern', 'unknown')}",
                    severity=severity,
                    location=f"{self.current_file_path} "
                    f"(pos {sequence.get('position', 0)})",
                    details={
                        **sequence,
                        "ml_context_confidence": ml_context.get(
                            "overall_confidence", 0
                        ),
                    },
                    why="This pickle contains an unusually high concentration of opcodes that can execute code (REDUCE, INST, OBJ, NEWOBJ). Such patterns are uncommon in legitimate model files.",
                )

            # Update metadata
            end_pos = file_obj.tell()
            result.bytes_scanned = end_pos - start_pos
            result.metadata.update(
                {"opcode_count": opcode_count, "suspicious_count": suspicious_count},
            )

        except Exception as e:
            # Handle known issues with legitimate serialization files
            file_ext = os.path.splitext(self.current_file_path)[1].lower()

            # Pre-validate file legitimacy to avoid nested exceptions
            is_legitimate_file = False
            if file_ext in {".joblib", ".dill"}:
                try:
                    is_legitimate_file = _is_legitimate_serialization_file(
                        self.current_file_path
                    )
                except Exception:
                    # If validation itself fails, treat as non-legitimate
                    is_legitimate_file = False

            # Check if this is a known benign error in legitimate serialization files
            is_benign_error = (
                isinstance(e, (ValueError, struct.error))
                and any(
                    msg in str(e).lower()
                    for msg in [
                        "unknown opcode",
                        "unpack requires",
                        "truncated",
                        "bad marshal data",
                    ]
                )
                and file_ext in {".joblib", ".dill"}
                and is_legitimate_file
            )

            if is_benign_error:
                # Log for security auditing but treat as non-fatal
                logger.warning(
                    f"Truncated pickle scan of {self.current_file_path}: {e}. "
                    f"This may be due to non-pickle data after STOP opcode."
                )
                result.metadata.update(
                    {
                        "truncated": True,
                        "truncation_reason": "post_stop_data_or_format_issue",
                        "exception_type": type(e).__name__,
                        "exception_message": str(e)[:100],  # Limit message length
                        "validated_format": True,
                    }
                )
                # Still add as info-level issue for transparency
                result.add_issue(
                    f"Scan truncated due to format complexity: {type(e).__name__}",
                    severity=IssueSeverity.INFO,
                    location=self.current_file_path,
                    details={
                        "reason": "post_stop_data_or_format_issue",
                        "opcodes_analyzed": opcode_count,
                        "file_format": file_ext,
                    },
                    why="This file contains data after the pickle STOP opcode or uses format features that cannot be fully analyzed. The analyzable portion was scanned for security issues.",
                )
            else:
                # Treat as critical error for unknown/suspicious cases
                result.add_issue(
                    f"Error analyzing pickle ops: {e}",
                    severity=IssueSeverity.CRITICAL,
                    details={
                        "exception": str(e),
                        "exception_type": type(e).__name__,
                        "file_extension": file_ext,
                        "opcodes_analyzed": opcode_count,
                    },
                )

        return result

    def _scan_binary_content(
        self, file_obj: BinaryIO, start_pos: int, file_size: int
    ) -> ScanResult:
        """Scan the binary content after pickle data for suspicious patterns"""
        result = self._create_result()

        try:
            # Common patterns that might indicate embedded Python code
            code_patterns = [
                b"import os",
                b"import sys",
                b"import subprocess",
                b"eval(",
                b"exec(",
                b"__import__",
                b"compile(",
                b"os.system",
                b"subprocess.call",
                b"subprocess.Popen",
                b"socket.socket",
            ]

            # Executable signatures with additional validation
            # For PE files, we need to check for the full DOS header structure
            # to avoid false positives from random "MZ" bytes in model weights
            executable_sigs = {
                b"\x7fELF": "Linux executable (ELF)",
                b"\xfe\xed\xfa\xce": "macOS executable (Mach-O 32-bit)",
                b"\xfe\xed\xfa\xcf": "macOS executable (Mach-O 64-bit)",
                b"\xcf\xfa\xed\xfe": "macOS executable (Mach-O)",
                b"#!/bin/": "Shell script shebang",
                b"#!/usr/bin/": "Shell script shebang",
            }

            # Read in chunks
            chunk_size = 1024 * 1024  # 1MB chunks
            bytes_scanned = 0

            while True:
                chunk = file_obj.read(chunk_size)
                if not chunk:
                    break

                current_offset = start_pos + bytes_scanned
                bytes_scanned += len(chunk)

                # Check for code patterns
                for pattern in code_patterns:
                    if pattern in chunk:
                        pos = chunk.find(pattern)
                        result.add_issue(
                            f"Suspicious code pattern in binary data: {pattern.decode('ascii', errors='ignore')}",
                            severity=IssueSeverity.INFO,
                            location=f"{self.current_file_path} (offset: {current_offset + pos})",
                            details={
                                "pattern": pattern.decode("ascii", errors="ignore"),
                                "offset": current_offset + pos,
                                "section": "binary_data",
                            },
                            why="Python code patterns found in binary sections of the file. Model weights are typically numeric data and should not contain readable code strings.",
                        )

                # Check for executable signatures
                for sig, description in executable_sigs.items():
                    if sig in chunk:
                        pos = chunk.find(sig)
                        result.add_issue(
                            f"Executable signature found in binary data: {description}",
                            severity=IssueSeverity.CRITICAL,
                            location=f"{self.current_file_path} (offset: {current_offset + pos})",
                            details={
                                "signature": sig.hex(),
                                "description": description,
                                "offset": current_offset + pos,
                                "section": "binary_data",
                            },
                            why="Executable files embedded in model data can run arbitrary code on the system. Model files should contain only serialized weights and configuration data.",
                        )

                # Special check for Windows PE files with more validation
                # to reduce false positives from random "MZ" bytes
                pe_sig = b"MZ"
                if pe_sig in chunk:
                    pos = chunk.find(pe_sig)
                    # For PE files, check if we have enough data to validate DOS header
                    if pos + 64 <= len(chunk):  # DOS header is 64 bytes
                        # Check for "This program cannot be run in DOS mode" string
                        # which appears in all PE files
                        dos_stub_msg = b"This program cannot be run in DOS mode"
                        # Look for this message within reasonable distance from MZ
                        search_end = min(pos + 512, len(chunk))
                        if dos_stub_msg in chunk[pos:search_end]:
                            result.add_issue(
                                "Executable signature found in binary data: Windows executable (PE)",
                                severity=IssueSeverity.CRITICAL,
                                location=f"{self.current_file_path} (offset: {current_offset + pos})",
                                details={
                                    "signature": pe_sig.hex(),
                                    "description": "Windows executable (PE) with valid DOS stub",
                                    "offset": current_offset + pos,
                                    "section": "binary_data",
                                },
                                why="Windows executable files embedded in model data can run arbitrary code on the system. The presence of a valid DOS stub confirms this is an actual PE executable.",
                            )

                # Check for timeout
                if time.time() - result.start_time > self.timeout:
                    result.add_issue(
                        f"Binary scanning timed out after {self.timeout} seconds",
                        severity=IssueSeverity.INFO,
                        location=self.current_file_path,
                        details={
                            "bytes_scanned": start_pos + bytes_scanned,
                            "timeout": self.timeout,
                        },
                        why="The binary content scan exceeded the configured time limit. Large model files may require more time to fully analyze.",
                    )
                    break

            result.bytes_scanned = bytes_scanned

        except Exception as e:
            result.add_issue(
                f"Error scanning binary content: {str(e)}",
                severity=IssueSeverity.CRITICAL,
                location=self.current_file_path,
                details={"exception": str(e), "exception_type": type(e).__name__},
            )

        return result
