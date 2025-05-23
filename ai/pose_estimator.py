import mediapipe as mp
import cv2
import numpy as np
from PIL import Image

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

def extract_pose_features_from_gif(gif_frames, size=(256, 256)):
    features = []
    for frame in gif_frames:
        img = Image.fromarray(frame).convert("RGB").resize(size)
        img_np = np.array(img)
        results = pose.process(cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR))
        if results.pose_landmarks:
            feature = []
            for lm in results.pose_landmarks.landmark:
                feature.extend([lm.x, lm.y, lm.z, lm.visibility])
            features.append(feature)
        else:
            features.append([0.0] * 132)  # 33 landmarks x 4
    return np.array(features)
