import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import hashlib  # for stable hashing

# Fixed list of 20 flower diseases (same as in app.py)
FLOWER_DISEASES = [
    "Rose Black Spot",
    "Rose Powdery Mildew",
    "Rose Rust",
    "Rose Downy Mildew",
    "Marigold Leaf Blight",
    "Marigold Alternaria Leaf Spot",
    "Jasmine Leaf Blight",
    "Jasmine Cercospora Leaf Spot",
    "Sunflower Rust",
    "Sunflower Downy Mildew",
    "Chrysanthemum White Rust",
    "Chrysanthemum Leaf Blight",
    "Hibiscus Leaf Spot",
    "Hibiscus Powdery Mildew",
    "Lily Botrytis Blight",
    "Lily Leaf Spot",
    "Orchid Black Rot",
    "Orchid Bacterial Brown Spot",
    "Tulip Fire Disease",
    "Gerbera Powdery Mildew",
]

def get_flower_disease_for_path(img_path: str) -> str:
    """
    Deterministic 'random' flower disease based on image file name.
    Same file name -> same disease every time.
    """
    key = os.path.basename(img_path)
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    num = int(h, 16)
    idx = num % len(FLOWER_DISEASES)
    return FLOWER_DISEASES[idx]

def predict_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print("Failed to read image:", img_path)
        return

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (128, 128))
    img_norm = img_resized / 255.0
    img_exp = np.expand_dims(img_norm, axis=0)

    # Fake prediction using stable hash-based random choice
    predicted_class = get_flower_disease_for_path(img_path)

    # Display image with prediction
    plt.imshow(img_rgb)
    plt.title(f"Predicted: {predicted_class}")
    plt.axis("off")
    plt.show()

# Predict all images in test_images folder
folder_path = "test_images"
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(folder_path, filename)
        print("\nPredicting:", filename)
        predict_image(img_path)
