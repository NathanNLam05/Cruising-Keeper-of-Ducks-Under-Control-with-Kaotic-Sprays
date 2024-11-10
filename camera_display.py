from picamera2 import Picamera2
import cv2

# Initialize the Pi Camera
picam2 = Picamera2()
picam2.configure(picam2.preview_configuration(main={"format": "RGB888", "size": (640, 480)}))

# Start the camera
picam2.start()

try:
    while True:
        # Capture the frame
        frame = picam2.capture_array()

        # Display the frame
        cv2.imshow("Pi Camera Module 3 Wide Display", frame)

        # Exit the display window when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Cleanup: Stop the camera and close the display window
    picam2.stop()
    cv2.destroyAllWindows()
