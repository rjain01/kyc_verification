import numpy as np
import cv2 as cv
import time


# q : quit the camera
# r : record
# s : stop record
flag = False

cap = cv.VideoCapture(0)

dims = (1280, 720)

# Resize cap
cap.set(3, dims[0])  # width
cap.set(4, dims[1])  # height

filename = 'riya.avi'

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

    # Press r to start recording
    if cv.waitKey(1) == ord('r'):
        print("Record")
        start = time.time()
        flag = True

    if flag:
        frame2 = frame.copy()
        if ((60-(time.time()-start) < 11)):
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)

        cv.putText(img=frame2, text=str(int(60-(time.time()-start))), org=(int(dims[0]-150), int(
            dims[1]-600)), fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=3, color=color, thickness=2)
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


# https://www.geeksforgeeks.org/uploading-files-on-google-drive-using-python/
