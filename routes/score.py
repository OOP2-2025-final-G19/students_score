from flask import Blueprint, render_template, request, redirect, url_for
from models import Score, User, Subject
from datetime import datetime

# Blueprintの作成 a
score_bp = Blueprint('score', __name__, url_prefix='/scores')


@score_bp.route('/')
def list():
    scores = Score.select()
    return render_template('score_list.html', title='注文一覧', items=scores)


@score_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        subject_id = request.form['subject_id']
        score_date = datetime.now()
        Score.create(user=user_id, subject=subject_id, score_date=score_date)
        return redirect(url_for('score.list'))
    
    users = User.select()
    subjects = Subject.select()
    return render_template('score_add.html', users=users, subjects=subjects)


@score_bp.route('/edit/<int:score_id>', methods=['GET', 'POST'])
def edit(score_id):
    score = Score.get_or_none(score.id == score_id)
    if not score:
        return redirect(url_for('score.list'))

    if request.method == 'POST':
        score.user = request.form['user_id']
        score.product = request.form['subject_id']
        score.save()
        return redirect(url_for('score.list'))

    users = User.select()
    subjects = Subject.select()
    return render_template('score_edit.html', score=score, users=users, subjects=subjects)
