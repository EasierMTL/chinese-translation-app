from optimum.onnxruntime.configuration import AutoQuantizationConfig
from optimum.onnxruntime import ORTQuantizer


def create_quantized_model(
    onnx_model_path: str,
    onnx_optimized_model_output_path: str,
    model_name: str = "Helsinki-NLP/opus-mt-zh-en",
    feature: str = "AutoModelForSeq2SeqLM",
):
    """Creates the graph optimized model
    """
    # The type of quantization to apply
    qconfig = AutoQuantizationConfig.arm64(is_static=False, per_channel=False)
    quantizer = ORTQuantizer.from_pretrained(model_name, feature=feature)

    # Quantize the model!
    quantizer.export(
        onnx_model_path=onnx_model_path,
        onnx_optimized_model_output_path=onnx_optimized_model_output_path,
        quantization_config=qconfig,
    )
