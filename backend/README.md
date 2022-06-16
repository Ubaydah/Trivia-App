# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql -U postgres trivia < trivia.psql  #for windows user
```

### Run the Server

Activate the virtual environment by navigating to the directory

```bash
cd env
cd Scripts
activate
```
After go back to the `backend directory`

```bash
set FLASK_APP=app
set FLASK_ENV=development
```

To run the server, execute:

```bash
python app.py or flask run
```


## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`


### Documentation 

`GET '/api/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with 3 keys
  - `success` boolean value
  - `categories` that contains an object of id: category_string key: value pairs
  - `total_categories` that contains total number of categories

```json
{
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

`GET '/api/questions'`

- Fetches a dictionary of questions array, categories, current_categiory, total_questions
- Request Arguments: None
- Returns: An object with 5 keys
  - `success` boolean value
  - `categories` that contains an object of id: category_string key: value pairs
  - `questions` that contains an array of questions
  - `total_questions` that contains total number of questions
  - `current_category`

```json
{
  "success": True,
  "questions": [ {
            "answer": "Edward Scissorhands",
            "category": "5",
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },],
  "categories":  {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
  "total_questions": 1,
  "current_category": 'Art',
}
```


`DELETE '/api/questions/<question_id>'`

- deletes the given question id from database 
- Request Arguments: None
- Returns: An object with 5 keys
  - `success` boolean value
  - `id` of item removed


`POST '/api/questions'`

- Creates a new question in the database
- Request Arguments: Question data

```json
{
  "question": "are you fine", 
  "answer": "yes", 
  "category": 2, 
  "difficulty": 1
}
```

- Returns: An object with 2 keys
  - `success` boolean value
  - `question_id` 
  ```json
  {
    "question": 59,
    "status": true
  }
  ```

`POST '/api/questions/search'`

- fetches search results matching the search term in questions table
- Request Arguments: Search term

```json
{
  "searchTerm": "are", 
}
```

- Returns: An object with 3 keys
  
  - `success` boolean value
  - `total_questions` that matched the search term in database
  - `questions_array` 
  
  ```json
  {
    "questions": [
        {
            "answer": "yes",
            "category": "2",
            "difficulty": 1,
            "id": 59,
            "question": "are you fine"
        }
    ],
    "success": true,
    "total_questions": 1
   }
  ```

`GET '/api/categories/<category_id>/questions'`

- Fetches a dictionary of questions in the specified category
- Request Arguments: None
- Returns: An object with 4 keys
  - `success` boolean value
  - `current_category` category of the specified Id
  - `total_questions` total questions in that category
  - `questions` an array of the questions in the specified category 

```json
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": "2",
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
       
    ],
    "success": true,
    "total_questions": 1
}
```

`POST '/api/quizzes'`

- fetches random question in a category not in previous questions
- Request Arguments: Object with key `previous_questions` containing an array of questions IDs to exclude and a category object.

```json
{
"previous_questions": [6, 9, 10],
"quiz_category": {"id": "3", "type": "Geography"}
 }
```

- Returns: An object with 2 keys
  
  - `success` boolean value
  - `question` random question object
  
  
  ```json
  {
    "question": {
        "answer": "Agra",
        "category": "3",
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
    },
    "success": true
  }

  ```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
