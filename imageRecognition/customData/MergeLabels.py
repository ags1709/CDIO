import os
from pathlib import Path

# Set these to the two directories of label .txt files
dir1 = Path("labels")  # First source
dir2 = Path("NewLabels")  # Second source
output_dir = Path("merged_labels")
output_dir.mkdir(exist_ok=True)

# Go through all files in dir1
for label_file1 in dir1.glob("*.txt"):
    filename = label_file1.name
    label_file2 = dir2 / filename

    # Read labels from both files (if second one exists)
    labels1 = label_file1.read_text().strip().splitlines()
    labels2 = label_file2.read_text().strip().splitlines() if label_file2.exists() else []

    # Combine them
    merged = labels1 + labels2

    # Write to output
    (output_dir / filename).write_text("\n".join(merged) + "\n")
    print(f"Merged {filename}")

print("Done.")
