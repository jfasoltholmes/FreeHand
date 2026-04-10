import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import cv2
import math
import time, logging
import numpy as np

last_timestamp = 0

# Contains latest snapshot of detected hand landmarks.
callback_results = None

def callback(result, output_image, timestamp_ms):
    try:
        # Pruned incremental callback building due to partial writes asynchronously.
        # Prototype assumes 1 hand in frame.
        global callback_results
        if not result.hand_landmarks:
            callback_results = None
            return
        hand = result.hand_landmarks[0]

        # Replace entire hand snapshot.
        callback_results = np.array([[lm.x, lm.y, lm.z] for lm in hand], dtype=np.float32)

    except Exception as e:
        logging.error(f"Error in callback function: {e}")

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
    webcam = cv2.VideoCapture(0)
    while True:
        _, frame = webcam.read()
        
        image_height, image_width, _ = frame.shape

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Ensure timestamps sent to detect_async are strictly increasing.
        timestamp = time.time()
        if timestamp <= last_timestamp:
            continue
        landmarker.detect_async(mp_image, mp.Timestamp.from_seconds(timestamp).value)
        last_timestamp = timestamp

        # Visualize landmarks and perform normalized distance calculations.
        if callback_results is not None:
            # imp_landmark structure:
            # idx 0:Wrist, 1:thumb tip, 2:index tip, 3:middle mcp, 4:middle tip, 5:ring tip, 6:pinky tip
            imp_landmarks = {0, 4, 8, 9, 12, 16, 20}
            coord_list = []

            # Display all 21 MediaPipe landmarks while storing important landmarks.
            for idx, fingertip_set in enumerate(callback_results):
                xloc, yloc = int(fingertip_set[0] * image_width), int(fingertip_set[1] * image_height)
                if idx in imp_landmarks:
                    # Store normalized float coordinates, while visualization uses integer pixel coordinates.
                    coord_list.append((fingertip_set[0], fingertip_set[1]))
                frame = cv2.circle(frame, (xloc, yloc), 5, (0, 0, 255), -1)
            
            # Normalize all finger distances by wrist to middle MCP distance (Relatively stable hand-size reference).
            hand_scale = math.dist(coord_list[0], coord_list[3])
            
            # idx refers to coord_list idx in this loop, not mediapipe landmark idx.
            for idx, coord_tuple in enumerate(coord_list):
                if idx == 0 or idx == 3:
                    continue
                
                if idx == 1:
                    # Thumb edge case: Calculate normalized distance from middle MCP to thumb tip.
                    normalized_distance = math.dist(coord_list[3], coord_tuple) / hand_scale
                else:
                    # Calculate normalized distance from wrist to each finger tip.
                    normalized_distance = math.dist(coord_list[0], coord_tuple) / hand_scale
                
                print(f"idx: {idx}, normalizedDist: {normalized_distance}")

        # Flip the frame (for aesthetics) and display.
        cv2.imshow('Hand Tracking', cv2.flip(frame, 1))
        if cv2.waitKey(1) == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()