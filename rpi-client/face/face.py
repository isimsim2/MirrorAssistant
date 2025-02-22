import os

import face_recognition
import cv2
import numpy as np


class Face:
    def __init__(self):
        # Using Camera 0
        self.video = cv2.VideoCapture(0)

        # 필요한 변수들 생성
        self.face_locations = []
        self.face_encodings = []
        self.fileName = None
        self.check = True

        # 얼굴 사진 폴더가 있다면
        if os.path.isdir("./faceimg"):
            # 해당 폴더의 파일명을 모두 불러온다
            self.faceImageList = os.listdir("./faceimg")
        # 없다면
        else:
            # 생성하고 빈 List 처리
            os.makedirs("./faceimg")
            self.faceImageList = []

        # 이미지 리스트 출력
        print('Face Image List :', self.faceImageList)

        # 이미지 처리 시작
        self.frEncodingList = []

        for imgFileName in self.faceImageList:
            # 파일 이름을 통해 이미지 불러오기
            loadImg = face_recognition.load_image_file('./faceimg/{0}'.format(imgFileName))

            # 얼굴 인식을 위한 인코딩 처리
            loadImgEncoding = face_recognition.face_encodings(loadImg)[0]

            # 인코딩 정보를 리스트에 Append
            self.frEncodingList.append(loadImgEncoding)

    # 얼굴 인식
    # 해당 함수는 무한 Loop가 필요함
    def recognitionFace(self):
        # 영상의 Single Frame 로드
        ret, frame = self.video.read()

        # 빠른 프로세싱을 위해 Video Frame을 1/2 줄임
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # OpenCV의 BGR 색상을 얼굴 인식 라이브러리에서 쓰이는 RGB 컬러로 변환
        rgb_small_frame = small_frame[:, :, ::-1]

        # 다른 프레임 체크인지 확인
        if self.check:
            # 얼굴 위치 로드
            self.face_locations = face_recognition.face_locations(rgb_small_frame)

            # 얼굴 인코딩
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            # 인코딩 데이터 체크
            for face_encoding in self.face_encodings:
                # 등록된 얼굴중 가장 유사한 얼굴을 찾음
                matches = face_recognition.compare_faces(self.frEncodingList, face_encoding)

                # 얼굴이 얼마나 유사한가?
                face_distances = face_recognition.face_distance(self.frEncodingList, face_encoding)

                # 가장 유사한 얼굴 Index 찾음
                best_match_index = np.argmin(face_distances)

                # 매치가 된다면
                if matches[best_match_index]:
                    # 해당 File 명을 설정
                    self.fileName = self.faceImageList[best_match_index]

        # 체크 변수 값 변경
        self.check = not self.check

        # 파일명 리턴
        return self.fileName

    # 카메라 릴리즈
    def cameraRelease(self):
        self.video.release()
        cv2.destroyAllWindows()


