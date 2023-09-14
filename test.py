import numpy as np
import cv2 as cv
import time


# face_cascade = cv.CascadeClassifier("haarcascade_frontalface_alt.xml")
face_cascade = cv.CascadeClassifier()
face_cascade.load('haarcascade_frontalface_default.xml')

# q : quit the camera
# r : record
# s : stop record

# flag = true means recording
flag = False

# saveFace : the faces have been saved
saveFace = 0
# cap = cv.VideoCapture(0)
cap = cv.VideoCapture('http://192.168.247.227:4747/mjpegfeed')

# dims : dimensions
# dims (width,height)

dims = (1280, 720)

# Resize cap
cap.set(3, dims[0])  # width
cap.set(4, dims[1])  # height

# VideoWriter attributes
file = input('Please enter name : ')
filename = file + '.avi'
# print(filename)
fourcc = cv.VideoWriter_fourcc(*'XVID')
fps = 24

out = cv.VideoWriter(filename=filename, fourcc=fourcc, fps=fps, frameSize=dims)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv.imshow('frame', frame)

    # Detect face
    # Number of faces detected
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)

    frame2 = frame.copy()

    for (x, y, w, h) in faces:
        frame2 = cv.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv.imshow('frame', frame2)

    # Press r to start recording
    if cv.waitKey(1) == ord('r'):
        print("Record")
        start = time.time()
        flag = True

    if flag:
        # frame2 = frame.copy()
        if ((60-(time.time()-start) < 11)):
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)

        cv.putText(img=frame2, text=str(int(60-(time.time()-start))), org=(int(dims[0]-150), int(
            dims[1]-600)), fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=3, color=color, thickness=2)

        count = 1
        numFace = len(faces)
        for (x, y, w, h) in faces:
            frame2 = cv.rectangle(frame2, (x, y), (x+w, y+h), (0, 0, 255), 2)
            frame = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            print(numFace)
            if numFace == 2:
                if saveFace < 2:
                    name = file + "_" + str(saveFace) + ".png"
                    print(name)
                    crop = frame[y:y+h, x:x+w]
                    cv.imwrite(filename=name, img=crop)
                    saveFace += 1

        cv.imshow('frame', frame2)

        out.write(frame)
        if (time.time() - start >= 60):
            break

    if cv.waitKey(1) == ord('q'):
        print('Quit')
        break


# When everything done, release the capture
print("Task Completed")
cap.release()
out.release()
cv.destroyAllWindows()
