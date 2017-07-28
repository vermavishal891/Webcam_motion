import cv2
from datetime import datetime
import pandas

video = cv2.VideoCapture(0)

base_frame = None
time=[]
status_list=[0,0]
df = pandas.DataFrame(columns=["Start","End"])

while True:

    check, frame = video.read()
    status = 0
    bw_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    bw_frame = cv2.GaussianBlur(bw_frame,(21,21),0)

    if base_frame is None:
        base_frame = bw_frame
        continue

    delta_frame = cv2.absdiff(base_frame,bw_frame)

    thresh_delta = cv2.threshold(delta_frame,20,255,cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta,None,iterations = 2)

    (_,cnts,_) = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000 or cv2.contourArea(contour) < 5000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x, y), (x+w, y+h), (0,255,0),3)
    status_list[-2] = status_list[-1]
    status_list[-1] = status

    if status_list[-1] != status_list[-2]:
        time.append(datetime.now())

    cv2.imshow("color",frame)
    #cv2.imshow("BW",bw_frame)
    #cv2.imshow("delta",delta_frame)
    #cv2.imshow("Thresh",thresh_delta)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            time.append(datetime.now())
        break

video.release()
cv2.destroyAllWindows
for i in range(0,len(time),2):
    df = df.append({"Start":time[i],"End":time[i+1]},ignore_index = True)

df.to_csv("times.csv")
