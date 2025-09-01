from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .forms import RegisterForm, LoginForm
from .models import User
from . import db, serializer
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Ese correo electrónico ya está registrado.', 'warning')
            return redirect(url_for('auth.register'))

        username = email.split('@')[0]
        new_user = User(
            email=email,
            username=username,
            confirmed=False
        )
        new_user.set_password(form.password.data)
        
        db.session.add(new_user)
        db.session.commit()

        token = serializer.dumps(email, salt='email-confirm')
        # En una app real, aquí enviarías el email.
        # Por ahora, redirigimos a una página de demostración.
        return redirect(url_for('auth.check_email', token=token))
        
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Este correo no está registrado.', 'danger')
            return redirect(url_for('auth.login'))

        if not user.confirmed:
            token = serializer.dumps(email, salt='email-confirm')
            flash('Tu cuenta no está validada. Por favor, revisa tu correo.', 'warning')
            return redirect(url_for('auth.check_email', token=token))

        if user.check_password(password):
            login_user(user) # Flask-Login maneja la sesión
            flash('¡Bienvenido de nuevo!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
            
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/check_email/<token>')
def check_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except:
        email = None
    return render_template('check_email.html', token=token, email=email)


@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            if not user.confirmed:
                user.confirmed = True
                user.points = 50 # Puntos de bienvenida
                db.session.commit()
                flash('¡Cuenta validada! Has recibido 50 puntos de bienvenida.', 'success')
            else:
                flash('Esta cuenta ya había sido validada. Ya puedes iniciar sesión.', 'info')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuario no encontrado.', 'danger')
            return redirect(url_for('auth.register'))
    except:
        flash('El enlace de validación ha expirado o es inválido.', 'danger')
        return redirect(url_for('auth.register'))