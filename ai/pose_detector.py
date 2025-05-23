
import cv2
import mediapipe as mp
import time
import sys

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def detect_pose(file):
    cap = cv2.VideoCapture(file)
    if not cap.isOpened():
        print("영상을 실행할 수 없습니다.")
        return

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        last_movement_time = time.time()
        prev_landmarks = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            # 이미지 전처리
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # 움직임 판단 (관절 이동량 기반)
                landmarks = results.pose_landmarks.landmark
                if prev_landmarks:
                    movement = sum(
                        ((l.x - p.x) ** 2 + (l.y - p.y) ** 2) ** 0.5
                        for l, p in zip(landmarks, prev_landmarks)
                    )
                    if movement > 0.01:  # 민감도 조절
                        last_movement_time = time.time()
                prev_landmarks = landmarks

                # 이상행동 감지 (10초 이상 움직임 없음)
                if time.time() - last_movement_time > 10:
                    cv2.putText(image, '!!! 이상행동 감지 !!!', (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            cv2.imshow('Pose Detector', image)
            if cv2.waitKey(5) & 0xFF == 27:  # ESC 눌러서 종료
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python pose_detector.py [비디오 파일 경로]")
    else:
        detect_pose(sys.argv[1])