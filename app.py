#!/usr/bin/env python
from flask import Flask, render_template, abort, request, redirect
import MySQLdb
import yaml

app = Flask(__name__)

stream   = open("database.yaml", 'r')
database = yaml.load(stream)

conn = MySQLdb.connect (host   = database['mysql']['host'],
                        user   = database['mysql']['user'],
                        passwd = database['mysql']['passwd'],
                        db     = database['mysql']['db'])
cursor = conn.cursor(MySQLdb.cursors.DictCursor)


@app.route("/tasks")
def index():
  cursor.execute("SELECT * FROM tasks")
  tasks = cursor.fetchall()
  return render_template("task/list.html", tasks=tasks)


@app.route("/task/view/<int:task_id>", methods=['GET'])
@app.route("/tarefa/ver/<int:task_id>", methods=['GET'])
def get(task_id):
  cursor.execute("SELECT * FROM tasks WHERE id = '%s'", (task_id))
  task = cursor.fetchone()
  if len(task) == 0:
    abort(404)
  return render_template("task/view.html", task=task)


@app.route("/task/new/")
def new():
  return render_template("task/new.html")


@app.route("/task/create", methods=['POST'])
def create():
  sql = "INSERT INTO tasks (title, description) VALUES (%s, %s)"
  cursor.execute(sql, (request.form['title'], request.form['description']))
  return redirect("/tasks", code=302)


@app.route("/task/edit/<int:task_id>", methods=['GET'])
def edit(task_id):
  cursor.execute("SELECT * FROM tasks WHERE id = '%s'", (task_id))
  task = cursor.fetchone()
  return render_template("task/edit.html", task=task)


@app.route("/task/update/<int:task_id>", methods=['GET', 'POST'])
def update(task_id):
  sql = "UPDATE tasks SET title = %s, description = %s WHERE id = '%s'"
  cursor.execute(sql, (request.form['title'], request.form['description'], task_id))
  task = cursor.fetchone()
  return redirect("/tasks", code=302)


@app.route("/task/remove/<int:task_id>", methods=['GET'])
def remove(task_id):
  cursor.execute("DELETE FROM tasks WHERE id = '%s'", (task_id))
  return redirect("/tasks", code=302)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)