import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = "trivia_test"
        myuser = os.environ['DB_USERNAME']
        mypassword = os.environ['DB_PASSWORD']
        self.database_path = "postgresql://{}:{}@{}/{}".format(myuser,
                                                                mypassword,
                                                                'localhost:5432',
                                                                self.database_name)

        self.db = setup_db(self.app, self.database_path)

        # binds the app to the current context
        #with self.app.app_context():
        #    self.db = SQLAlchemy()
        #    self.db.init_app(self.app)
            # create all tables
        #    self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """


    def test_get_questions_for_quiz(self):
        previous_questions = []
        quiz_category = {'type': 'click', 'id': 0}
        for p_question in range(20):
            previous_questions.append(p_question)
            dc = {'previous_questions': previous_questions,
              'quiz_category': quiz_category}

            res = self.client().post('/quizzes', json = dc)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(len(data['question']))
            self.assertFalse(data['question']['id'] in previous_questions)

    def test_delete_non_existant_question(self):
        res = self.client().delete(f'/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_add_question_with_missing_parameter_4(self):
        new_question = {'answer': 'new answer',
                        'difficulty': 3,
                        'category': 5}

        res = self.client().post('/questions', json = new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_add_question_with_missing_parameter_3(self):
        new_question = {'question': 'new question',
                        'difficulty': 3,
                        'category': 5}

        res = self.client().post('/questions', json = new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_add_question_with_missing_parameter_2(self):
        new_question = {'question': 'new question',
                        'answer': 'new answer',
                        'category': 5}

        res = self.client().post('/questions', json = new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_add_question_with_missing_parameter_1(self):
        new_question = {'question': 'new question',
                        'answer': 'new answer',
                        'difficulty': 3
                        }

        res = self.client().post('/questions', json = new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_add_search_delete_a_question(self):
        test_word = 'BpCxfYjbVz'
        new_question = {'question': f'new question {test_word}',
                        'answer': 'new answer',
                        'difficulty': 3,
                        'category': 5}

        # Test add
        res_add = self.client().post('/questions', json = new_question)
        data_add = json.loads(res_add.data)

        self.assertEqual(res_add.status_code, 200)
        self.assertTrue(data_add['success'])

        self.assertTrue(data_add['created'])
        self.assertIsInstance(data_add['created'], int)

        self.assertTrue(len(data_add['questions']))
        self.assertIsInstance(data_add['questions'], list)

        self.assertTrue(data_add['total_questions'])
        self.assertIsInstance(data_add['total_questions'], int)

        self.assertTrue(len(data_add['categories']))
        self.assertIsInstance(data_add['categories'], dict)

        question_id = data_add['created']


        # Test search
        search_term = {'searchTerm': test_word}
        res_search = self.client().post('/questions', json = search_term)
        data_search = json.loads(res_search.data)


        self.assertEqual(res_search.status_code, 200)
        self.assertTrue(data_search['success'])
        self.assertEqual(data_search['search_term'], test_word)
        self.assertTrue(data_search['total_questions'])

        found_id = data_search['questions'][0]['id']
        self.assertEqual(question_id, found_id)

        # Test delete
        res_del = self.client().delete(f'/questions/{question_id}')
        data_del = json.loads(res_del.data)

        self.assertEqual(res_del.status_code, 200)
        self.assertTrue(data_del['success'])

        self.assertTrue(len(data_del['questions']))
        self.assertIsInstance(data_del['questions'], list)

        self.assertTrue(data_del['total_questions'])
        self.assertIsInstance(data_del['total_questions'], int)

        self.assertTrue(len(data_del['categories']))
        self.assertIsInstance(data_del['categories'], dict)

        self.assertEqual(data_add['created'], data_del['deleted'])

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyound_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
