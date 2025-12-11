from flask import Blueprint, render_template, request, redirect, url_for
from models import Score, User, Product
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
        product_id = request.form['product_id']
        score_date = datetime.now()
        Score.create(user=user_id, product=product_id, score_date=score_date)
        return redirect(url_for('score.list'))
    
    users = User.select()
    products = Product.select()
    return render_template('score_add.html', users=users, products=products)


@score_bp.route('/edit/<int:score_id>', methods=['GET', 'POST'])
def edit(score_id):
    score = Score.get_or_none(score.id == score_id)
    if not score:
        return redirect(url_for('score.list'))

    if request.method == 'POST':
        score.user = request.form['user_id']
        score.product = request.form['product_id']
        score.save()
        return redirect(url_for('score.list'))

    users = User.select()
    products = Product.select()
    return render_template('score_edit.html', score=score, users=users, products=products)
