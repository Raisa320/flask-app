from datetime import datetime
from flask_login import current_user, login_required
from app import db
from flask import flash, redirect, render_template, url_for,Blueprint
from app.forms import PostForm
from app.models import Posts

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
