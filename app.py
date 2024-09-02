from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap5
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasktician.db"
db = SQLAlchemy(app)

class DBModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    task_content: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[datetime] = mapped_column(nullable=False)

# create database schema - run once then comment it out
# with app.app_context():
#     db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['task-add']
        new_task = DBModel(task_content=task_content, date_created=datetime.now().date())
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Look's like something is wrong with the database please try again"
    else:
        tasks = DBModel.query.order_by(DBModel.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):

    task_to_delete = DBModel.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
            return "Look's like something is wrong with the database please try again"



@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = DBModel.query.get_or_404(id)
    if request.method == 'POST':
        try:
            task.task_content = request.form['task-update']
            db.session.commit()
            return redirect('/')
        except:
            return "Look's like something is wrong with the database please try again"
    return render_template('update.html', task = task)



if __name__ == '__main__':
    app.run(debug=True)