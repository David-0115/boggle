from flask import Flask, render_template, jsonify, request, session
from boggle import Boggle
from support import gen_key

app = Flask(__name__)

key = gen_key()
app.config["SECRET_KEY"] = key


boggle_game = Boggle()
high_score = 0
current_score = 0


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/boggle')
def boggle_start():
    """Generates the boggle gameboard, calls other functions to prep game data"""
    board = boggle_game.make_board()
    session["board"] = board
    get_high_score()
    update_play_count()
    return render_template('boggle.html', board=board)


@app.route('/submit', methods=["POST"])
def submit():
    """When a user submits a word it checks the word and returns a json response"""
    word = request.json["guess"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    update_score(response, word)
    return jsonify(response)


@app.route('/user-info')
def user_info():
    """Sends json response with high score and play count"""
    global current_score
    get_high_score()
    plays = session["play_count"]
    data = {"high_score": high_score, "play_count": plays}
    current_score = 0
    return jsonify(data)


def get_high_score():
    """Gets high score session data, sets high score variable"""
    high = session.get("high_score", None)

    if high is None:
        session["high_score"] = 0
        high_score = 0
    else:
        high_score = high


def update_play_count():
    """Gets play count session data, sets play count variable"""
    global play_count
    plays = session.get("play_count", None)

    if plays is None:
        session["play_count"] = 1
    else:
        count = int(session["play_count"])
        session["play_count"] = count + 1


def update_score(resp, word):
    """If word is found, updates the current score and calls update_high_score"""
    global current_score
    if resp == 'ok':
        current_score += len(word)
    update_high_score()


def update_high_score():
    """Checks current score versus high score - updates session high score if current score is greater"""
    if current_score > high_score:
        session["high_score"] = current_score
