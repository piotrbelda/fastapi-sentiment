const sentiments = document.querySelectorAll("#sentiment-wrapper");

const sentimentsCopy = [...sentiments];

document.getElementById("hideNegative").addEventListener('change', (e) => {
    checked = document.getElementById("hideNegative").checked;
    if (checked) {
        document.getElementById('sentiments').innerHTML = "";
    }
    else {
        sentimentsCopy.forEach(sentiment => {
            document.getElementById('sentiments').appendChild(sentiment);
        })
    }
})