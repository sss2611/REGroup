from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from forms import RegisterForm, LoginForm
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

app = Flask(__name__)
app.secret_key = os.urandom(24)
serializer = URLSafeTimedSerializer(app.secret_key)

# Base de datos en memoria para la demo.
# ¡Ahora incluimos los puntos!
# Formato: {'email': {'username': '...', 'password': '...', 'confirmed': False, 'points': 0}}
users = {}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_data = users.get(email)

        if not user_data:
            flash('Este correo no está registrado.', 'danger')
            return render_template('login.html', form=form)

        if not user_data['confirmed']:
            token = serializer.dumps(email, salt='email-confirm')
            flash('Tu cuenta no está validada. Por favor, revisa tu correo.', 'warning')
            return redirect(url_for('check_email', token=token))

        if check_password_hash(user_data['password'], password):
            session['email'] = email
            flash('¡Bienvenido de nuevo!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
            
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email in users:
            flash('Ese correo electrónico ya está registrado.', 'warning')
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # Al registrar un usuario, sus puntos inician en 0
        users[email] = {'email ': email, 'password': hashed_password, 'confirmed': False, 'points': 0}
        
        # Simulación: Damos 50 puntos de bienvenida al validar la cuenta
        users[email]['points'] = 50

        token = serializer.dumps(email, salt='email-confirm')
        return redirect(url_for('check_email', token=token))
        
    return render_template('register.html', form=form)

@app.route('/check_email/<token>')
def check_email(token):
    try:
        email_address = serializer.loads(token, salt='email-confirm', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        email_address = None
    return render_template('check_email.html', token=token, email=email_address)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
        user = users.get(email)
        if user:
            user['confirmed'] = True
            flash('¡Cuenta validada! Has recibido 50 puntos de bienvenida.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Usuario no encontrado.', 'danger')
            return redirect(url_for('register'))
    except (SignatureExpired, BadTimeSignature):
        flash('El enlace de validación ha expirado o es inválido.', 'danger')
        return redirect(url_for('register'))

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        email = session['email']
        user_data = users.get(email, {})
        username = user_data.get('username', 'Usuario')
        points = user_data.get('points', 0) # Obtenemos los puntos
        return render_template('dashboard.html', username=username, points=points) # Pasamos los puntos a la plantilla
    
    flash('Debes iniciar sesión para ver esta página.', 'info')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

