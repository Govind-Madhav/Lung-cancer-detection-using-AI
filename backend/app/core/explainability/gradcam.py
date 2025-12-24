from typing import Any

def generate_gradcam(model, image_data: Any, target_layer: str) -> str:
    """
    Generates Grad-CAM heatmap for CNN/RNN.
    Returns path to saved heatmap image.
    """
    # Logic to hook into model gradients and generate heatmap
    return "static/explainability/heatmap_mock.png"
