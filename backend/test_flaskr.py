import unittest
import json

from flaskr import create_app
from models import db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        "Define test variables and initialize app."

        self.app = create_app()
        self.client = self.app.test_client

        with self.app.app_context():
            self.db = db
            self.db.create_all()

            self.new_question = {
                "question": "Who is the President of America?",
                "answer": "Trump Donald",
                "category": 4,
                "difficulty": 3,
            }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions(self):
        response = self.client().get("/api/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_cannot_request_beyond_valid_page(self):
        response = self.client().get("/api/questions?page=1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")

    def test_get_categories(self):
        response = self.client().get("/api/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_categories"])

    def test_get_questions_by_category(self):
        response = self.client().get("/api/categories/3/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])

    def test_cannot_get_questions_by_category_that_dont_exist(self):
        response = self.client().get("/api/categories/140/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")

    def test_add_new_question(self):
        response = self.client().post("/api/questions", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data["status"])

    def test_delete_question(self):
        response = self.client().delete("/api/questions/40")

        self.assertEqual(response.status_code, 204)

    def test_error_if_question_to_delete_does_not_exist(self):
        response = self.client().delete("/api/questions/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")

    def test_search_question(self):
        response = self.client().post(
            "/api/questions/search", json={"searchTerm": "what"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

    def test_search_returns_error_if_not_found(self):
        response = self.client().post(
            "/api/questions/search", json={"searchTerm": "movie"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "Page not found")

    def test_get_random_quiz(self):
        response = self.client().post(
            "/api/quizzes",
            json={
                "previous_questions": [6, 9, 10],
                "quiz_category": {"id": "3", "type": "Geography"},
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["question"])
        self.assertEqual(data["question"]["category"], "3")

    def test_422_get_quiz(self):
        res = self.client().post("/api/quizzes", json={"previous_questions": []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable entity")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
