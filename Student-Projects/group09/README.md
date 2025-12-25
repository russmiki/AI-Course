# Group 9

Object Detection Web Application with YOLOv8

group members :
1. Hanie Asali
2. h
3. r
4. m
5. s


A complete web-based computer vision application for real-time object detection using YOLOv8 and Streamlit.
Table of Contents

    Project Overview
    Features
    Installation
    Usage
    Project Structure
    Dependencies
    Configuration
    How It Works
    Output
    Troubleshooting


Project Overview

This application provides a user-friendly interface for detecting objects in images using the state-of-the-art YOLOv8 (You Only Look Once version 8) object detection model. It processes uploaded images, identifies objects with bounding boxes, and provides detailed statistics about the detected objects.
Features

    Image Upload: Supports JPG, PNG, and JPEG formats

    Multiple Models: Choose between YOLOv8n, YOLOv8s, and YOLOv8m models

    Real-time Detection: Instant object detection with visual feedback

    Detailed Analytics: Object counts, confidence scores, and statistics

    Export Functionality: Download processed images and CSV data

    Responsive UI: Clean interface with sidebar controls

    Modular Code: Well-organized project structure

Installation
Prerequisites

    Python 3.8 or higher

    pip package manager

Step-by-Step Setup

    Clone or create project directory

mkdir object-detection-app
cd object-detection-app

    Create project structure

mkdir utils
mkdir models

    Create required files

# On Windows:
type nul > app.py
type nul > requirements.txt
type nul > utils\__init__.py
type nul > utils\detection.py
type nul > utils\counting.py

# On Mac/Linux:
touch app.py requirements.txt
touch utils/__init__.py utils/detection.py utils/counting.py

    Install dependencies
    Add the following to requirements.txt:

ultralytics==8.0.196
streamlit==1.28.0
opencv-python==4.8.1.78
pandas==2.1.1
Pillow==10.0.0

Then install:
pip install -r requirements.txt

Usage
Running the Application

streamlit run app.py

The application will open in your default web browser at http://localhost:8501.
Using the Application

    Upload Image: Use the file uploader in the sidebar to select an image

    Select Model: Choose from available YOLOv8 models (nano, small, medium)

    View Results:

        Left panel: Original image

        Right panel: Processed image with bounding boxes

    Analyze Data: Review detection statistics and object counts

    Export Results: Download the processed image and CSV data

Project Structure

object-detection-app/
 app.py                 # Main Streamlit application
 requirements.txt       # Python dependencies
 models/                # YOLO model storage
 utils/                 # Utility modules
    __init__.py       # Package initializer
    detection.py      # Object detection logic
    counting.py       # Statistics functions
 

Dependencies

    ultralytics: YOLOv8 implementation and model loading

    streamlit: Web application framework

    opencv-python: Image processing and computer vision

    pandas: Data manipulation and CSV export

    Pillow: Image handling and processing

Configuration
Model Selection

The application supports three YOLOv8 models:

    yolov8n.pt: Nano model (fastest, least accurate)

    yolov8s.pt: Small model (balanced speed/accuracy)

    yolov8m.pt: Medium model (slower, more accurate)

Detection Parameters

    Confidence threshold: Built into YOLOv8 model

    Non-maximum suppression: Automatic

    Class filtering: All 80+ COCO dataset classes available

How It Works
1. Image Processing Pipeline
 
Upload → Preprocess → YOLOv8 Detection → Bounding Box Drawing → Results Display

3. Detection Process

    Image is loaded and converted to appropriate format

    YOLOv8 model processes the image

    Bounding boxes are drawn around detected objects

    Confidence scores and class labels are added

    Results are displayed side-by-side with original

4. Data Extraction

    Object class names

    Confidence scores (0-1)

    Bounding box coordinates (x1, y1, x2, y2)

    Statistical analysis of detections

Output
1. Visual Output

    Processed image with colored bounding boxes

    Class labels and confidence scores on each detection

    Color-coded boxes for different object classes

2. Data Output (CSV Format)
csv

class,confidence,x1,y1,x2,y2
person,0.89,100,150,200,350
car,0.95,300,200,450,300
dog,0.78,50,400,150,500

3. Statistics

    Total objects detected

    Objects per category

    Average confidence score

    Detection distribution

Troubleshooting
Common Issues
Issue 1: Model fails to download

Solution: Check internet connection or download manually:

wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

Issue 2: Application runs slowly

Solution:

    Use yolov8n.pt instead of larger models

    Reduce image size before uploading

    Close other applications using GPU

Issue 3: Memory errors

Solution:

    Upload smaller images

    Use the nano model

    Restart the application

Issue 4: Import errors

Solution:

# Reinstall dependencies
pip uninstall -y ultralytics streamlit opencv-python pandas Pillow
pip install -r requirements.txt


