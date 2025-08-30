# app.py
from flask import Flask, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from werkzeug.middleware.proxy_fix import ProxyFix
from forms import RegisterForm, LoginForm
from urllib.parse import quote
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-super-secreta")
serializer = URLSafeTimedSerializer(app.secret_key)

# 🔐 Seguridad para sesiones en Render
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# 🛡️ Detectar HTTPS detrás de proxy (Render)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# 🧠 Base de datos en memoria (demo)
users = {}

# 🔒 Decorador para proteger rutas privadas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('Debes iniciar sesión para acceder.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 🧭 Ruta raíz redirige al registro
@app.route('/')
def index():
    return redirect(url_for('register'))

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'email' in session:
        flash('Ya estás autenticado.', 'info')
        return redirect(url_for('dashboard'))

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_data = users.get(email)

        if not user_data:
            flash('Este correo no está registrado.', 'danger')
            return render_template('login.html', form=form)

        if not user_data['confirmed']:
            token = serializer.dumps(email, salt='email-confirm')
            safe_token = quote(token)
            flash('Tu cuenta no está validada. Por favor, revisa tu correo.', 'warning')
            return redirect(url_for('check_email', token=safe_token))

        if check_password_hash(user_data['password'], password):
            session['email'] = email
            flash('¡Bienvenido de nuevo!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)

# 📝 Registro
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
        users[email] = {
            'username': email.split('@')[0],
            'password': hashed_password,
            'confirmed': False,
            'points': 50
        }

        token = serializer.dumps(email, salt='email-confirm')
        safe_token = quote(token)
        return redirect(url_for('check_email', token=safe_token))

    return render_template('register.html', form=form)

# 📩 Verificación de correo
@app.route('/check_email/<token>')
def check_email(token):
    try:
        email_address = serializer.loads(token, salt='email-confirm', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        email_address = None

    return render_template('check_email.html', token=token, email=email_address)

# ✅ Confirmación de cuenta
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

# 🏠 Dashboard protegido
@app.route('/dashboard')
@login_required
def dashboard():
    email = session['email']
    user_data = users.get(email, {})
    username = user_data.get('username', 'Usuario')
    points = user_data.get('points', 0)

    return render_template('dashboard.html', username=username, points=points)

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('login'))

# 🚀 Configuración para Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
