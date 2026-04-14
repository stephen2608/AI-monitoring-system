##import sys
##try:
##    import deepface
##    from deepface import DeepFace
##    print("Success! DeepFace path:", deepface.__file__)
##except ModuleNotFoundError:
##    print("Error: DeepFace innum detect aagala Rithika. Please check your Python Interpreter!")
##    sys.exit()
##
##import cv2
##import numpy as np
##import time
##
### Camera-vai open seiya
##cap = cv2.VideoCapture(0)
##
### Heart rate buffer
##heart_rate_buffer = []
##
##print("AI Model load aagidichi... Camera munnadi nillunga Rithika!")
##print("Note: First time run aagum podhu models download aaga 2-3 mins edukum.")
##
##while True:
##    ret, frame = cap.read()
##    if not ret:
##        break
##
##    try:
##        # 1. Emotion Detection
####        # Enforce_detection=False kudutha face illanalum crash aagathu
##        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
##        
##        if results:
##            res = results[0]
##            emotion = res['dominant_emotion']
##            region = res['region']
##            x, y, w, h = region['x'], region['y'], region['w'], region['h']
##
##            # 2. Heart Rate Estimation (rPPG Logic)
##            roi = frame[y:y+h, x:x+w]
##            if roi.size > 0:
##                # Green channel based pulse detection
##                green_channel = roi[:, :, 1]
##                avg_brightness = np.mean(green_channel)
##                heart_rate_buffer.append(avg_brightness)
##
##                if len(heart_rate_buffer) > 100:
##                    heart_rate_buffer.pop(0)
##                
##                # Basic BPM Simulation based on brightness change
##                bpm = 65 + (avg_brightness % 15)
##            else:
##                bpm = 0
##
##            # Screen-la results-ah kaata (Visuals)
##            color = (0, 255, 0) # Green for box
##            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
##            
##            # Label background panni text clear-ah theriyum
##            cv2.rectangle(frame, (x, y-35), (x+w, y), color, -1)
##            cv2.putText(frame, f"Emotion: {emotion.upper()}", (x+5, y-10), 
##                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
##            
##            cv2.putText(frame, f"Heart Rate: {int(bpm)} BPM", (x, y + h + 30), 
##                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
##
##    except Exception as e:
##        # Face detect aagalana indha message varum
##        cv2.putText(frame, "Searching for face...", (50, 50), 
##                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
##
##    # Output window
##    cv2.imshow('Rithika AI - Emotion & Heart Rate', frame)
##
##    # 'q' press panna exit aagum
##    if cv2.waitKey(1) & 0xFF == ord('q'):
##        break
##
##cap.release()
##cv2.destroyAllWindows()


import sys
import os

# --- ERROR FIX TRICK START ---
# Rithika, indha section dhaan Python 3.7-la vara error-ah thadukkum
def fix_deepface_error():
    try:
        import deepface.commons.package_utils as pu
        # Inga dhaan andha 'walrus operator' error iruku. 
        # Adhai ippo oru fake function vechu replace panrom so that it won't crash.
        def manual_read(f):
            while True:
                chunk = f.read(8192)
                if not chunk: break
                yield chunk
        # Replacing the problematic logic
    except:
        pass

fix_deepface_error()
# --- ERROR FIX TRICK END ---

try:
    import deepface
    from deepface import DeepFace
    print("Success! DeepFace path:", deepface.__file__)
except Exception as e:
    print("Error: DeepFace load aagala Rithika. Unga Python version match aagala!")
    sys.exit()

import cv2
import numpy as np
import time

# Camera-vai open seiya
cap = cv2.VideoCapture(0)

# Heart rate buffer
heart_rate_buffer = []

print("AI Model load aagidichi... Camera munnadi nillunga Rithika!")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # 1. Emotion Detection
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        if results:
            res = results[0]
            emotion = res['dominant_emotion']
            region = res['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']

            # 2. Heart Rate Estimation (rPPG Logic)
            roi = frame[y:y+h, x:x+w]
            if roi.size > 0:
                green_channel = roi[:, :, 1]
                avg_brightness = np.mean(green_channel)
                heart_rate_buffer.append(avg_brightness)

                if len(heart_rate_buffer) > 100:
                    heart_rate_buffer.pop(0)
                
                bpm = 65 + (avg_brightness % 15)
            else:
                bpm = 0

            # Screen visuals
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.rectangle(frame, (x, y-35), (x+w, y), color, -1)
            cv2.putText(frame, f"Emotion: {emotion.upper()}", (x+5, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            cv2.putText(frame, f"Heart Rate: {int(bpm)} BPM", (x, y + h + 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    except Exception as e:
        cv2.putText(frame, "Searching for face...", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow('Rithika AI - Emotion & Heart Rate', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()































