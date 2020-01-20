import os
from flask import Flask, request, abort, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.sql import func
from sqlalchemy.orm import load_only

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):

  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions



def categories_as_dict():
    # Read all categories from the db and return as a dictionary
    try:
        selection = Category.query.order_by(Category.id).all()
        categories = {}
        for category in selection:
            categories[category.id] = category.type
        return categories
    except:
        abort(404)

def paginated_questions(request):
    # Return paginated questions and total_questions_count

    try:
        selection = Question.query.order_by(Question.id).all()
        total_questions_count = len(selection)
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)
        return current_questions, total_questions_count

    except:
        abort(404)

def request_matter(request):
    """Determines if the POST request to '/questions'
       is for search or for adding a new question.
    """

    
    body = request.get_json()



    if 'question' in body and \
       'answer' in body and \
       'difficulty' in body and \
       'category' in body:

       return 'new_question'

    elif 'searchTerm' in body:
       return 'search'

    else:
        abort(400)

def add_new_question(request):
    # add new question to the database
    body = request.get_json()




    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = int(body.get('difficulty', None))
    new_category = int(body.get('category', None))

    try:
        question = Question(question=new_question,
                            answer=new_answer,
                            difficulty=new_difficulty,
                            category=new_category)
        question.insert()


        current_questions, total_questions_count = paginated_questions(request)
        categories = categories_as_dict()



        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_questions': total_questions_count,
          'categories': categories,
          })

    except:
      abort(422)


def found_questions(request):
    # Retrieve questions from th db that match the search term,
    # paginate found questions and return

    try:
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        selection = Question.query.filter(
                        Question.question.ilike(f'%{search_term}%')).all()
        total_questions_count = len(selection)

        current_questions = paginate_questions(request, selection)
        return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': total_questions_count,
                        'search_term': search_term
                        })
    except Exception as e:
        abort(404)



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)

    '''
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    def questions_id_list(category_id=0):
        """
        Return list of IDs of Questions.
        If given category id is 0 then IDs of all questions will be returned.
        If another category id is given the IDs of questins in the given
        category will be returned
        """

        if category_id == 0:
            questions_ids = db.session.query(Question.id).all()
        else:
            questions_ids = db.session.query(Question.id).\
            filter(Question.category==category_id).all()


        questions_id_list = []

        for id in questions_ids:
            questions_id_list.append(id[0])
        return questions_id_list

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def retrieve_categories():
        categories = categories_as_dict()
        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(categories)
         })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions')
    def retrieve_questions():
        current_questions, total_questions_count  = paginated_questions(request)
        categories = categories_as_dict()

        return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': total_questions_count,
                        'categories': categories
                        })



    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
        except:
            abort(422)

        current_questions, total_questions_count = paginated_questions(request)
        categories = categories_as_dict()

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions_count,
            'categories': categories,
            'deleted': question_id
            })


    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def post_to_question():

        request_matter_r = request_matter(request)

        if request_matter_r == 'new_question':
            return add_new_question(request)
        elif request_matter_r == 'search':

            return found_questions(request)


    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    # DONE
    # implimented in @app.route('/questions', methods=['POST'])


    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        selection = Question.query.filter_by(category=category_id).all()
        total_questions_count = len(selection)
        current_questions = paginate_questions(request, selection)

        return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': total_questions_count,
                        'current_category': category_id
                        })


    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def play_the_quiz():
        body = request.get_json()
        #print(body)
        try:
            quiz_category_dict = body['quiz_category']
            quiz_category_id = int(quiz_category_dict['id'])
            previous_questions = body['previous_questions']
        except:
            abort(400)
        questions_ids = questions_id_list(quiz_category_id)

        for previous_question in previous_questions:
            try:
                questions_ids.remove(previous_question)
            except:
                pass

        try:
            rand_question_id = random.choice(questions_ids)

            question = Question.query.get(rand_question_id)

            question = question.format()
            return jsonify({'success': True,
                            'question': question,
                            })
        except:
            abort(422)


    '''
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
        }), 400

    return app
