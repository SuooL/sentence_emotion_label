# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie, Comment


@login_required
@app.route('/', methods=['GET', 'POST'])
def index():

    page=request.args.get('page',1,type=int)

    if current_user.id == 2:
        pagination=Comment.query.filter_by(rank_a=0).order_by(Comment.id.asc()).paginate(page,per_page=10,error_out=False)
    elif current_user == 3:
        pagination=Comment.query.filter_by(rank_a=0).order_by(Comment.id.asc()).paginate(page,per_page=10,error_out=False)
    else:
        pagination=Comment.query.filter_by(rank_a=0).order_by(Comment.id.asc()).paginate(page,per_page=10,error_out=False)
    
    comments=pagination.items

    return render_template('index.html', comments=comments, pagination=pagination)


@app.route('/movie/edit/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit(comment_id):
    movie = Movie.query.get_or_404(comment_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', comment_id=comment_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/comment/label/<int:comment_id>', methods=['POST'])
@login_required
def label(comment_id):

    comment = Comment.query.get_or_404(comment_id)
    name = request.form['rank']
    comment.rank_a = name
    
    db.session.commit()
    flash(str(comment_id) + str(name))

    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))
