from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    email = StringField('Correo Electrónico', 
                        validators=[InputRequired(), Email(message='Por favor, introduce un correo válido.')])
    
    password = PasswordField('Contraseña', 
                             validators=[InputRequired(), Length(min=6, max=80)])
    
    confirm_password = PasswordField('Confirmar Contraseña', 
                                     validators=[InputRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')])
    
    submit = SubmitField('Crear Cuenta')

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', 
                        validators=[InputRequired(), Email(message='Por favor, introduce un correo válido.')])
    
    password = PasswordField('Contraseña', 
                             validators=[InputRequired(), Length(min=6, max=80)])
    
    submit = SubmitField('Iniciar Sesión')
