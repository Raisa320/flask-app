from datetime import datetime
from flask_login import current_user, login_required, login_user, logout_user
from app import app,db
from flask import flash, redirect, render_template, request, url_for
from app.forms import LoginForm, RegistrationForm,EditProfileForm,PostForm
from app.models import User,Permission,Role,Posts
from werkzeug.urls import url_parse

from app.permisos import admin_required, permission_required

@app.route('/',methods=["GET","POST"])
@app.route('/index',methods=["GET","POST"])
@login_required
def index():
    form=PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Posts(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    posts = Posts.query.order_by(Posts.timestamp.desc()).all()
    return render_template("index.html",title="Home" ,form = form, posts = posts, WRITE = Permission.WRITE)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nombre de usuario o password incorrecto')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title="Login",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Felicitaciones, es usted ahora un usuario registrado!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "Para admins!"

@app.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Para comentarios de moderadores!"

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts= user.posts.all()
    return render_template('user.html',title="Profile" ,user=user, posts=posts)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Tu perfil se actualizó correctamente.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit-profile.html',title="Edit Profile", form=form)

@app.route('/edit-profile/<username>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(username):
    form = EditProfileForm()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Su perfil se actualizó correctamente.')
        return redirect(url_for('.user', username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit-profile.html',title="Edit Profile", form=form)

@app.route('/editar-post/<int:id>',methods=['GET','POST'])
@login_required
def editar_post(id):
    post = Posts.query.filter_by(id=id).first_or_404()
    if current_user.id==post.user_id:
        form=PostForm()
        if form.validate_on_submit():
            post.body=form.body.data
            #post.timestamp=datetime.utcnow()
            db.session.add(post)
            db.session.commit()
            flash('Tu post se actualizó correctamente.')
            return redirect(url_for('.index'))
        form.body.data=post.body
        return render_template('edit-post.html',form=form)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_notfound(error):
    return render_template("404.html"), 404