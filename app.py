from flask import Flask, render_template, redirect, request, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def start_page():
    """Shows start page with button to begin"""

    return render_template('start.html')

@app.route('/game')
def game_page():
    """Shows game board"""

    return render_template('game.html')


@app.route('/submit')
def submit_guess():
    """Send guess to server, check if correct"""

    return redirect('/game')


