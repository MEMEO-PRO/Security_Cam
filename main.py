import cv2
import time
import datetime

cap = cv2.VideoCapture(0)
#haarcascade pretrained model for detecting faces bodies etc

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

#Variables initiation
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD = 5

frame_size = (int(cap.get(3)), int(cap.get(4)))             #Gets frame size of the device used
fourcc = cv2.VideoWriter_fourcc(*"mp4v")                    #4 digit code m p 4 v , just separates mp4v
out = cv2.VideoWriter("video.mp4", fourcc, 20,frame_size)   #saves video name and video



while True:
    _, frame = cap.read()
    # changing input image to greyscale imagea as haarcascade uses greyscale image to process
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    bodies = face_cascade.detectMultiScale(gray, 1.1, 3)

    if len(faces) + len(bodies) > 0 :
        if detection:
            timer_started = False
        else:
            detection = True
            #Writing the name of the file
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording!!")
    elif detection:
        if timer_started:
            #Checking if timer is more or less than the preffered time after sus goes out of frame
            if time.time() -detection_stopped_time >= SECONDS_TO_RECORD:
                detection = False
                timer_started = False
                out.release()
                print("Stopped Recording!!")
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)


    out.write(frame)

#Draws Rectangle on the colorfull image
    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y+height), (0, 0,255), 3)


#shows camera named window and shows frame

    #cv2.imshow("camera", frame)
#if pressed q it quits
    if cv2.waitKey(1) == ord('q'):
        break
#releasing the memory
out.release()
cap.release()
cv2.destroyAllWindows()
