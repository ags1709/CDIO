import os
import xml.etree.ElementTree as ET

# Define paths
xml_dir = "imageRecognition/data/labeledImages"  # Path to XML files
yolo_dir = "imageRecognition/data/train/labels"  # Path where YOLO txt files should be saved
image_dir = "imageRecognition/data/train/labels/images"  # Path where images are stored
classes_file = "classes.txt"  # Path to save class names (optional)

# Ensure YOLO output directory exists
os.makedirs(yolo_dir, exist_ok=True)

# Set to hold unique class names
class_names = set()

# Function to convert XML to YOLO format
def convert_xml_to_yolo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Get image size
    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    yolo_data = []
    
    # Parse each object
    for obj in root.findall("object"):
        class_name = obj.find("name").text
        class_names.add(class_name)  # Add the class name to the set

        bbox = obj.find("bndbox")
        
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        # Normalize coordinates
        x_center = (xmin + xmax) / (2 * img_width)
        y_center = (ymin + ymax) / (2 * img_height)
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        # Append YOLO format data
        yolo_data.append(f"{class_name} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    # Write to YOLO file
    txt_filename = os.path.join(yolo_dir, os.path.basename(xml_file).replace(".xml", ".txt"))
    with open(txt_filename, "w") as f:
        f.write("\n".join(yolo_data))

# Process all XML files in the directory
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith(".xml"):
        convert_xml_to_yolo(os.path.join(xml_dir, xml_file))

# Save class names to a file (optional)
with open(classes_file, "w") as f:
    for class_name in sorted(class_names):
        f.write(f"{class_name}\n")

print("Conversion complete! YOLO annotations saved in:", yolo_dir)
print(f"Class names saved in: {classes_file}")
