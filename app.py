from flask import Flask, render_template, abort, request, redirect
app = Flask(__name__)

tasks = [
  {'id': 1,
   'title': u'Buy groceries',
   'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
   'done': False},
  {'id': 2,
   'title': u'Learn Python',
   'description': u'Need to find a good Python tutorial on the web',
   'done': False}]

@app.route("/tasks")
def index():
  return render_template("task/list.html", tasks=tasks)

@app.route("/task/view/<int:task_id>", methods=['GET'])
@app.route("/tarefa/ver/<int:task_id>", methods=['GET'])
def get(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  return render_template("task/view.html", task=task[0])

@app.route("/task/new/")
def new():
  return render_template("task/new.html")

@app.route("/task/create", methods=['POST'])
def create():
  task = {'id': tasks[-1]['id'] + 1,
          'title': request.form['title'],
          'description': request.form['description'],
          'done': False}

  tasks.append(task)
  return redirect("/tasks", code=302)

@app.route("/task/edit/<int:task_id>", methods=['GET'])
def edit(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  return render_template("task/edit.html", task=task[0])

@app.route("/task/update/<int:task_id>", methods=['GET', 'POST'])
def update(task_id):
  key = [int(i) for i, task in enumerate(tasks) if task['id'] == task_id]
  tasks[key[0]]['title']       = request.form['title']
  tasks[key[0]]['description'] = request.form['description']
  return redirect("/tasks", code=302)

@app.route("/task/remove/<int:task_id>", methods=['GET'])
def remove(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  tasks.remove(task[0])
  return redirect("/tasks", code=302)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)