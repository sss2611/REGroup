from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    """Formulario para que los usuarios se registren."""
    # El campo 'username' ha sido eliminado.
    
    email = StringField('Correo Electrónico', 
                        validators=[InputRequired(), Email(message='Por favor, introduce un correo válido.')])
    
    password = PasswordField('Contraseña', 
                             validators=[InputRequired(), Length(min=6, max=80)])
    
    confirm_password = PasswordField('Confirmar Contraseña', 
                                     validators=[InputRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')])
    
    accept_tos = BooleanField(
        'Acepto los Términos y Condiciones', # La etiqueta aquí es simple, el enlace se crea en el HTML.
        validators=[InputRequired(message='Debes aceptar los términos para registrarte.')]
    )

    submit = SubmitField('Crear Cuenta')

class LoginForm(FlaskForm):
    """Formulario para que los usuarios inicien sesión."""
    email = StringField('Correo Electrónico', validators=[InputRequired(), Email(message='Correo inválido.')])
    password = PasswordField('Contraseña', validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField('Iniciar Sesión')

class DeclarationForm(FlaskForm):
    """Formulario para que los usuarios declaren el residuo que depositan."""
    item_description = StringField('¿Qué residuo vas a depositar?',
                                   validators=[InputRequired(message="Debes describir el artículo."),
                                               Length(min=5, max=100)])
    submit = SubmitField('Registrar Depósito')