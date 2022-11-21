from urllib.parse import urlparse
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.forms import LoginForm, PostForm, RegistrationForm
from app.models.posts import Posts
from app.models.role import Permission
from app import db
from app.models.user import User
from app.permisos import admin_required, permission_required

index_scope=Blueprint("index",__name__)


@index_scope.route('/',methods=["GET","POST"])
@index_scope.route('/index',methods=["GET","POST"])
@login_required
def index():
    form=PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Posts(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index.index'))
    posts = Posts.query.order_by(Posts.timestamp.desc()).all()
    return render_template("index.html",title="Home" ,form = form, posts = posts, WRITE = Permission.WRITE)

@index_scope.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nombre de usuario o password incorrecto')
            return redirect(url_for('index.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index.index')
        return redirect(next_page)
    return render_template('login.html',title="Login",form=form)

@index_scope.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@index_scope.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Felicitaciones, es usted ahora un usuario registrado!')
        return redirect(url_for('index.login'))
    return render_template('register.html', title='Register', form=form)

@index_scope.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "Para admins!"

@index_scope.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Para comentarios de moderadores!"