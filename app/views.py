# -*- coding: UTF-8 -*-
from app import app, db
from models import Films, Genre, Users
from flask import render_template, request, Response, redirect, url_for, flash, g
from flask.ext.login import login_user , logout_user , current_user , login_required, LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/', methods=['POST','GET'])
@app.route('/index', methods=['POST','GET'])
def index():
    films = db.session.query(Films, Genre).join(Genre).all()
    if request.method == 'POST':
        return redirect(url_for('update',film_id =request.form['film_id']))
    return render_template('index.html', films=films)

@app.route('/add', methods = ['POST','GET'])
@login_required
def add():
    if request.method == 'POST':
        film = Films(caption=request.form['name'], year= request.form['year'], director= request.form['director'], lenght= request.form['length'], country=request.form['country'],genre_id=request.form['genre'])
        db.session.add(film)
        db.session.commit()
    genres = db.session.query(Genre).all()
    return render_template('add.html', genres=genres)

@app.route('/update', methods = ['POST','GET'])
@login_required
def update():
    film_id = request.args['film_id']
    films, genre = db.session.query(Films, Genre).join(Genre).filter(Films.id == film_id).first()
    genres = db.session.query(Genre).all()
    if request.method == 'POST':
        films.caption = request.form['name']
        films.year = request.form['year']
        films.director = request.form['director']
        films.lenght = request.form['length']
        films.country = request.form['country']
        films.genre_id = request.form['genre']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html',films=films, genre=genre, genres=genres)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['Login']
        password = request.form['Password']
        registered_user = Users.query.filter_by(login=username,password=password).first()
        if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        login_user(registered_user)
        flash('Logged in successfully')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user