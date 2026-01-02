import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import cv2
import time, logging
import numpy as np

last_timestamp = 0
callback_results = None

def callback(result, output_image, timestamp_ms):
    try:
        """
        # This may be causing issues because instead of creating callback_results in one snapshot it is writing incrementally from the for loop.
        # This causes issues because the callback is running asynchronously which results in the main webcam loop reading partial writes in the callback_results
        for hand_idx, hand_landmarks in enumerate(result.hand_landmarks):
            # Add hands to callback snapshot
            if hand_idx not in callback_results:
                callback_results[hand_idx] = {}

            for landmark_idx, landmark in enumerate(hand_landmarks):
                # Add each hands 
                callback_results[hand_idx][landmark_idx] = {
                    "landmark_x": landmark.x,
                    "landmark_y": landmark.y,
                    "landmark_z": landmark.z
                } 
        """
        # Assumes 1 hand, use a for loop in place of hand assignment if num_hands=2
        global callback_results
        if not result.hand_landmarks:
            callback_results = None
            return
        hand = result.hand_landmarks[0]
        callback_results = np.array([[lm.x, lm.y, lm.z] for lm in hand], dtype=np.float32)

    except Exception as e:
        logging.error(f"Error in callback function: {e}")

# Creating HandLandmarker object for webcam livestream type
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
running_mode = vision.RunningMode('LIVE_STREAM')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                        running_mode=running_mode,
                                        num_hands=1,
                                        min_hand_detection_confidence=0.5,
                                        min_hand_presence_confidence=0.5,
                                        min_tracking_confidence=0.5,
                                        result_callback=callback)

with vision.HandLandmarker.create_from_options(options) as landmarker:
    # Run webcam video capture
    webcam = cv2.VideoCapture(0)
    while True:
        start_time = time.time()

        _, frame = webcam.read()
        
        image_height, image_width, _ = frame.shape

        # Convert each frame to mediapipe image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        timestamp = time.time()
        if timestamp <= last_timestamp:
            continue

        # Detect landmarks in frame through callback function
        testVariable = landmarker.detect_async(mp_image, mp.Timestamp.from_seconds(timestamp).value)
        last_timestamp = timestamp

        # Similar to callback, loop through each hand and then 
        #print(callback_results)
        # Loop through each hand.
          # For each hand, loop through and plot each all 21 hand landmarks

        """
        # Possibly use output image versus using frame to get x, y center pixel points. may improve accuracy if bad
        for hand_idx, hand in callback_results.items():
            #print(f"Key: {key},  Value: {value}\n")
            for landmark_set_idx, landmark_set in hand.items():
                #print(f"Key: {landmark_set_idx},  Value: {landmark_set}\n")
                #print(f"Value for X: {landmark_set['landmark_x']}\nValue for Y: {landmark_set['landmark_y']}\n")
                xloc, yloc = int(landmark_set['landmark_x'] * image_width), int(landmark_set['landmark_y'] * image_height)
                frame = cv2.circle(frame, (xloc, yloc), 5, (0, 0, 255), -1)
        """
        if callback_results is not None:
            for landmark_set_idx, landmark_set in enumerate(callback_results):
                print(f"Index: {landmark_set_idx}, Set: {landmark_set}")
                xloc, yloc = int(landmark_set[0] * image_width), int(landmark_set[1] * image_height)
                frame = cv2.circle(frame, (xloc, yloc), 5, (0, 0, 255), -1)
            # Check the differences between index 4, 8, 12, 16, and 20 from index 0(wrist)
            # For loop with step 4
            # For _, fingertip_set in enumerate(callback_results[0:20:4])

        # Flip the frame (for aesthetics) and show the frame
        cv2.imshow('Hand Tracking', cv2.flip(frame, 1))
        if cv2.waitKey(1) == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()