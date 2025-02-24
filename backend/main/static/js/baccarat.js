
document.querySelectorAll(".baccarat-bet-button").forEach(button => {
    button.addEventListener('click', function () {
        const betAmount = parseFloat(document.getElementById('bet').value);
        const selectedBet = this.id;
        const gold = parseFloat(document.getElementById('gold-display').textContent);

        if (!betAmount || isNaN(betAmount) || betAmount <= 0) {
            alert("Lütfen geçerli bir bahis miktarı girin.");
            return;
        }

        if (betAmount > gold) {
            alert("Gecersiz Bakiye.");
            return;
        }

        resetGame();  // Önceki oyunu temizle
        startGame(selectedBet, betAmount);
    });
});

function resetGame() {
    document.getElementById('player-cards').innerHTML = '';
    document.getElementById('banker-cards').innerHTML = '';
    document.getElementById('game-result').innerText = '';
    document.getElementById('result-section').style.display = 'none';
}

function startGame(selectedBet, betAmount) {
    const cardValues = {
        'Ace_of_Hearts': 1, 'King_of_Hearts': 10, 'Queen_of_Hearts': 10, 'Jack_of_Hearts': 10,
        'Ten_of_Hearts': 10, 'Nine_of_Hearts': 9, 'Eight_of_Hearts': 8, 'Seven_of_Hearts': 7,
        'Six_of_Hearts': 6, 'Five_of_Hearts': 5, 'Four_of_Hearts': 4, 'Three_of_Hearts': 3, 'Two_of_Hearts': 2
    };

    const keys = Object.keys(cardValues);
    let playerCards = [];
    let bankerCards = [];
    let playerScore = 0;
    let bankerScore = 0;
    let finalAmount = 0;

    function drawCardWithDelay(handArray, cardContainer, delay) {
        setTimeout(() => {
            const randomCard = keys[Math.floor(Math.random() * keys.length)];
            const cardValue = cardValues[randomCard];
            handArray.push(cardValue);

            // Kartı görsel olarak göster
            const cardElement = document.createElement('img');
            cardElement.src = `/static/images/cards/${randomCard}.png`;
            cardElement.className = 'baccarat-card';
            cardContainer.appendChild(cardElement);
        }, delay);
    }

    drawCardWithDelay(playerCards, document.getElementById('player-cards'), 0);
    drawCardWithDelay(playerCards, document.getElementById('player-cards'), 1000);
    drawCardWithDelay(bankerCards, document.getElementById('banker-cards'), 2000);
    drawCardWithDelay(bankerCards, document.getElementById('banker-cards'), 3000);

    // Skoru hesapla ve sonucu belirle
    setTimeout(() => {
        playerScore = playerCards.reduce((acc, val) => acc + val, 0) % 10;
        bankerScore = bankerCards.reduce((acc, val) => acc + val, 0) % 10;

        let resultMessage;
        if (playerScore > bankerScore) {
            if (selectedBet === 'player-bet') {
                finalAmount += betAmount;
                resultMessage = `Kazandin  ${finalAmount}`;
            } else {
                finalAmount -= betAmount;
                resultMessage = "Kaybettin ";
            }
        } else if (bankerScore > playerScore) {
            if (selectedBet === 'banker-bet') {
                finalAmount += betAmount ;
                resultMessage = `Kazandin  ${finalAmount}`;
            } else {
                finalAmount -= betAmount;
                resultMessage = "Kaybettin";
            }
        } else {
            if (selectedBet === 'tie-bet') {
                finalAmount = betAmount * 7;
                resultMessage = `Berabere ! Kazanc: ${finalAmount}`;
            } else {
                finalAmount -= betAmount;
                resultMessage = "Berabere! ";
            }
        }

        console.log("Final amount (kazanç/kayıp):", finalAmount);
        document.getElementById('game-result').innerText = resultMessage;
        document.getElementById('result-section').style.display = 'block';

        // Sonucu backend'e gönder
        sendResultToBackend(betAmount, selectedBet, finalAmount);
    }, 4000);  // 4 saniye sonra sonucu hesapla
}

function sendResultToBackend(betAmount, selectedBet, finalAmount) {
    const data = new FormData();
    data.append('bet_amount', betAmount);
    data.append('bet_on', selectedBet);
    data.append('final_amount', finalAmount);

    console.log("Gönderilen final amount (POST isteği):", finalAmount);

    fetch('/baccarat/', {
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Sunucudan gelen mesaj:", data.message);
    })
    .catch(error => {
        console.error('Hata:', error);
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
