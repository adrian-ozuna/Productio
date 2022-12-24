import random as random
from flask import Blueprint, render_template, request, flash, get_flashed_messages, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Note, Task, SubTask

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user = current_user)

@views.route('/notes')
@login_required
def notes():
    return render_template("notes.html", user = current_user)

@views.route('/create-note', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')
        
        hexColors = [
            "#FF5733",
            "#FFF52D",
            "#06B0FF",
            "#2406FF",
            "#A61AEC",
            "#EC1A70",
            "#EC1A37",
            "#63EC1A"
            ]
        randomColor = hexColors[random.randint(0,7)]
        textColor = "white"
        
        if randomColor == hexColors[0] or randomColor == hexColors[7]:
            textColor = "black"

        if len(title) < 1:
            flash("Your note needs a title.", category="error")

        messages = get_flashed_messages()

        if len(messages) == 0:
            new_note = Note(title = title, data = text, borderColor = randomColor, textColor = textColor, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()

            return redirect(url_for('views.home'))

    return render_template("createnote.html", user = current_user)

@views.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.filter_by(id = id).first()
    noteTitle = note.title
    noteText = note.data
    noteId = note.id

    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
    
        if len(title) < 1:
            flash("Your note needs a title.", category="error")

        messages = get_flashed_messages()

        if len(messages) == 0:
            note.title = title
            note.data = text
            db.session.commit()

            return redirect(url_for('views.home'))
    return render_template("editnote.html", user = current_user, title = noteTitle, text = noteText, noteId = noteId)

@views.route('/delete-note/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    note = Note.query.filter_by(id = id).first()

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return redirect(url_for('views.home'))

@views.route('/tasks')
@login_required
def tasks():
    return render_template("tasks.html", user = current_user)

@views.route('/create-task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form['description']

        priority = ''.join(request.form.getlist('btnradio'))

        if len(title) < 1:
            flash("Your task needs a title.", category='error') 

        subtasks = request.form.getlist('subtask')

        if subtasks:
            for subtask in subtasks:
                if len(subtask) < 1:
                    flash("You left an empty step!.")

        messages = get_flashed_messages()
            
        if len(messages) == 0:
            new_task = Task(title = title, description = description, isCompleted = False, priority = priority, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            if subtasks:
                for subtask in subtasks:
                    new_subtask = SubTask(title = subtask.title(), isCompleted = False, task_id = new_task.id)
                    print(new_subtask.id)
                    db.session.add(new_subtask)
                    db.session.commit()

            return redirect(url_for('views.tasks'))

    return render_template("createtask.html", user = current_user)

@views.route('/finish-task/<int:id>', methods=['GET', 'POST'])
@login_required
def finish_task(id):
    task = Task.query.filter_by(id = id).first()
    task.isCompleted = True
    db.session.commit()

    return redirect(url_for('views.tasks'))

@views.route('/delete-task/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    task = Task.query.filter_by(id = id).first()

    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()


    return redirect(url_for('views.tasks'))
