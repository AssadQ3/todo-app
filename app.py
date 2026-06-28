from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "completed": task.completed})

@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/tasks/<int:id>", methods=["PUT"])
def toggle_task(id):
    task = Task.query.get(id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({"id": task.id, "completed": task.completed})

if __name__ == "__main__":
    app.run(debug=True)