import onnxruntime as ort
import numpy as np
from PIL import Image

# Load model
session = ort.InferenceSession("model/best.onnx", providers=["CPUExecutionProvider"])

# Get input/output names
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def preprocess(image_path, size=224):
    # Load image with PIL
    img = Image.open(image_path).convert("RGB")
    # Resize
    img = img.resize((size, size))
    # Convert to numpy array
    img = np.array(img).astype(np.float32) / 255.0
    # HWC → CHW
    img = np.transpose(img, (2, 0, 1))
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    return img

def predict(image_path):
    img = preprocess(image_path)
    preds = session.run([output_name], {input_name: img})[0]
    class_id = int(np.argmax(preds))
    confidence = float(np.max(preds))
    return class_id == 0, confidence

# Example
cls, conf = predict("model/test2.JPEG")
print(f"is damaged: {cls}, confidence: {conf:.2f}")