import os
import cv2
import mediapipe as mp
import numpy as np
from tqdm import tqdm

def extract_pose_from_video(video_path, max_frames=300):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False)
    cap = cv2.VideoCapture(video_path)

    features = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        if results.pose_landmarks:
            landmark_vector = []
            for lm in results.pose_landmarks.landmark:
                landmark_vector.extend([lm.x, lm.y, lm.z, lm.visibility])
            features.append(landmark_vector)
        frame_count += 1
        if frame_count >= max_frames:  # 너무 많은 프레임 방지
            break
    cap.release()
    return features

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import joblib
import matplotlib.pyplot as plt

# 데이터셋 경로 및 일부만 사용
X, y = [], []
train_root = "UCF_Crime_Split/train"
max_videos_per_class = 5  # 클래스당 최대 5개 파일만 사용 (테스트용)

for cls in os.listdir(train_root):
    class_dir = os.path.join(train_root, cls)
    video_files = [f for f in os.listdir(class_dir) if f.endswith(".mp4")]
    for file in tqdm(video_files[:max_videos_per_class], desc=f"{cls} (최대 {max_videos_per_class}개)"):
        video_path = os.path.join(class_dir, file)
        try:
            poses = extract_pose_from_video(video_path, max_frames=300)
            X.extend(poses)
            y.extend([cls] * len(poses))
        except Exception as e:
            print(f"Error processing {video_path}: {e}")

print(f"총 샘플 개수: {len(X)}")
if X:
    print(f"특징 벡터 차원: {len(X[0])}")

# 데이터 전처리 및 분할
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# RandomForest로 학습
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

# 성능 평가
print("Train set 성능:")
print(classification_report(y_train, clf.predict(X_train)))
print("Validation set 성능:")
print(classification_report(y_val, clf.predict(X_val)))

# Confusion matrix 시각화
y_pred = clf.predict(X_val)
cm = confusion_matrix(y_val, y_pred, labels=clf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
disp.plot(cmap='Blues')
plt.title("Validation Confusion Matrix")
plt.show()

# 모델 및 스케일러 저장
os.makedirs("output", exist_ok=True)
joblib.dump(clf, "output/rf_model.pkl")
joblib.dump(scaler, "output/scaler.pkl")

print("모델과 스케일러가 output 폴더에 저장되었습니다.")