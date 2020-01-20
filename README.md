# Udacity Trivia API
This project is the 2nd project out of 5 projects of Udacity Full Stack  Developer Nanodegree.
The scope of the project is to create a RESTful API for a Trivia game.
Udacity Trivia is a quiz game. Users are able to:
- View questions - both all questions and by category.
- View categories.
- Delete a question.
- Add a question.
- Search the questions database.
- Play the quiz.

By completing this project, students learn and apply their skills structuring and implementing well formatted API endpoints that leverage knowledge of HTTP and API development best practices.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).


## Getting Started

### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client:
```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

### Tests
In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

### Endpoints
#### GET /categories
- General:
    - Returns a list of categories' ids with names, success value, and total number of categories
    - Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

#### GET /questions
- General:
    - Returns a list of question objects, list of categories' ids with names, success value, total number of questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### DELETE /questions/{question_id}
- General:
	- Deletes the question of the given ID if it exists. Returns the id of the deleted question, list of categories' ids with names, success value, total number of questions., and the paginated list of question objects based on current page number to update the frontend.
  - Sample:  `curl -X DELETE http://127.0.0.1:5000/questions/10`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "deleted": 10,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```



#### POST /questions
- General:
    - Sending a POST request to this endpoint can either search the question database or add a new question to the database. If the request body contains a new question object then the posted question is added to the database and if the request body contains a search term then the question database is searched and matched questions are returned. Look below for searching description.
    - Creates a new question using the question, answer, category and difficulty score. Returns the id of the created question, success value, total questions, and paginated list of question objects based on current page number to update the frontend.
	- sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Which planet is the closest to Earth?", "answer":"Venus", "difficulty":"4", "category": "1"}'`
```
{
"categories":{
"1":"Science",
"2":"Art",
"3":"Geography",
"4":"History",
"5":"Entertainment",
"6":"Sports"
},
"created":28,
"questions":[
{
"answer":"Apollo 13",
"category":5,
"difficulty":4,
"id":2,
"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
{
"answer":"Tom Cruise",
"category":5,
"difficulty":4,
"id":4,
"question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
},
{
"answer":"Maya Angelou",
"category":4,
"difficulty":2,
"id":5,
"question":"Whose autobiography is entitled "I Know Why the Caged Bird Sings"?"
},
{
"answer":"Edward Scissorhands",
"category":5,
"difficulty":3,
"id":6,
"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
},
{
"answer":"Muhammad Ali",
"category":4,
"difficulty":1,
"id":9,
"question":"What boxer"s original name is Cassius Clay?"
},
{
"answer":"Brazil",
"category":6,
"difficulty":3,
"id":10,
"question":"Which is the only team to play in every soccer World Cup tournament?"
},
{
"answer":"Uruguay",
"category":6,
"difficulty":4,
"id":11,
"question":"Which country won the first ever soccer World Cup in 1930?"
},
{
"answer":"George Washington Carver",
"category":4,
"difficulty":2,
"id":12,
"question":"Who invented Peanut Butter?"
},
{
"answer":"Lake Victoria",
"category":3,
"difficulty":2,
"id":13,
"question":"What is the largest lake in Africa?"
},
{
"answer":"The Palace of Versailles",
"category":3,
"difficulty":3,
"id":14,
"question":"In which royal palace would you find the Hall of Mirrors?"
}
],
"success":True,
"total_questions":20
}
```

#### POST /questions
- General:
    - Sending a POST request to this endpoint can either search the question database or add a new question to the database. If the request body contains a new question object then the posted question is added to the database and if the request body contains a search term then the question database is searched and matched questions are returned. Look above for question adding description description.
    - Search questions that match the search term. Returns the search term, success value, number of total questions that match the search term, and paginated list of question objects that match the search term.
	- Sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`
```
{
"questions":[
{
"answer":"Maya Angelou",
"category":4,
"difficulty":2,
"id":5,
"question":"Whose autobiography is entitled "I Know Why the Caged Bird Sings"?"
},
{
"answer":"Edward Scissorhands",
"category":5,
"difficulty":3,
"id":6,
"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
}
],
"search_term":"title",
"success":True,
"total_questions":2
}
```

#### GET /categories/{category_id}/questions
- General:
	- Gets questions based on category. Returns current category, success value, total number of questions in this category and the paginated list of question objects in this category.  
  - Sample: `curl http://127.0.0.1:5000/categories/5/questions`
```
  {
    "current_category": 5,
    "questions": [
      {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
      {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }
    ],
    "success": true,
    "total_questions": 3
  }
```

#### POST /quizzes
- General:
    - Gets questions to play the quiz. This endpoint takes a category and the list of previous questions and returns a random questions within the given category, if provided, and the question provided is not one of the previous questions.
- sample `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":["3", "9", "12"], "quiz_category": {"id": "3"}}'`
```
{
"question":{
"answer":"Agra",
"category":3,
"difficulty":2,
"id":15,
"question":"The Taj Mahal is located in which Indian city?"
},
"success":True
}
```

## Deployment N/A

## Authors
Hakob K.
