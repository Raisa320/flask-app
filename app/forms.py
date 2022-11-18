from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length

from app.models.user import User

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(message="Campo obligatorio")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="Campo Obligatorio")])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField(
        'Repita la contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor use un nombre de usuario diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor ingrese otro email.')

class EditProfileForm(FlaskForm):
    name = StringField('Nombre real', validators=[Length(0, 64)])
    location = StringField('Locación', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mi')
    submit = SubmitField('Actualizar')

class PostForm(FlaskForm):
    body = TextAreaField("¿En qué estás pensando?", validators=[DataRequired()])
    submit = SubmitField('Postear')