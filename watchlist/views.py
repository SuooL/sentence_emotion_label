# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie, Comment


@login_required
@app.route('/', methods=['GET', 'POST'])
def index():

    page=request.args.get('page',1,type=int)

    if current_user.is_authenticated:
        if current_user.id == 2:
            pagination=Comment.query.filter_by(rank_a=0).order_by(Comment.id.asc()).paginate(page,per_page=10,error_out=False)
        elif current_user.id == 3:
            pagination=Comment.query.filter_by(rank_b=0).order_by(Comment.id.asc()).paginate(page,per_page=10,error_out=False)
        elif current_user.id == 4:
            pagination=Comment.query.filter_by(rank_c=0).order_by(Comment.id.asc()).paginate(page,per_page=10,error_out=False)
        else:
            flash("未授权用户")
            pagination=Comment.query.order_by(Comment.id.asc()).paginate(page,per_page=10,error_out=False)
            # return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
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

    if current_user.id == 2:
        comment.rank_a = name
    elif current_user.id == 3:
        comment.rank_b = name
    elif current_user.id == 4:
        comment.rank_c = name    

    if int(name) == 4:
        flash(str(comment_id) + str(name))
        db.session.delete(comment)

    db.session.commit()
    flash(str(comment_id) + str(name))

    return redirect(url_for('index'))

@app.route('/comment/relabel/<int:comment_id>', methods=['POST'])
@login_required
def relabel(comment_id):

    comment = Comment.query.get_or_404(comment_id)
    name = request.form['rank']

    if current_user.id == 2:
        comment.rank_a = name
    elif current_user == 3:
        comment.rank_b = name
    elif current_user == 4:
        comment.rank_c = name    



    db.session.commit()
    flash(str(comment_id) + str(name))

    return redirect(url_for('records'))


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

@app.route('/records', methods=['GET', 'POST'])
@login_required
def records():

    page=request.args.get('page',1,type=int)

    if current_user.is_authenticated:
        if current_user.id == 2:
            pagination=Comment.query.filter(Comment.rank_a>0).order_by(Comment.id.asc()).paginate(page,per_page=10000,error_out=False)
        elif current_user.id == 3:
            pagination=Comment.query.filter(Comment.rank_b>0).order_by(Comment.id.asc()).paginate(page,per_page=10000,error_out=False)
        elif current_user.id == 4:
            pagination=Comment.query.filter(Comment.rank_c>0).order_by(Comment.id.asc()).paginate(page,per_page=10000,error_out=False)
        else:
            flash("未授权用户")
            pagination=Comment.query.order_by(Comment.id.asc()).paginate(page,per_page=10000,error_out=False)
            # return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    comments=pagination.items

    # if request.method == 'POST':
    #     comment = Comment.query.get_or_404(comment_id)
    #     name = request.form['rank']

    #     if current_user.id == 2:
    #         comment.rank_a = name
    #     elif current_user == 3:
    #         comment.rank_b = name
    #     else:
    #         comment.rank_c = name    

    #     db.session.commit()
    #     flash(str(comment_id) + str(name))


    return render_template('records.html', comments=comments, pagination=pagination)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

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
