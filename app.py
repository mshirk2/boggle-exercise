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
    """Show gameboard"""

    board = boggle_game.make_board()
    session['board'] = board

    return render_template('index.html', board=board)


@app.route('/submit')
def check_word():
    """Send guess to server, check if word is valid"""

    word = request.args.get("#guess")
    print("@app.route guess = ", word)
    board = session['board']
    status = boggle_game.check_valid_word(board, word)

    result = jsonify({'result': status})
    print("@app.route result = ", result)
    return result


