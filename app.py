from flask import Flask, render_template, Response, jsonify, request, session, redirect, url_for
import cv2
import csv
import drowsiness_detector
from drowsiness_detector import process_frame

app = Flask(__name__)
app.secret_key = "supersecretkey"  # 🔐 Required for login session


# 🔥 RESET VARIABLES
drowsiness_detector.TOTAL_BLINKS = 0
drowsiness_detector.TOTAL_YAWNS = 0
drowsiness_detector.COUNTER = 0


# ===================== 🔐 LOGIN SYSTEM =====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🔥 Simple demo login
        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid Login ❌"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ===================== 📊 STATS =====================

@app.route('/stats')
def stats():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"})

    status = "DROWSY" if drowsiness_detector.COUNTER >= 20 else "AWAKE"

    return jsonify({
        "blinks": drowsiness_detector.TOTAL_BLINKS,
        "yawns": drowsiness_detector.TOTAL_YAWNS,
        "status": status
    })


# ===================== 🔊 SOUND =====================

@app.route('/toggle_sound', methods=['POST'])
def toggle_sound():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"})

    drowsiness_detector.SOUND_ON = not drowsiness_detector.SOUND_ON

    # 🔥 Force stop immediately
    if not drowsiness_detector.SOUND_ON:
        drowsiness_detector.stop_alarm()

    return jsonify({"sound": drowsiness_detector.SOUND_ON})


# ===================== 📊 GRAPH =====================

@app.route('/graph_data')
def graph_data():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"})

    times = []
    ears = []

    try:
        with open("session_data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                times.append(float(row["Time"]))
                ears.append(float(row["EAR"]))
    except:
        return jsonify({"time": [], "ear": []})

    return jsonify({
        "time": times,
        "ear": ears
    })


# ===================== 🎥 CAMERA =====================

cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = process_frame(frame)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# ===================== 🌐 ROUTES =====================

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/video')
def video():
    if 'user' not in session:
        return "Unauthorized"

    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ===================== ▶️ RUN =====================

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)