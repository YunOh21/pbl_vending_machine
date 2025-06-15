# <img src="assets/vending-machine.png" width="30"/>전지적 자판기 시점👀

## 소개
- 평범한 음료 자판기에 관리 및 상품 안내 기능을 추가했습니다.
- RDB(SQLite)로 관리자/사용자에게 함께 보여야 할 데이터를 관리합니다.

## 디렉토리 구조
```
PBL_VENDING_MACHINE/
├── admin/         ← 관리자 웹 페이지
├── ai/            ← CCTV 
├── core/          ← 주문 로직
├── db/            ← DB 접근 로직 (db_admin, db_client)
├── ui/            ← PyQt 기반 자판기 프론트엔드
├── README.md
└── requirements.txt
```

## 개발 환경
|   |   |
|---|---|
|개발환경|![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white) ![DBeaver](https://img.shields.io/badge/DBeaver-382923?style=for-the-badge&logo=DBeaver&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white) ![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)|
|기술|![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=SQLAlchemy&logoColor=white) ![Qt](https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white) ![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![ScikitLearn](https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white) ![MediaPipe](https://img.shields.io/badge/mediapipe-0097A7?style=for-the-badge&logo=mediapipe&logoColor=white)|

## 설계
- 시나리오: 고객이 음료 구매
<p align="center">
  <img src="design/SequenceDiagram.jpg">
</p>

- 클래스 다이어그램
<img src="design/ClassDiagram.jpg">

- 데이터베이스 구조
<img src="design/ERD.png">

## 시연 영상

## 실행 방법
- 모든 명령어는 프로젝트 루트 디렉토리에서 실행해주세요.
### 0. 외부 라이브러리 설치
```
pip install -r requirements.txt
```
- 개발환경은 python 3.12.3, ubuntu 24.04입니다.
- Qt 앱 실행을 위해서는 OS에 Qt가 설치 되어 있어야 합니다.
- ubuntu 기준으로는 다음 명령어로 설치 가능합니다.
```
sudo apt update
sudo apt install python3-pyqt5
```

### 1. DB 생성 및 데이터 입력
```
python3 -m db.db_starter
```

### 2. 자판기 (PyQt)
- 자판기이므로 IoT로 구현가능하도록 PyQt로 UI를 제작했습니다.
```
python3 -m ui.main_window
```

### 3. 자판기 관리자 (웹페이지)
- 로컬호스트에서 실행됩니다.
- 관리자가 PC에서 접속하는 페이지로 가정하고 Flask를 사용하여 개발했습니다.
```
python3 -m admin.app
```

## 부가 기능: 이상행동 감지
- 자판기에 부착된 카메라가 있다고 가정하고, 자판기 근처에서 이상행동(쓰러짐, 폭력 등)이 있을 경우 파악하고자 했습니다.
- 개발을 위해 [UCF Crime Dataset](https://www.crcv.ucf.edu/research/real-world-anomaly-detection-in-surveillance-videos)을 사용했습니다.
- 현재 개발된 모델은 예측 정확도가 매우 낮으므로, 시각인공지능 학습 후 개선이 필요합니다.
<img src="assets/CCTV_mediapipe_with_random_forest.gif">
