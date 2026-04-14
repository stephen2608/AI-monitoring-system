from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
from deepface import DeepFace
import time

app = Flask(__name__)

# Global variables for camera control
global_cap = None
is_monitoring = False

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    global global_cap, is_monitoring
    while True:
        # Camera OFF-ah irundha blank frame (Offline screen)
        if not is_monitoring or global_cap is None:
            blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(blank_frame, "OFFLINE", (250, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', blank_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)
            continue

        success, frame = global_cap.read()
        if not success:
            continue

        h, w, _ = frame.shape
        green = (0, 255, 0)
        orange = (0, 165, 255)
        red = (0, 0, 255)
        
        # HUD Bar
        cv2.rectangle(frame, (0, 0), (w, 60), (30, 30, 30), -1)
        cv2.putText(frame, " AI - MONITOR ACTIVE", (20, 35), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

        try:
            results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if results and results[0]['face_confidence'] > 0.4:
                res = results[0]
                region = res['region']
                rx, ry, rw, rh = region['x'], region['y'], region['w'], region['h']
                
                # Attention Logic for Visual Box
                face_center = rx + (rw // 2)
                offset = face_center - (w // 2)
                
                # Color changing logic
                box_color = green if abs(offset) <= 100 else orange
                
                cv2.rectangle(frame, (rx, ry), (rx+rw, ry+rh), box_color, 2)
                cv2.putText(frame, "SUBJECT DETECTED", (rx, ry-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 1)
            else:
                cv2.rectangle(frame, (0, 0), (w, h), red, 4)
        except:
            pass
       

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control_camera')
def control_camera():
    global global_cap, is_monitoring
    action = request.args.get('action')
    if action == 'on':
        if global_cap is None:
            global_cap = cv2.VideoCapture(0)
        is_monitoring = True
        return jsonify({"status": "on"})
    else:
        is_monitoring = False
        if global_cap:
            global_cap.release()
            global_cap = None
        return jsonify({"status": "off"})

@app.route('/get_data')
def get_data():
    global global_cap, is_monitoring
    if not is_monitoring or global_cap is None:
        return jsonify({"status": "Searching...", "attention": "MISSING"})

    ret, frame = global_cap.read()
    if not ret: return jsonify({"status": "error"})
    
    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        if results and results[0]['face_confidence'] > 0.4:
            res = results[0]
            # --- UNGA DATA LOGIC ---
            h, w, _ = frame.shape
            face_center = res['region']['x'] + (res['region']['w'] // 2)
            offset = face_center - (w // 2)
            
            attn = "100%"
            if offset < -100: attn = "LEFT"
            elif offset > 100: attn = "RIGHT"

            roi = frame[res['region']['y']:res['region']['y']+res['region']['h'], 
                        res['region']['x']:res['region']['x']+res['region']['w']]
            bpm = int(65 + (np.mean(roi[:,:,1]) % 15))

            return jsonify({
                "emotion": res['dominant_emotion'].upper(),
                "bpm": bpm,
                "attention": attn,
                "status": "Face Detected"
            })
    except:
        pass
    return jsonify({"status": "Searching...", "attention": "MISSING"})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)