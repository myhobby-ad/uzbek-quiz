const tg = window.Telegram.WebApp;
tg.expand();

let currentLevelQuestions = [];
let currentIndex = 0;
let score = 0;
let selectedLevelName = "";

function startQuiz(level) {
    selectedLevelName = level;
    currentLevelQuestions = allQuestions[level];
    
    if (!currentLevelQuestions) {
        alert("Savollar yuklanmadi!");
        return;
    }

    document.getElementById("menu").classList.add("hidden");
    document.getElementById("quiz").classList.remove("hidden");
    
    currentIndex = 0;
    score = 0;
    loadQuestion();
}

function loadQuestion() {
    const q = currentLevelQuestions[currentIndex];
    document.getElementById("question-num").innerText = `DARAJA: ${selectedLevelName} | SAVOL: ${currentIndex + 1}/${currentLevelQuestions.length}`;
    document.getElementById("question-text").innerText = q.question;
    
    const container = document.getElementById("options-container");
    container.innerHTML = "";

    q.options.forEach((opt, index) => {
        const btn = document.createElement("button");
        btn.className = "btn";
        btn.innerText = opt;
        btn.onclick = () => checkAnswer(index, btn);
        container.appendChild(btn);
    });
}

function checkAnswer(index, btn) {
    const correct = currentLevelQuestions[currentIndex].correct;
    const buttons = document.querySelectorAll("#options-container .btn");
    
    buttons.forEach(b => b.disabled = true);

    if (index === correct) {
        score++;
        btn.style.backgroundColor = "#00ff88";
        btn.style.color = "#0a0e14";
    } else {
        btn.style.backgroundColor = "#ff4444";
        btn.style.color = "white";
        buttons[correct].style.border = "2px solid #00ff88";
    }

    setTimeout(() => {
        currentIndex++;
        if (currentIndex < currentLevelQuestions.length) {
            loadQuestion();
        } else {
            showFinalResult();
        }
    }, 1000);
}

function showFinalResult() {
    const container = document.getElementById("main-container");
    const percent = Math.round((score / currentLevelQuestions.length) * 100);
    
    container.innerHTML = `
        <h2 style="color: #00ff88">Test Yakunlandi!</h2>
        <p style="font-size: 1.2rem">Daraja: <b>${selectedLevelName}</b></p>
        <p style="font-size: 1.5rem">Natija: ${score} / ${currentLevelQuestions.length}</p>
        <p style="margin-bottom: 20px;">Ko'rsatkich: ${percent}%</p>
        <button class="btn" onclick="location.reload()">Bosh menyuga qaytish</button>
        <button class="btn" style="background: #00ff88; color: #0a0e14" onclick="sendResult()">Botga yuborish</button>
    `;
}

function sendResult() {
    const resultData = {
        level: selectedLevelName,
        score: score,
        total: currentLevelQuestions.length
    };
    tg.sendData(JSON.stringify(resultData));
    tg.close();
}