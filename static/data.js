let guesses = [];
let score = 0;
let timer = 60;
let highScore = 0;
let plays = 0;


//checks to see if duplicate guess has been made using checkGuess function
//if it has been used alerts user, if not passes guess to the API in postWord
function checkDup(guess) {
    let isDup = checkGuess(guess)
    if (isDup) {
        const msg = `${guess} has been previously submitted`
        handleResponse(msg);
    } else {
        postWord(guess)
    }
}

//checks guesses array to see if word has been used already, if not it addes it to the array 
//returns True of False to isDup in checkDup function
function checkGuess(word) {
    word = word.toLowerCase();

    if (guesses.find(guess => guess === word)) { return true }
    else {
        guesses.push(word);
        return false;
    }
}

//posts word to server, retrieves a response, sends response message to handleResponse
async function postWord(guess) {
    try {
        const response = await axios.post('http://localhost:5000/submit', { guess: `${guess}` })

        if (response.status === 200) {
            const msg = response.data;
            console.log(response)
            updateList(guess, msg)
            handleResponse(msg);
            keepScore(msg, guess.length)

        }
        else {
            console.error('Error', response.status, response.statusText)
        }

    } catch (err) {
        console.error('An error occured:', err)
    }
}

function keepScore(msg, num) {
    if (msg === "ok") {
        score += num
    }
    updateScore(score)
    updateHighScore()
}

function countdown() {
    cd = setInterval(function () {
        timer--
        updateTime();
        handleTimer();
    }, 1000)
}

function reset() {
    guesses = [];
    score = 0;
    timer = 300;
}

function updateList(guess, msg) {
    let isfound = ''
    if (msg !== 'ok') {
        isfound = false
    } else { isfound = true }

    addGuess(guess, isfound);

}

function handleTimer() {
    if (timer === 0) {
        clearInterval(cd);
        endGame();
    }
}

async function getStats() {
    const response = await axios.get('http://localhost:5000/user-info')
    highScore = response.data.high_score
    plays = response.data.play_count
    updateStats()
}

function updateHighScore() {
    if (score > highScore) {
        highScore = score
        updateStats()
    }
}




