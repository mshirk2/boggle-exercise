from flask import Flask, render_template, redirect, request, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def homepage():
    """Shows game board"""

    board = boggle_game.make_board()
    session['board'] = board

    return render_template('index.html', board=board)


@app.route('/submit')
def check_guess():
    """Send guess to server, check if word is valid"""

    window.preventDefault()

    return redirect('/')


