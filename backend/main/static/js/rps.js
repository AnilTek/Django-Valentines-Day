document.querySelectorAll(".rps-bet-button").forEach(button => {
    button.addEventListener("click", function (event) {
        const betAmount = parseFloat(document.getElementById("bet").value);
        const selectedBet = event.target.value;
        const gold = parseFloat(document.getElementById("gold-display")?.textContent || 100);

        if (!betAmount || isNaN(betAmount) || betAmount <= 0) {
            alert("Lütfen geçerli bir bahis miktarı girin.");
            return;
        }

        if (betAmount > gold) {
            alert("Geçersiz Bakiye.");
            return;
        }

        resetGame();
        startGame(selectedBet, betAmount);
    });
});

// 🎨 Image paths
const images = {
    rock: "/static/images/rock.png",
    paper: "/static/images/paper.png",
    scissors: "/static/images/scissors.png",
};


function getBotChoice() {
    const choices = Object.keys(images);
    return choices[Math.floor(Math.random() * choices.length)];
}

function startGame(selectedBet, betAmount) {
    const bots_choice = getBotChoice();
    const playerChoiceImg = document.getElementById("player-choice");
    const botChoiceImg = document.getElementById("bot-choice");

    const choices = Object.values(images);
    let index = 0;

    // 🎞️ Animation Effect (Looping Choices)
    const animationInterval = setInterval(() => {
        playerChoiceImg.innerHTML = `<img src="${choices[index]}" class="rps-img">`;
        botChoiceImg.innerHTML = `<img src="${choices[index]}" class="rps-img">`;
        index = (index + 1) % choices.length;
    }, 300);

    // 🛑 Stop Animation and Show Final Selection After 3s
    setTimeout(() => {
        clearInterval(animationInterval);
        playerChoiceImg.innerHTML = `<img src="${images[selectedBet]}" class="rps-img">`;
        botChoiceImg.innerHTML = `<img src="${images[bots_choice]}" class="rps-img">`;

        let finalAmount = determineWinner(selectedBet, bots_choice, betAmount);
        
        // ✅ Send Result to Backend After the Game Finishes
        sendResultToBackend(betAmount, finalAmount);
    }, 3000);
}

function determineWinner(userChoice, botChoice, betAmount) {
    let resultText = "";
    let finalAmount = -betAmount;  // Default: User loses bet

    if (userChoice === botChoice) {
        resultText = "🤝 Berabere!";
        finalAmount = 0;
    } else if (
        (userChoice === "rock" && botChoice === "scissors") ||
        (userChoice === "paper" && botChoice === "rock") ||
        (userChoice === "scissors" && botChoice === "paper")
    ) {
        resultText = "🏆 Tebrikler! Kazandınız!";
        finalAmount = +betAmount ;  // User wins double the bet
    } else {
        resultText = "❌ Kaybettiniz!";
    }

    document.getElementById("result-section").style.display = "block";
    document.getElementById("game-result").textContent = resultText;

    return finalAmount;
}

function resetGame() {
    document.getElementById("result-section").style.display = "none";
    document.getElementById("game-result").textContent = "";
}





function sendResultToBackend(betAmount, finalAmount) {
    const data = new FormData();
    data.append('bet_amount', betAmount);
    data.append('final_amount', finalAmount);

    console.log("📤 Sending Result to Backend: Bet =", betAmount, "| Final Amount =", finalAmount);

    fetch('/slot/', {  // ✅ Send to slot endpoint
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("✅ Server Response:", data.message);
        goldDisplay.textContent = data.new_gold; // ✅ Update gold balance in UI
    })
    .catch(error => {
        console.error('❌ Error:', error);
    });
}


function getCSRFToken() {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length);
        }
    }
    return '';
}
