from datetime import datetime
from flask_login import current_user, login_required
from app import db,auth
from flask import flash, g, jsonify, redirect, render_template, request, url_for,Blueprint
from app.forms import PostForm
from app.models import Posts
from app.models.role import Permission
from app.models.user import User
from app.permisos import permission_required_rest

post_scope=Blueprint("post",__name__)

@post_scope.route('/editar-post/<int:id>',methods=['GET','POST'])
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
            return redirect(url_for('index.index'))
        form.body.data=post.body
        return render_template('edit-post.html',form=form)
    return redirect(url_for('index.index'))


@auth.verify_password
def verify_password(email, password):
    if email == '':
        return False
    user = User.query.filter_by(email = email).first()
    if not user:
        return False
    print(user.email)
    g.current_user = user
    print(g.current_user)
    return user.check_password(password)

@post_scope.route('/postJson/',methods=['POST'])
@auth.login_required
@permission_required_rest(Permission.WRITE)
def new_post():
    post=Posts.from_json(json_post=request.json)
    post.author=g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('.post_detail', id=post.id)}

@post_scope.route("/post-detail/<id>")
def post_detail(id):
    return id