// 🔁 AUTO UPDATE STATS
function updateStats() {
    fetch('/stats')
        .then(response => response.json())
        .then(data => {

            const statusText = document.getElementById("status");
            const ring = document.querySelector(".ring");

            document.getElementById("blinks").innerText = data.blinks;
            document.getElementById("yawns").innerText = data.yawns;
            statusText.innerText = data.status;

            if (data.status === "DROWSY") {
                statusText.style.color = "red";
                ring.style.background = "conic-gradient(red, red)";
                ring.style.boxShadow = "0 0 40px red";
            } else {
                statusText.style.color = "lime";
                ring.style.background = "conic-gradient(lime, lime)";
                ring.style.boxShadow = "0 0 40px lime";
            }

        });
}
setInterval(updateStats, 1000);


// 🌌 PARTICLE BACKGROUND
const canvas = document.getElementById("bgCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

for (let i = 0; i < 60; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 2,
        dx: Math.random() - 0.5,
        dy: Math.random() - 0.5
    });
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {
        p.x += p.dx;
        p.y += p.dy;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = "cyan";
        ctx.fill();
    });

    requestAnimationFrame(animateParticles);
}
animateParticles();


// 🔊 SOUND TOGGLE (🔥 FINAL PERFECT VERSION)
const soundBtn = document.getElementById("soundBtn");

// 🔥 Initial UI state (no glow by default)
soundBtn.innerText = "🔇 Sound OFF";
soundBtn.classList.remove("active");

// 🔊 Click toggle
soundBtn.onclick = () => {
    fetch('/toggle_sound', { method: 'POST' })
        .then(res => res.json())
        .then(data => {

            if (data.sound) {
                soundBtn.innerText = "🔊 Sound ON";
                soundBtn.classList.add("active");   // ✅ glow only ON
            } else {
                soundBtn.innerText = "🔇 Sound OFF";
                soundBtn.classList.remove("active"); // ❌ remove glow
            }

        });
};


// 📊 GRAPH SYSTEM
const graphBtn = document.getElementById("graphBtn");
const popup = document.getElementById("graphPopup");

function loadGraph() {
    fetch('/graph_data')
        .then(res => res.json())
        .then(data => {

            const ctx = document.getElementById('chart').getContext('2d');

            if (window.myChart) {
                window.myChart.destroy();
            }

            window.myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.time,
                    datasets: [{
                        label: 'EAR vs Time',
                        data: data.ear,
                        borderColor: 'cyan',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.3,

                        pointRadius: 3,
                        pointBackgroundColor: data.ear.map(v => v < 0.18 ? 'red' : 'cyan')
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: { display: true, text: 'Time' },
                            ticks: { maxTicksLimit: 8 }
                        },
                        y: {
                            title: { display: true, text: 'EAR' }
                        }
                    },
                    plugins: {
                        annotation: {
                            annotations: {
                                thresholdLine: {
                                    type: 'line',
                                    yMin: 0.18,
                                    yMax: 0.18,
                                    borderColor: 'red',
                                    borderWidth: 2,
                                    label: {
                                        content: 'Drowsy Threshold',
                                        enabled: true,
                                        position: 'end'
                                    }
                                }
                            }
                        }
                    }
                }
            });
        });
}


// 🔥 OPEN GRAPH
graphBtn.onclick = () => {
    popup.style.display = "block";

    loadGraph();

    window.graphInterval = setInterval(loadGraph, 2000);

    window.statusInterval = setInterval(() => {
        fetch('/stats')
            .then(res => res.json())
            .then(data => {
                popup.style.boxShadow =
                    data.status === "DROWSY"
                        ? "0 0 40px red"
                        : "0 0 40px cyan";
            });
    }, 1000);
};


// ❌ CLOSE POPUP
popup.addEventListener("click", (e) => {
    if (e.target === popup) {
        popup.style.display = "none";

        clearInterval(window.graphInterval);
        clearInterval(window.statusInterval);
    }
});


// ⛶ FULLSCREEN
const fullBtn = document.getElementById("fullBtn");

fullBtn.onclick = () => {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
};


// ⚡ LOADER REMOVE
window.addEventListener("load", () => {
    document.getElementById("loader").style.display = "none";
});