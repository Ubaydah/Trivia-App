import os
from flask import Flask, request, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category, db
from utils import paginate_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    @app.route("/")
    def hello_world():
        return jsonify({"message": "Wecome to trivia API"})

    @app.route("/api/categories", methods=["GET"])
    def get_all_categories():
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        categories_length = len(formatted_categories)

        if len(formatted_categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": formatted_categories,
                "total_categories": categories_length,
            }
        )

    @app.route("/api/questions", methods=["GET"])
    def get_paginated_questions():
        questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginate_questions(request, questions)
        total_questions = len(questions)
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}

        if len(paginated_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": paginated_questions,
                "categories": formatted_categories,
                "total_questions": total_questions,
                "current_category": "Art",
            }
        )

    @app.route("/api/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404, "Item not found")

        try:
            db.session.delete(question)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
        finally:
            db.session.close()

        return jsonify({"success": True, "id": question_id}), 204

    @app.route("/api/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty,
            )
            question.insert()

            return jsonify({"status": True, "question": question.id}), 201
        except Exception as e:
            abort(422)

    @app.route("/api/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        questions = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
        ).all()

        if questions:
            resultQuestions = paginate_questions(request, questions)
            return (
                jsonify(
                    {
                        "success": True,
                        "questions": resultQuestions,
                        "total_questions": len(questions),
                    }
                ),
                200,
            )

        else:
            abort(404, "no result found")

    @app.route("/api/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)

        if category is None:
            abort(404, "Category does not exist")

        questions_in_category = Question.query.filter(
            Question.category == str(category_id)
        ).all()
        paginated_questions = paginate_questions(request, questions_in_category)

        if len(paginated_questions) == 0:
            abort(404)

        return (
            jsonify(
                {
                    "success": True,
                    "questions": paginated_questions,
                    "total_questions": len(questions_in_category),
                    "current_category": category.type,
                }
            ),
            200,
        )

    @app.route("/api/quizzes", methods=["POST"])
    def get_quizzes():
        try:

            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category = body.get("quiz_category", None)
            category_id = quiz_category["id"]

            if category_id == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()

            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == str(category_id),
                ).all()

                question = random.choice(questions)

            return (
                jsonify(
                    {
                        "success": True,
                        "question": question.format(),
                    }
                ),
                200,
            )
        except Exception as e:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Page not found"}),
            404,
        )

    @app.errorhandler(422)
    def entity_unprocessable(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Unprocessable entity"}
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal server error"}
            ),
            500,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "message": "Method not allowed", "error": 405}),
            405,
        )

    @app.errorhandler(503)
    def server_unavailable(error):
        return (
            jsonify({"success": False, "message": "Server Unavailable", "error": 503}),
            503,
        )

    return app
