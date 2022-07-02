from flask import Flask, render_template, request, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def homepage():
    """Make the board, add it to the session and render it in the DOM"""

    board = boggle_game.make_board()
    session['board'] = board

    # get the high score from the session and render in the DOM, default to 0
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    return render_template('index.html', board=board, highscore=highscore, numplays=numplays)


@app.route('/submit')
def check_word():
    """Send guess to server, check if word is valid"""

    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route('/end-game', methods=['POST'])
def end_game():
    """get score from endGame post and update highscore in session"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)
    session["highscore"] = max(score, highscore)
    session["numplays"] = numplays + 1
    return "game over"

