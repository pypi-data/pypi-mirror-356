from . import (
    base,
    flax_msgpack_scanner,
    gguf_scanner,
    joblib_scanner,
    keras_h5_scanner,
    manifest_scanner,
    numpy_scanner,
    oci_layer_scanner,
    onnx_scanner,
    pickle_scanner,
    pmml_scanner,
    pytorch_binary_scanner,
    pytorch_zip_scanner,
    safetensors_scanner,
    tf_savedmodel_scanner,
    tflite_scanner,
    weight_distribution_scanner,
    zip_scanner,
)

# Import scanner classes for direct use
from .base import BaseScanner, Issue, IssueSeverity, ScanResult
from .flax_msgpack_scanner import FlaxMsgpackScanner
from .gguf_scanner import GgufScanner
from .joblib_scanner import JoblibScanner
from .keras_h5_scanner import KerasH5Scanner
from .manifest_scanner import ManifestScanner
from .numpy_scanner import NumPyScanner
from .oci_layer_scanner import OciLayerScanner
from .onnx_scanner import OnnxScanner
from .pickle_scanner import PickleScanner
from .pmml_scanner import PmmlScanner
from .pytorch_binary_scanner import PyTorchBinaryScanner
from .pytorch_zip_scanner import PyTorchZipScanner
from .safetensors_scanner import SafeTensorsScanner
from .tf_savedmodel_scanner import TensorFlowSavedModelScanner
from .tflite_scanner import TFLiteScanner
from .weight_distribution_scanner import WeightDistributionScanner
from .zip_scanner import ZipScanner

# Create a registry of all available scanners
# Order matters - more specific scanners should come before generic ones
SCANNER_REGISTRY = [
    PickleScanner,
    PyTorchBinaryScanner,  # Must come before generic scanners for .bin files
    TensorFlowSavedModelScanner,
    KerasH5Scanner,
    OnnxScanner,
    PyTorchZipScanner,  # Must come before ZipScanner since .pt/.pth files are zip files
    GgufScanner,
    JoblibScanner,
    NumPyScanner,
    OciLayerScanner,
    ManifestScanner,
    PmmlScanner,
    WeightDistributionScanner,
    SafeTensorsScanner,
    FlaxMsgpackScanner,
    TFLiteScanner,
    ZipScanner,  # Generic zip scanner should be last
    # Add new scanners here as they are implemented
]

__all__ = [
    "BaseScanner",
    "GgufScanner",
    "Issue",
    "IssueSeverity",
    "JoblibScanner",
    "KerasH5Scanner",
    "ManifestScanner",
    "PmmlScanner",
    "NumPyScanner",
    "OciLayerScanner",
    "OnnxScanner",
    "PickleScanner",
    "PyTorchBinaryScanner",
    "PyTorchZipScanner",
    "SCANNER_REGISTRY",
    "SafeTensorsScanner",
    "FlaxMsgpackScanner",
    "TFLiteScanner",
    "ScanResult",
    "TensorFlowSavedModelScanner",
    "WeightDistributionScanner",
    "ZipScanner",
    "base",
    "gguf_scanner",
    "joblib_scanner",
    "keras_h5_scanner",
    "manifest_scanner",
    "numpy_scanner",
    "oci_layer_scanner",
    "onnx_scanner",
    "pickle_scanner",
    "pytorch_binary_scanner",
    "pytorch_zip_scanner",
    "safetensors_scanner",
    "flax_msgpack_scanner",
    "tflite_scanner",
    "pmml_scanner",
    "tf_savedmodel_scanner",
    "weight_distribution_scanner",
    "zip_scanner",
]
