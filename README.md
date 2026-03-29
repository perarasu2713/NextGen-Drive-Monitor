# 🚗✨ NextGen Drive Monitor

### 🧠 Intelligent Driver Drowsiness Detection System

<p align="center">
  <img src="https://img.shields.io/badge/AI-Driven-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Computer%20Vision-OpenCV-green?style=for-the-badge&logo=opencv">
  <img src="https://img.shields.io/badge/Frontend-JavaScript-yellow?style=for-the-badge&logo=javascript">
  <img src="https://img.shields.io/badge/Backend-Flask-red?style=for-the-badge&logo=flask">
</p>

---

## 🌟 Overview

**NextGen Drive Monitor** is a real-time AI-powered driver monitoring system designed to detect fatigue and prevent accidents caused by drowsiness.

Using advanced **Computer Vision** techniques, the system continuously analyzes facial landmarks to detect:

* 👁️ Eye closure (blink detection)
* 😮 Yawning behavior
* 🚨 Signs of drowsiness

It provides **instant alerts**, a **live dashboard**, and **data visualization** for enhanced driver safety.

---

## ⚡ Key Features

### 🧠 Real-Time AI Monitoring

* Face detection using MediaPipe
* Eye Aspect Ratio (EAR) tracking
* Mouth Aspect Ratio (MAR) analysis

### 🚨 Smart Alert System

* Audio alarm when drowsiness is detected
* Automatic start/stop logic
* Toggle sound control

### 📊 Live Dashboard

* Real-time blink & yawn count
* Dynamic status indicator (AWAKE / DROWSY)
* Animated UI with modern design

### 📈 Data Visualization

* Graph of EAR vs Time
* Threshold-based highlighting
* Insight into driver behavior

### 🔐 Authentication System

* Login & session management
* Secure access to dashboard

---

## 🧩 System Architecture

```text
Camera → OpenCV → MediaPipe → Feature Extraction (EAR/MAR)
        ↓
   Drowsiness Detection Logic
        ↓
 Flask Backend (API + Streaming)
        ↓
Frontend Dashboard (HTML + JS + Chart.js)
```

---

## 🛠️ Tech Stack

| Layer         | Technology Used       |
| ------------- | --------------------- |
| 👨‍💻 Backend | Python, Flask         |
| 👁️ Vision    | OpenCV, MediaPipe     |
| 📊 Data       | CSV Logging           |
| 🎨 Frontend   | HTML, CSS, JavaScript |
| 📈 Charts     | Chart.js              |
| 🔊 Audio      | Pygame                |

---

## 📂 Project Structure

```text
📦 NextGen-Drive-Monitor
 ┣ 📂 static
 ┃ ┣ script.js
 ┃ ┗ style.css
 ┣ 📂 templates
 ┃ ┣ index.html
 ┃ ┗ login.html
 ┣ app.py
 ┣ drowsiness_detector.py
 ┣ requirements.txt
 ┗ README.md
```

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/NextGen-Drive-Monitor.git
cd NextGen-Drive-Monitor
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python app.py
```

### 4️⃣ Open in Browser

```text
http://127.0.0.1:5000
```

---

## 📸 Screenshots (Add your images 🔥)

```md
![Dashboard](screenshots/dashboard.png)
![Graph](screenshots/graph.png)
![Login](screenshots/login.png)
```

---

## 🧠 How It Works

### 👁️ Eye Aspect Ratio (EAR)

* Measures eye openness
* Detects blink patterns
* Low EAR → eye closed

### 😮 Mouth Aspect Ratio (MAR)

* Detects yawning
* High MAR → mouth open

### 🚨 Drowsiness Logic

* Continuous low EAR → fatigue detected
* Triggers alert system

---

## ⚠️ Limitations

* Requires good lighting conditions
* Works best with single face detection
* Camera-based detection works locally

---

## 🔮 Future Enhancements

* 📱 Mobile app integration
* 🌐 WebRTC camera support (browser-based)
* 🤖 Deep learning model (CNN/LSTM)
* ☁️ Cloud deployment
* 🚗 Integration with vehicle systems

---

## 👨‍💻 Author

**Perarasu**
🎓 Engineering Student

---

## 💡 Inspiration

Road accidents due to driver fatigue are a major issue.
This project aims to leverage AI to improve **road safety** and **save lives**.

---

## ⭐ Show Your Support

If you like this project:

* ⭐ Star this repo
* 🍴 Fork it
* 🧠 Share ideas

---

## 🏁 Final Note

> “Technology should not just be smart — it should be life-saving.”

---

✨ Built with passion, curiosity, and a vision for safer roads.
