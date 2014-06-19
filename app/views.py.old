#views.py
# ---- IMPORTS and CONFIGS ---- #
from flask import Flask, flash, redirect, render_template, request, \
    session, url_for, g

from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import AddTask, RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import FTasks, User

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in',None)
    session.pop('user_id', None)
    flash('You are logged out.  Bye. :(')
    return redirect(url_for('login'))
    
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = User.query.filter_by(name=request.form['name'],
                                password=request.form['password']).first()
        if u is None:
            error = 'Invalid username or password.'
        else:
            session['logged_in'] = True
            session['user_id'] = u.id
            flash('You are logged in.  Go crazy.')
            return redirect(url_for('tasks'))
    return render_template('login.html',
                           form = LoginForm(request.form),
                           error=error)

@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(FTasks).filter_by(status='1').order_by(FTasks.due_date.asc())
    closed_tasks = db.session.query(FTasks).filter_by(status='0').order_by(FTasks.due_date.asc())
    return render_template('tasks.html', form = AddTask(request.form), open_tasks=open_tasks, closed_tasks=closed_tasks)

#add new tasks
@app.route('/add/', methods=["GET", "POST"])
@login_required
def new_task():
    form = AddTask(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_task = FTasks(
            form.name.data,
            form.due_date.data,
            form.priority.data,
            form.posted_date.data,
            '1',
            session['user_id']
            )
        db.session.add(new_task)
        db.session.commit()
        flash("New entry was successfuly posted.  Thank you.")
    else:
        flash_errors(form)
    return redirect(url_for('tasks'))
    
# mark tasks as complete
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).update({"status":"0"})
    db.session.commit()
    flash('The task was marked as complete.')
    return redirect(url_for('tasks'))
        
# delete tasks
@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('The task was deleted.')
    return redirect(url_for('tasks'))

# register
@app.route('/register/', methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(
            form.name.data,
            form.email.data,
            form.password.data,
            )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please login.')
            return redirect(url_for('login'))
        except IntegrityError:
            error = "User and/or email already exists."
            return render_template('register.html', form=form, error=error)
    else:
        flash_errors(form)
    return render_template('register.html', form=form, error=error)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'Error in the %s field - %s' % (
                getattr(form, field).label.text, error), 'error')
 
# ----- ERROR HANDLERS ----- #            
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
    
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404
    
@app.errorhandler(402)
def internal_error(error):
    return render_template('403.html'), 404
    

