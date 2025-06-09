import os
from pathlib import Path
import shutil

# ChatGPT
# Set the source directory where your .png and .txt files currently are
source_dir = Path("imageRecognition\customData\eggSet")  # Change this as needed
images_dir = source_dir / "images"
labels_dir = source_dir / "labels"

# Create output directories if they don't exist
images_dir.mkdir(exist_ok=True)
labels_dir.mkdir(exist_ok=True)

# Go through all files in the source directory
for file in source_dir.iterdir():
    if file.is_file():
        if file.suffix.lower() == ".png":
            shutil.move(str(file), images_dir / file.name)
            print(f"Moved image: {file.name}")
        elif file.suffix.lower() == ".txt":
            shutil.move(str(file), labels_dir / file.name)
            print(f"Moved label: {file.name}")

print("Done.")
