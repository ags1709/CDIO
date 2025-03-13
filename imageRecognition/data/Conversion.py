import os
import xml.etree.ElementTree as ET

#CHAT CODE

# Define paths
xml_dir = "imageRecognition/data/labeledImages"  # Path to XML files
yolo_dir = "imageRecognition/data/Yolo"  # Output path for YOLO txt files

# Ensure YOLO output directory exists
os.makedirs(yolo_dir, exist_ok=True)

# Function to convert XML to YOLO format
def convert_xml_to_yolo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Get image size
    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    yolo_data = []
    
    # Parse each object in the XML
    for obj in root.findall("object"):
        class_name = obj.find("name").text

        # Get the class index from the object name
        # You can create a unique mapping for class names, or just use a dictionary
        class_id = hash(class_name) % 1000  # Use hash of class name as class_id

        # Extract bounding box coordinates
        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        # Normalize coordinates to YOLO format
        x_center = (xmin + xmax) / (2 * img_width)
        y_center = (ymin + ymax) / (2 * img_height)
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        # Append YOLO format data
        yolo_data.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    # Write YOLO annotations to .txt file
    txt_filename = os.path.join(yolo_dir, os.path.basename(xml_file).replace(".xml", ".txt"))
    with open(txt_filename, "w") as f:
        f.write("\n".join(yolo_data))

# Process all XML files in the directory
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith(".xml"):
        xml_path = os.path.join(xml_dir, xml_file)
        convert_xml_to_yolo(xml_path)

print("Conversion complete! YOLO annotations saved in:", yolo_dir)
