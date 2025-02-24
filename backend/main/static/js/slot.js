document.addEventListener("DOMContentLoaded", () => {
    const images = {
        banana: "/static/images/banana_icon.png",
        grape: "/static/images/grape_icon.png",
        cat: "/static/images/cat_icon.png",
        default: "/static/images/question_mark.png" // Placeholder before spin
    };

    const spinButton = document.getElementById("spin-button");
    const reels = [
        document.getElementById("reel1"),
        document.getElementById("reel2"),
        document.getElementById("reel3")
    ];
    const slotResult = document.getElementById("slot-result");
    const betInput = document.getElementById("bet-amount");
    const goldDisplay = document.getElementById("gold-display"); // Display for current gold

    // ✅ Set Default Images on Load
    reels.forEach(reel => {
        reel.innerHTML = `<img src="${images.default}" class="slot-img">`;
    });

    if (!spinButton) {
        console.error("❌ Spin button not found in the DOM!");
        return;
    }

    spinButton.addEventListener("click", () => {
        console.log("✅ Spin button clicked!");
        startSlot();
    });

    function getRandomImage() {
        const keys = Object.keys(images).filter(key => key !== "default");
        return images[keys[Math.floor(Math.random() * keys.length)]];
    }

    function startSlot() {
        const betAmount = parseFloat(betInput.value);
        let currentGold = parseFloat(goldDisplay.textContent);

        // ✅ Validate Bet Amount
        if (!betAmount || isNaN(betAmount) || betAmount <= 0) {
            alert("Lütfen geçerli bir bahis miktarı girin.");
            return;
        }

        if (betAmount > currentGold) {
            alert("Yetersiz bakiye!");
            return;
        }

        slotResult.textContent = ""; 
        let spinDuration = 3000; 
        let intervalTime = 150; 

        let intervals = reels.map((reel, index) => {
            return setInterval(() => {
                reel.innerHTML = `<img src="${getRandomImage()}" class="slot-img">`;
            }, intervalTime + index * 50);
        });

       
        setTimeout(() => {
            intervals.forEach(clearInterval);
            let finalImages = reels.map(reel => reel.querySelector("img").src);

            let prize = checkWin(finalImages, betAmount);
            sendResultToBackend(betAmount, prize); 
        }, spinDuration);
    }

    function checkWin(finalImages, betAmount) {
        let finalAmount = -betAmount;

        if (finalImages[0] === finalImages[1] && finalImages[1] === finalImages[2]) {
            finalAmount = betAmount * 10; 
            slotResult.textContent = `🎉 JACKPOT! You won ${finalAmount} gold!`;
            slotResult.style.color = "green";
        } else {
            slotResult.textContent = `❌ Try again! You lost ${betAmount} gold.`;
            slotResult.style.color = "black";
        }

        return finalAmount;
    }

    function sendResultToBackend(betAmount, finalAmount) {
        const data = new FormData();
        data.append('bet_amount', betAmount);
        data.append('final_amount', finalAmount);

        console.log("📤 Sending Result to Backend: Bet =", betAmount, "| Final Amount =", finalAmount);

        fetch('/slot/', {  
            method: 'POST',
            body: data,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ Server Response:", data.message);
            goldDisplay.textContent = data.new_gold; 
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
});
