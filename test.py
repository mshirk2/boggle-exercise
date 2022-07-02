from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """check to make sure the homepage loads with the data correctly"""

        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)
            print(html)
            self.assertIn("Score: 0", html)
            self.assertIn("Times Played: 0", html)
            self.assertIn("High Score: 0", html)
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("numplays"))


    def test_valid_word(self):
        """Test if a word is valid compared to a board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ["R", "A", "O", "P", "T"],
                    ["W", "B", "K", "M", "L"],
                    ["X", "T", "S", "P", "T"],
                    ["R", "A", "I", "F", "A"],
                    ["E", "H", "O", "P", "N"]]
        
        response = self.client.get('/submit?word=hat')
        self.assertEqual(response.json['result'], 'ok')

    
    def test_not_word(self):
        """Test if word is not English"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ["R", "A", "O", "P", "T"],
                    ["W", "B", "K", "M", "L"],
                    ["X", "T", "S", "P", "T"],
                    ["R", "A", "I", "F", "A"],
                    ["E", "H", "O", "P", "N"]]
        
        response = self.client.get('/submit?word=raop')
        self.assertEqual(response.json['result'], 'not-word')

    def test_not_on_board(self):
        """Test if word is not on the board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ["R", "A", "O", "P", "T"],
                    ["W", "B", "K", "M", "L"],
                    ["X", "T", "S", "P", "T"],
                    ["R", "A", "I", "F", "A"],
                    ["E", "H", "O", "P", "N"]]
        
        response = self.client.get('/submit?word=breakfast')
        self.assertEqual(response.json['result'], 'not-on-board')



