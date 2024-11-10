import cv2
import numpy as np
import tensorflow as tf
from picamera2 import Picamera2

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="detect.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']

# Load COCO labels
with open("coco_labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Initialize Pi Camera Module 3
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

while True:
    # Capture frame from Pi Camera
    frame = picam2.capture_array()

    # Preprocess the frame for the model
    img = cv2.resize(frame, (input_shape[2], input_shape[1]))
    img = np.expand_dims(img, axis=0).astype(np.uint8)

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], img)

    # Run inference
    interpreter.invoke()

    # Extract detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]

    # Screen center for side detection
    screen_center_x = frame.shape[1] // 2

    # Loop through detections and draw bounding boxes for ducks
    for i in range(len(scores)):
        if scores[i] > 0.5 and labels[int(classes[i])] == "duck":
            ymin, xmin, ymax, xmax = boxes[i]
            (left, top) = (int(xmin * frame.shape[1]), int(ymin * frame.shape[0]))
            (right, bottom) = (int(xmax * frame.shape[1]), int(ymax * frame.shape[0]))
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Duck", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Check if the bounding box is on the left side of the screen
            if left < screen_center_x:
                # Left side logic goes here
                pass

            # Check if the bounding box is on the right side of the screen
            if right >= screen_center_x:
                # Right side logic goes here
                pass

    # Display the resulting frame
    cv2.imshow("Duck Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
picam2.close()
