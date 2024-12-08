import os
import cv2
import shutil
import numpy as np
from skimage.metrics import structural_similarity as ssim


def calculate_similarity(img1_path, img2_path):
    """Calculate the similarity between two images."""
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        return -1  # Return a low similarity score if the image can't be loaded

    # Resize images to the same size for comparison
    img1 = cv2.resize(img1, (100, 100))
    img2 = cv2.resize(img2, (100, 100))

    # Compute SSIM between two images
    similarity = ssim(img1, img2)

    return similarity


def match_and_rename_images(old_folder, image_folder, new_folder, threshold=0.9):
    """Match images from image_folder to old_folder, rename and save them in new_folder."""
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    # Include .webp in the list of supported image extensions
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')

    old_images = [f for f in os.listdir(old_folder) if f.lower().endswith(supported_formats)]
    image_images = [f for f in os.listdir(image_folder) if f.lower().endswith(supported_formats)]

    for old_image in old_images:
        old_image_path = os.path.join(old_folder, old_image)
        best_match = None
        best_score = -1

        for image in image_images:
            image_path = os.path.join(image_folder, image)
            similarity = calculate_similarity(old_image_path, image_path)

            if similarity > best_score:
                best_score = similarity
                best_match = image

        # If the best match score is above the threshold, rename and save the image
        if best_match and best_score >= threshold:
            new_image_name = old_image  # use the name from the old folder
            old_name_path = os.path.join(image_folder, best_match)
            new_name_path = os.path.join(new_folder, new_image_name)

            shutil.copyfile(old_name_path, new_name_path)
            print(f"Matched and saved: {old_name_path} as {new_name_path}")


# Specify the folders
old_folder = r'C:\Users\10921\Desktop\old'
image_folder = r'C:\Users\10921\Desktop\image'
new_folder = r'C:\Users\10921\Desktop\new'

# Run the matching and renaming process
match_and_rename_images(old_folder, image_folder, new_folder)
