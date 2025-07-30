import os

from .base import BaseScanner, IssueSeverity, ScanResult

try:
    import tflite

    HAS_TFLITE = True
except Exception:  # pragma: no cover - optional dependency
    HAS_TFLITE = False

# Thresholds to detect potential overflow or malicious sizes
_MAX_COUNT = 1_000_000
_MAX_DIM = 10_000_000


class TFLiteScanner(BaseScanner):
    """Scanner for TensorFlow Lite model files."""

    name = "tflite"
    description = "Scans TensorFlow Lite models for integrity and safety issues"
    supported_extensions = [".tflite"]

    @classmethod
    def can_handle(cls, path: str) -> bool:
        if not HAS_TFLITE:
            return False
        return (
            os.path.isfile(path)
            and os.path.splitext(path)[1].lower() in cls.supported_extensions
        )

    def scan(self, path: str) -> ScanResult:
        path_check_result = self._check_path(path)
        if path_check_result:
            return path_check_result

        result = self._create_result()
        result.metadata["file_size"] = self.get_file_size(path)

        if not HAS_TFLITE:
            result.add_issue(
                "tflite package not installed. Install with 'pip install modelaudit[tflite]'",
                severity=IssueSeverity.CRITICAL,
                location=path,
            )
            result.finish(success=False)
            return result

        try:
            with open(path, "rb") as f:
                data = f.read()
                result.bytes_scanned = len(data)
            model = tflite.Model.Model.GetRootAsModel(data, 0)
        except Exception as e:  # pragma: no cover - parse errors
            result.add_issue(
                f"Invalid TFLite file or parse error: {e}",
                severity=IssueSeverity.CRITICAL,
                location=path,
                details={"exception": str(e), "exception_type": type(e).__name__},
            )
            result.finish(success=False)
            return result

        subgraph_count = model.SubgraphsLength()
        result.metadata["subgraph_count"] = subgraph_count
        if subgraph_count > _MAX_COUNT:
            result.add_issue(
                f"Model declares {subgraph_count} subgraphs which exceeds the safe limit",
                severity=IssueSeverity.CRITICAL,
                location=path,
            )

        for sg_index in range(subgraph_count):
            subgraph = model.Subgraphs(sg_index)
            tensors_len = subgraph.TensorsLength()
            operators_len = subgraph.OperatorsLength()
            result.metadata.setdefault("tensor_counts", []).append(tensors_len)
            result.metadata.setdefault("operator_counts", []).append(operators_len)

            if tensors_len > _MAX_COUNT or operators_len > _MAX_COUNT:
                result.add_issue(
                    "TFLite model has extremely large tensor or operator count",
                    severity=IssueSeverity.CRITICAL,
                    location=path,
                    details={"tensors": tensors_len, "operators": operators_len},
                )
                continue

            for t_index in range(tensors_len):
                tensor = subgraph.Tensors(t_index)
                shape = [tensor.Shape(i) for i in range(tensor.ShapeLength())]
                if any(dim > _MAX_DIM for dim in shape):
                    result.add_issue(
                        "Tensor dimension extremely large (possible overflow)",
                        severity=IssueSeverity.CRITICAL,
                        location=f"{path} (tensor {t_index})",
                        details={"shape": shape},
                    )

            for o_index in range(operators_len):
                op = subgraph.Operators(o_index)
                opcode = model.OperatorCodes(op.OpcodeIndex())
                builtin = opcode.BuiltinCode()
                if builtin == tflite.BuiltinOperator.CUSTOM:
                    custom = opcode.CustomCode()
                    name = custom.decode("utf-8", "ignore") if custom else "unknown"
                    result.add_issue(
                        f"Model uses custom operator '{name}'",
                        severity=IssueSeverity.WARNING,
                        location=f"{path} (operator {o_index})",
                        details={"custom_op": name},
                    )

        result.finish(success=not result.has_errors)
        return result
