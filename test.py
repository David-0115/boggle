from unittest import TestCase
from app import app, high_score, boggle_game
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    def test_home_page(self):
        with self.app as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h3 class="title title-link">Click to play!</h3>', html)

    def test_boggle_start(self):
        with self.app as client:
            resp = client.get('/boggle')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            with client.session_transaction() as ses:
                board = ses['board']
                self.assertEqual(ses['board'], board)

            for char in board[0]:
                self.assertIn(char, html)

    def test_submit(self):
        with self.app as client:
            with client.session_transaction() as ses:
                ses['board'] = [['A', 'B', 'C', 'D', 'E'],
                                ['F', 'G', 'H', 'O', 'I'],
                                ['K', 'L', 'M', 'G', 'O'],
                                ['P', 'Q', 'R', 'S', 'T'],
                                ['U', 'V', 'W', 'X', 'Y']]
        post = client.post('/submit', json={"guess": "dog"})

        self.assertIn(post.get_json(), "ok")

        post = client.post('/submit', json={"guess": "ghost"})

        self.assertIn(post.get_json(), "not-on-board")

        post = client.post('/submit', json={"guess": "abcde"})

        self.assertIn(post.get_json(), "not-word")

    def test_user_info(self):
        with self.app as client:
            with client.session_transaction() as ses:
                ses["play_count"] = 5
                ses["high_score"] = 20

        response = client.get('/user-info')
        data = response.get_json()

        self.assertEqual(data["high_score"], 20)
        self.assertEqual(data["play_count"], 5)

    # def test_get_high_score(self):
    #     with app.test_request_context():
    #         with self.app.test_client() as client:
    #             with client.session_transaction() as ses:
    #                 self.assertEqual(get_high_score(), 0)
    #                 ses["high_score"] = 5
    #                 self.assertEqual(get_high_score(), 5)

    # def test_update_play_count(self):
    #     with app.test_client() as client:
    #         with client.session_transaction() as ses:
    #             self.assertEqual(ses["play_count"], 1)

    # def test_update_score(self, resp='ok', word='test'):
    #     global current_score
    #     self.assertEqual(current_score, 4)

    # def test_update_high_score(self):
    #     global current_score
    #     global high_score
    #     current_score = 10
    #     high_score = 8
    #     with app.test_client() as client:
    #         with client.session_transaction() as ses:
    #             self.assertEqual(ses["high_score", current_score])
