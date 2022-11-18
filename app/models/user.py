from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import AnonymousUserMixin, UserMixin
from app.models.role import Role, Permission
from hashlib import md5
from datetime import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #NEW 18-11-22
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar = db.Column(db.String(300))
    #ENDNEW
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    posts = db.relationship("Posts", backref="author", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == "marcelo":
                self.role = Role.query.filter_by(name="Administrator").first()
        if self.role is None:
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        url = 'https://secure.gravatar.com/avatar'
        hash = md5(self.email.lower().encode("utf-8")).hexdigest()
        self.avatar="{url}/{hash}?d={default}&s={size}&r={rating}".format(
            url=url, hash=hash, size=256, default="retro", rating="g"
        )
    def gravatar(self, size, default="retro", rating="g"):
        url = 'https://secure.gravatar.com/avatar'
        hash = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "{url}/{hash}?d={default}&s={size}&r={rating}".format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        
    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login.anonymous_user = AnonymousUser
