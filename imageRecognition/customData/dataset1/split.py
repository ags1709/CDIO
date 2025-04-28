import os
import random
import shutil

# Source directories
image_dir = './images'  # original image folder
label_dir = './labels'  # original label folder

# Output dataset directory
output_dir = './dataset'
splits = {
    'train': 0.7,
    'valid': 0.15,
    'test': 0.15
}

# Collect all images with corresponding label files
image_extensions = ['.jpg', '.jpeg', '.png']
all_image_files = [f for f in os.listdir(image_dir) if os.path.splitext(f)[1].lower() in image_extensions]

# Filter out any image that doesn't have a corresponding label
image_files = [f for f in all_image_files if os.path.exists(os.path.join(label_dir, os.path.splitext(f)[0] + '.txt'))]

# Shuffle the files
random.shuffle(image_files)

# Split the files
n_total = len(image_files)
n_train = int(n_total * splits['train'])
n_valid = int(n_total * splits['valid'])

train_files = image_files[:n_train]
valid_files = image_files[n_train:n_train + n_valid]
test_files = image_files[n_train + n_valid:]

# Helper to copy files
def copy_files(file_list, subset):
    img_out = os.path.join(output_dir, subset, 'images')
    lbl_out = os.path.join(output_dir, subset, 'labels')
    os.makedirs(img_out, exist_ok=True)
    os.makedirs(lbl_out, exist_ok=True)

    for img_file in file_list:
        base = os.path.splitext(img_file)[0]
        label_file = base + '.txt'
        shutil.copy(os.path.join(image_dir, img_file), os.path.join(img_out, img_file))
        shutil.copy(os.path.join(label_dir, label_file), os.path.join(lbl_out, label_file))

# Copy all sets
copy_files(train_files, 'train')
copy_files(valid_files, 'valid')
copy_files(test_files, 'test')

print("Dataset split complete:")
print(f"Train: {len(train_files)} images")
print(f"valid:   {len(valid_files)} images")
print(f"Test:  {len(test_files)} images")
