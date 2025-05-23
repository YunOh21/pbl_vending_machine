import cv2, mediapipe as mp, numpy as np

def extract_pose_from_video(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False)
    cap = cv2.VideoCapture(video_path)

    features = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        if results.pose_landmarks:
            landmark_vector = []
            for lm in results.pose_landmarks.landmark:
                landmark_vector.extend([lm.x, lm.y, lm.z, lm.visibility])
            features.append(landmark_vector)
    cap.release()
    return features

import os
from tqdm import tqdm

X, y = [], []
train_root = "UCF_Crime_Split/train"

for cls in os.listdir(train_root):
    class_dir = os.path.join(train_root, cls)
    for file in tqdm(os.listdir(class_dir), desc=cls):
        if not file.endswith(".mp4"):
            continue
        video_path = os.path.join(class_dir, file)
        poses = extract_pose_from_video(video_path)
        X.extend(poses)
        y.extend([cls] * len(poses))
        
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, stratify=y)

clf = SVC(kernel='linear')
clf.fit(X_train, y_train)

print(classification_report(y_val, clf.predict(X_val)))

joblib.dump(clf, "svm_model.pkl")
joblib.dump(scaler, "scaler.pkl")