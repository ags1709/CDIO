import os
HOME = os.getcwd()
print(HOME)

# run in terminal to use both gpus: export CUDA_VISIBLE_DEVICES=0,1
# unbuffer python3 train_gpu.py | tee run_gpu.txt
# !nvidia-smi
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126


import ultralytics
ultralytics.checks()

import torch
from ultralytics import YOLO

# Model Size 'n' for nano, 's' for small, 'm' for medium, 'l' for large, 'x' for extra large
model_size = 'l'  # Change this to 'n', 's', 'm', 'l', or 'x' as needed

model_name = f'yolov8{model_size}.pt'
model = YOLO(model_name)
model.model.load_pretrained = False

# if torch.cuda.is_available() and torch.cuda.device_count() > 1:
#     print(f"Training on {torch.cuda.device_count()} GPUs.")
#     # Wrap the model with DataParallel
#     model = torch.nn.DataParallel(model)  # Automatically uses all available GPUs

# Move model to GPUs
model = model.cuda()

dloc = f"{HOME}/dataset/"

# Train

print(f"Training YOLOv8{model_size.upper()} model...")

train_config = {
    'epochs': 200,  # Number of training epochs
    'patience': 50,  # Early stopping patience
    'batch': 16,  # Batch size
    'imgsz': 1280,  # Input image size for training
    #'device': 'cuda' if torch.cuda.is_available() else 'cpu',  # Use GPU if available
    'device': '1,3',
    'data': f"{dloc}data.yaml",  # Path to dataset YAML file
    'project': 'runs/train',  # Path to save training results
    'name': 'experiment',  # Name of the experiment
    'save_period': 20,  # Save checkpoint every 'n' epochs
    'verbose': True  # Enable verbose output
}


model.train(**train_config)
#results = model.train(data=f"{dloc}data.yaml", epochs=25, batch_size=80)
model.save(f'yolov8_{model_size}.pt')
#os.system(f"yolo task=detect mode=train model=yolov8l.pt data={dloc}data.yaml epochs=50 imgsz=800 plots=True device=cpu")

# Detecting
#print("Detecting")
#os.system(f"yolo task=detect mode=predict model={HOME}/runs/detect/train1/weights/best.pt conf=0.5 source={dloc}/test/images save=True")