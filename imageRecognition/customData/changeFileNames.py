import os
import re

# === Configuration ===
directory = 'eggSet/labels'  # Replace this
new_batch_number = 5  # Desired batch number

# === Batch renaming function ===
def rename_and_renumber_files(directory, new_batch_number):
    pattern = re.compile(r'^batch\d+_picture\d+(\.\w+)$')  # Matches batchX_pictureY.<ext>
    
    # Collect matching files
    files = [f for f in os.listdir(directory) if pattern.match(f)]
    
    # Sort files to maintain consistent ordering
    files.sort()

    for i, filename in enumerate(files):
        ext = os.path.splitext(filename)[1]
        new_filename = f"batch{new_batch_number}_picture{i}{ext}"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")

# === Run ===
rename_and_renumber_files(directory, new_batch_number)
