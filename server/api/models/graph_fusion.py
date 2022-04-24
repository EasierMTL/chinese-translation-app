from optimum.onnxruntime.configuration import OptimizationConfig
from optimum.onnxruntime import ORTOptimizer


def create_graph_optimized_model(
    onnx_model_path: str,
    onnx_optimized_model_output_path: str,
    model_name: str = "Helsinki-NLP/opus-mt-zh-en",
    feature: str = "AutoModelForSeq2SeqLM",
):
    """Creates the graph optimized model
    """
    # optimization_config=99 enables all available graph optimisations
    optimization_config = OptimizationConfig(optimization_level=99)

    optimizer = ORTOptimizer.from_pretrained(
        model_name,
        feature=feature,
    )

    # Export the optimized model
    optimizer.export(
        onnx_model_path=onnx_model_path,
        onnx_optimized_model_output_path=onnx_optimized_model_output_path,
        optimization_config=optimization_config,
    )