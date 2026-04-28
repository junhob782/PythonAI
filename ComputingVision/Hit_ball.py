import cv2
import numpy as np

class Ball(object):
    def __init__(mySelf):
        super().__init__()
        print("Ball object is created")
        mySelf.radius = 0 #반지름
        (mySelf.x,mySelf.y) = (0,0) #좌표값
        mySelf.is_activate = False
    def __del__(mySelf):
        print("Ball object is deleted")

import random
def get_random_position(frame_width, frame_height, radius):
    x = random.randint(radius, frame_width - radius)
    y = random.randint(radius, frame_height - radius)
    return (x,y)

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    exit("Could not start camera.")

#카메라 화면의 크기를 가져와야 함.

frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

#공을 초기화
red_ball = Ball()
red_ball.radius = 20
(red_ball.x, red_ball.y) = get_random_position(frame_width, frame_height, red_ball.radius)
red_ball.is_activate = True

score = 0
pre_gray_frame = None

while True:
    (ret, frame) = capture.read()

    if ret is None:
      print("Cannot capture frame")
      break

    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #가우시안 필터링으로 노이즈 제거
    cv2.GaussianBlur(gray_frame, (21, 21), 0)

    #첫 프레임 일 때
    if pre_gray_frame is None:
        pre_gray_frame = gray_frame.copy()
        continue

    # 움직임을 감지
    diff_frame = cv2.absdiff(pre_gray_frame, gray_frame)
    #이진화
    _, thresh_frame = cv2.threshold(diff_frame, 25, 255, cv2.THRESH_BINARY)

    #공과 충돌
    if red_ball.is_activate:
        (x1, y1 ) = (max(0, red_ball.x - red_ball.radius),
                     max(0, red_ball.y - red_ball.radius))
        (x2, y2)  = (min(frame_width, red_ball.x + red_ball.radius),
                     min(frame_height, red_ball.y + red_ball.radius))
        cv2.rectangle(frame, (x1, y1), (x2, y2),
                      (0,255,0), 2)
        roi = thresh_frame[y1:y2, x1:x2]
        movement_pixel = cv2.countNonZero(roi)

        #민감도 설정
        # cv2.countNonZero(roi)
        area = (x2-x1) * (y2-y1)
        if movement_pixel > area * 0.1:
            score += 1
            print(f"터치 점수 : {score}")
            (red_ball.x, red_ball.y) = get_random_position(frame_width,frame_height, red_ball.radius)

    cv2.circle(frame, (red_ball.x, red_ball.y),
               red_ball.radius, (0,0,255), -1) #공을 빨간색으로 채움
    #화면에 점수 표시
    cv2.putText(frame, f"Score : {score}", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, \
                (255,255,255), 2)



    cv2.imshow("GAME", frame)
    pre_gray_frame = gray_frame.copy()
    if cv2.waitKey(20) == 27:
        break
capture.release()
cv2.destroyAllWindows()