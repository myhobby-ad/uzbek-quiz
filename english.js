// Telegram Web App ob'ektini olish
const tg = window.Telegram.WebApp;
tg.expand();

// 20 ta ingliz tili savoli
const questions = [
    { question: "I ___ a student.", options: ["am", "is", "are", "be"], correct: 0 },
    { question: "She ___ to school every day.", options: ["go", "goes", "going", "gone"], correct: 1 },
    { question: "Where ___ you live?", options: ["does", "do", "are", "is"], correct: 1 },
    { question: "Choose the correct plural: Child -> ___", options: ["childs", "children", "childrens", "childes"], correct: 1 },
    { question: "___ color is your car?", options: ["Who", "Which", "What", "How"], correct: 2 },
    { question: "Yesterday, I ___ a new movie.", options: ["see", "saw", "seen", "seeing"], correct: 1 },
    { question: "Have you ___ been to London?", options: ["never", "ever", "yet", "already"], correct: 1 },
    { question: "I am ___ than my brother.", options: ["tall", "taller", "tallest", "the tallest"], correct: 1 },
    { question: "We ___ watching TV when the phone rang.", options: ["was", "are", "were", "been"], correct: 2 },
    { question: "If it rains, I ___ stay at home.", options: ["would", "will", "am", "was"], correct: 1 },
    { question: "I've been working here ___ three years.", options: ["since", "for", "during", "while"], correct: 1 },
    { question: "The car ___ repaired tomorrow.", options: ["will be", "is", "was", "will"], correct: 0 },
    { question: "I don't mind ___ early.", options: ["get up", "to get up", "getting up", "got up"], correct: 2 },
    { question: "He asked me where ___.", options: ["did I live", "I lived", "do I live", "I live"], correct: 1 },
    { question: "You ___ smoke here. It's forbidden.", options: ["don't have to", "mustn't", "needn't", "shouldn't"], correct: 1 },
    { question: "I wish I ___ more money.", options: ["have", "had", "will have", "would have"], correct: 1 },
    { question: "By next year, I ___ my studies.", options: ["finish", "will finish", "will have finished", "finished"], correct: 2 },
    { question: "This is the house ___ my father built.", options: ["who", "whose", "which", "where"], correct: 2 },
    { question: "Although it was cold, ___ we went for a swim.", options: ["but", "so", "yet", "(no word)"], correct: 3 },
    { question: "I am looking forward to ___ you.", options: ["see", "seeing", "to see", "seen"], correct: 1 }
];

let currentQuestion = 0;
let score = 0;

function loadQuestion() {
    const q = questions[currentQuestion];
    
    // HTML elementlarni yangilash
    document.getElementById("question-num").innerText = `Savol ${currentQuestion + 1}/${questions.length}`;
    document.getElementById("question-text").innerText = q.question;
    
    const container = document.getElementById("options-container");
    container.innerHTML = ""; 

    q.options.forEach((opt, index) => {
        const btn = document.createElement("button");
        btn.className = "btn";
        btn.innerText = opt;
        btn.onclick = () => checkAnswer(index);
        container.appendChild(btn);
    });
}

function checkAnswer(index) {
    if (index === questions[currentQuestion].correct) {
        score++;
    }
    
    currentQuestion++;

    if (currentQuestion < questions.length) {
        loadQuestion();
    } else {
        finishQuiz();
    }
}

function finishQuiz() {
    const resultData = {
        score: score,
        total: questions.length
    };
    
    // Ma'lumotni botga yuborish
    tg.sendData(JSON.stringify(resultData));
    tg.close();
}

// O'yinni boshlash
loadQuestion();