from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app.forms import EditProfileForm
from app import db
from app.models.user import User
from app.permisos import admin_required

user_scope=Blueprint("user",__name__)


@user_scope.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts= user.posts.all()
    return render_template('user.html',title="Profile" ,user=user, posts=posts)

@user_scope.route('/edit-profile', methods=['GET', 'POST'])
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

@user_scope.route('/edit-profile/<username>', methods=['GET', 'POST'])
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