from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Todo({self.title}, {self.description}, {self.completed})"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/todos", methods=["GET"])
def get_all_todos():
    todos = Todo.query.all()
    return jsonify([todo.serialize() for todo in todos])

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    todo = Todo(title=data["title"], description=data["description"])
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.serialize())

@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo.serialize())

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    data = request.get_json()
    todo.title = data["title"]
    todo.description = data["description"]
    todo.completed = data["completed"]
    db.session.commit()
    return jsonify(todo.serialize())

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)