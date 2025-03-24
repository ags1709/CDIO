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
model = YOLO('yolov8m.yaml')

# if torch.cuda.is_available() and torch.cuda.device_count() > 1:
#     print(f"Training on {torch.cuda.device_count()} GPUs.")
#     # Wrap the model with DataParallel
#     model = torch.nn.DataParallel(model)  # Automatically uses all available GPUs

# Move model to GPUs
model = model.cuda()

dloc = f"{HOME}/PublicColoredShapes/"

# Train

print("Training")

train_config = {
    'epochs': 25,  # Number of training epochs
    'batch': 32,  # Batch size
    'imgsz': 800,  # Input image size for training
    #'device': 'cuda' if torch.cuda.is_available() else 'cpu',  # Use GPU if available
    'device': '0,1',
    'data': f"{dloc}data.yaml",  # Path to dataset YAML file
    'project': 'runs/train',  # Path to save training results
    'name': 'experiment',  # Name of the experiment
    'save_period': 10,  # Save checkpoint every 'n' epochs
    'verbose': True  # Enable verbose output
}


model.train(**train_config)

# Change the below name to a suitable name for the model
model.save('yolov8mRobotDetection.pt')