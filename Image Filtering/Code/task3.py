import cv2

def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(frame, 25, 75)
        cv2.imshow('Canny Edge LIVE', edge)
        if cv2.waitKey(20) == ord('q'):		# Introduce 20 millisecond delay. press q to exit.
            break

if __name__ == '__main__':
	main()