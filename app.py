import os
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="meerab_study_hub"
    )


@app.route("/")
def home():
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, task_name, completed FROM tasks ORDER BY id"
    )

    rows = cursor.fetchall()

    tasks = []

    for row in rows:
        task_id = row[0]
        task_name = row[1]
        completed = row[2]

        if completed:
            task_name = "✅ " + task_name + " — Completed"

        tasks.append(task_name)

    cursor.close()
    db.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form["task"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO tasks (task_name) VALUES (%s)",
        (task,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


@app.route("/delete_task/<int:index>")
def delete_task(index):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM tasks ORDER BY id"
    )

    rows = cursor.fetchall()

    if 1 <= index <= len(rows):
        task_id = rows[index - 1][0]

        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

        db.commit()

    cursor.close()
    db.close()

    return redirect("/")


@app.route("/complete_task/<int:index>")
def complete_task(index):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM tasks ORDER BY id"
    )

    rows = cursor.fetchall()

    if 1 <= index <= len(rows):
        task_id = rows[index - 1][0]

        cursor.execute(
            "UPDATE tasks SET completed = TRUE WHERE id = %s",
            (task_id,)
        )

        db.commit()

    cursor.close()
    db.close()

    return redirect("/")


@app.route("/python")
def python_page():
    return render_template("python.html")


@app.route("/dbms")
def dbms_page():
    return render_template("dbms.html")


@app.route("/cpp")
def cpp_page():
    return render_template("cpp.html")


@app.route("/web")
def web_page():
    return render_template("web.html")


app.run(debug=True)