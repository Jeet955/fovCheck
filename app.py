import streamlit as st
import cv2
import tempfile
import yaml
import os

# Title
st.title("🎯 FOV Checker App")
st.write("Upload a video aur adjust karo x & y position of FOV box.")

# Load original rectangle values from YAML
with open("params.yaml", 'r') as file:
    params = yaml.safe_load(file)

# Streamlit sliders to dynamically adjust x and y
x = st.slider("🔧 Adjust X (Left-Right)", min_value=0, max_value=1920, value=params['rectangle']['x'])
y = st.slider("🔧 Adjust Y (Up-Down)", min_value=0, max_value=1080, value=params['rectangle']['y'])

# Keep width and height fixed from yaml
w = params['rectangle']['w']
h = params['rectangle']['h']

# Upload video
video_file = st.file_uploader("🎥 Upload a video", type=["mp4", "avi", "mov"])

if video_file is not None:
    # Save to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    # Open video
    cap = cv2.VideoCapture(tfile.name)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Draw rectangle with updated x, y
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

        # Optional delay
        #cv2.waitKey(30)

    cap.release()
    os.unlink(tfile.name)
