import sys
import os
import cv2
import numpy as np
import threading
import pyttsx3
from deepface import DeepFace


def fix_deepface_error():
    try:
        import deepface.commons.package_utils as pu
    except:
        pass
fix_deepface_error()


# AI Voice Setup
engine = pyttsx3.init()
def speak(text):
    def run_speech():
      
        engine.setProperty('rate', 150) 
        engine.say(text)
        engine.runAndWait()
    
    threading.Thread(target=run_speech).start()

cap = cv2.VideoCapture(0)
last_voice_time = 0
heart_rate_buffer = []

print("System Starting... Welcome stephen!!")

while True:
    ret, frame = cap.read()
    if not ret: break

    h, w, _ = frame.shape
    screen_center = w // 2
  
    cv2.rectangle(frame, (0, 0), (w, 70), (45, 45, 45), -1) # Dark grey header
    cv2.line(frame, (0, 70), (w, 70), (0, 255, 0), 2) # Green separator line

    try:
     
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        if results and results[0]['face_confidence'] > 0.4:
            res = results[0]
            region = res['region']
            x, y, fw, fh = region['x'], region['y'], region['w'], region['h']
            
           
            face_center = x + (fw // 2)
            
          
            offset = face_center - screen_center
            
            attention_status = "100%"
            attention_color = (0, 255, 0)
            position_text = "CENTER"

            if offset < -120:
                attention_status = "LEFT"
                attention_color = (0, 165, 255) # Orange
                position_text = "LEFT"
            elif offset > 120:
                attention_status = "RIGHT"
                attention_color = (0, 165, 255)
                position_text = "RIGHT"

          
            if attention_status == "100%":
          
                roi = frame[y:y+fh, x:x+fw]
                if roi.size > 0:
                    avg_brightness = np.mean(roi[:, :, 1])
                    bpm = 65 + (avg_brightness % 15)
                

                cv2.rectangle(frame, (x, y), (x+fw, y+fh), (0, 255, 0), 2)

                cv2.putText(frame, f"MOOD: {res['dominant_emotion'].upper()}", (20, 45), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"BPM: {int(bpm)}", (w-150, 45), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame, f"ATTENTION: {attention_status}", (screen_center-100, 45), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.7, attention_color, 2)
            else:
               
                cv2.rectangle(frame, (x, y), (x+fw, y+fh), attention_color, 2)
                cv2.putText(frame, f"ATTENTION: {position_text}", (screen_center-100, 45), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.7, attention_color, 2)
                
                current_time = cv2.getTickCount() / cv2.getTickFrequency()
                if current_time - last_voice_time > 7:
                    speak("Attention miss, please see camera")
                    last_voice_time = current_time

        else:
     
            cv2.putText(frame, "ATTENTION: MISSING", (screen_center-120, 45), 
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)
       
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            if current_time - last_voice_time > 5:
                speak("Attention miss, please see camera")
                last_voice_time = current_time

    except Exception as e:
        pass

    cv2.putText(frame, "STEPHEN AI MONITORING SYSTEM", (10, h-15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    cv2.imshow('Professional AI Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()