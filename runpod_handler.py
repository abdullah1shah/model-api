import runpod
import base64
import numpy as np
import tensorflow as tf
from PIL import Image
import io
from tensorflow.keras.preprocessing.image import img_to_array
from pathlib import Path

# Constants
CLASS_NAMES = [
    "beaus lines", 
    "bluish nails", 
    "clubbing", 
    "healthy nails", 
    "koilonychia", 
    "melanoma",
    "muehrckes Lines", 
    "nail pitting", 
    "onychogryphosis", 
    "onycholysis", 
    "onychomycosis",
    "psoriasis", 
    "terrys nails"
]

MODEL_PATH = Path(__file__).resolve().parent / "cnn_model_final-v1.keras"
model = tf.keras.models.load_model(str(MODEL_PATH))

def preprocess_image(image, target_size=(256, 256)):
    image = image.resize(target_size)
    image_array = img_to_array(image)
    image_array /= 255.0
    return np.expand_dims(image_array, axis=0)

# The main function RunPod calls
def handler(event):
    try:
        # Decode base64 image string from JSON input
        base64_image = event['input']['image']
        image_data = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(image_data)).convert('RGB')

        # Preprocess and predict
        preprocessed_img = preprocess_image(img)
        predictions = model.predict(preprocessed_img)
        predicted_index = int(np.argmax(predictions))
        predicted_class = CLASS_NAMES[predicted_index]
        confidence = float(predictions[0][predicted_index])

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "class_index": predicted_index,
            "all_predictions": predictions.tolist()[0]
        }

    except Exception as e:
        return {"error": str(e)}

# Start the RunPod serverless function
runpod.serverless.start({"handler": handler})
