const $score = $('#score');
const $time = $('#time');
const $start = $('#start');
const $guesses = $('#guesses');
const $form = $('#form');
const $list = $('#word-list');
const $msg = $('#msg');
const $submit = $('#word-submit');
const $textbox = $('#word');
const $restart = $('#restart');
const $subHeader = $("#form-head")
const $formLabel = $('#form-label')
const $table = $('#game-table')
const $userBoard = $('#user-info')
const $highScore = $('#high-score')
const $plays = $('#plays')


function start() {
    reset()
    setDom()
    countdown()
    getStats()
}


$start.on('click', start)
//when word is submitted prevents default then checks for duplicate guesses in data.js
function wordCheck(e) {
    e.preventDefault();
    const guess = $textbox.val();
    checkDup(guess)
    $('td').removeClass('clicked');
    $textbox.val("");
}

$submit.on('click', wordCheck)

function handleResponse(msg) {
    $msg.text(msg)
    //improve how the dom shows the message
}

function updateScore(score) {
    $score.text(`${score}`)
}

function updateTime() {

    $time.text(`${timer}`)
}

function setDom() {
    $start.addClass('hide')
    $table.removeClass('hide')
    $guesses.removeClass('hide')
    $form.removeClass('hide')
    $userBoard.removeClass('hide').addClass('flex')
}

function addGuess(guess, isfound) {
    let li = ''
    if (isfound) {
        li = $(`<li class="found">${guess}</li>`)
    } else {
        li = $(`<li class="not-found">${guess}</li>}`)
    }
    $list.append(li);
}

function endGame() {
    $submit.addClass('hide');
    $textbox.addClass('hide');
    $subHeader.addClass('hide');
    $formLabel.addClass('hide')
    $msg.text('Game Over')
    $restart.removeClass('hide');
    redirect()
}

$restart.on('click', function () { location.reload() })

$('td').on('click', addLetter)

function addLetter(evt) {
    evt.target.classList.add('clicked')
    letter = evt.target.textContent
    currentText = $textbox.val()
    newText = currentText + letter.toLowerCase()
    $textbox.val(newText);
}

function redirect() {
    const newUrl = "http://localhost:5000/"
    setTimeout(function () {
        window.location.replace(newUrl)
    }, 5000)
}

function updateStats() {
    $highScore.text(highScore)
    $plays.text(plays)
}



