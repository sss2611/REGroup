from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request, session
from flask_login import login_required, current_user
from .models import RegPoint, Deposit
from .forms import DeclarationForm
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    recent_activity = [
        {'item': 'Entrega de Celular Antiguo', 'points': 25, 'icon': 'fa-solid fa-mobile-screen-button'},
        {'item': 'Registro de Monitor CRT', 'points': 40, 'icon': 'fa-solid fa-desktop'},
        {'item': 'Bono de Bienvenida', 'points': 50, 'icon': 'fa-solid fa-gift'}
    ]
    return render_template(
        'dashboard.html', 
        username=current_user.username, 
        points=current_user.points, 
        recent_activity=recent_activity
    )

@main.route('/map')
@login_required
def map_view():
    puntos = RegPoint.query.all()
    puntos_data = [punto.to_dict() for punto in puntos]
    return render_template('map.html', puntos_reg=puntos_data)

@main.route('/scan')
@login_required
def scan():
    """Muestra la página de escaneo."""
    return render_template('scan.html')

@main.route('/process-scan', methods=['POST'])
@login_required
def process_scan():
    """Recibe el ID del Punto REG escaneado desde el JavaScript."""
    data = request.get_json()
    reg_point_id = data.get('reg_point_id')

    if not reg_point_id or not reg_point_id.isdigit():
        return jsonify({'error': 'Código QR inválido.'}), 400

    session['scanned_reg_point_id'] = int(reg_point_id)
    
    redirect_url = url_for('main.declare_deposit')
    return jsonify({'redirect': redirect_url})

@main.route('/declare-deposit', methods=['GET', 'POST'])
@login_required
def declare_deposit():
    """Muestra el formulario para declarar el residuo y lo procesa."""
    reg_point_id = session.get('scanned_reg_point_id')
    if not reg_point_id:
        flash('Primero debes escanear un código QR.', 'warning')
        return redirect(url_for('main.dashboard'))

    reg_point = RegPoint.query.get_or_404(reg_point_id)
    form = DeclarationForm()

    if form.validate_on_submit():
        new_deposit = Deposit(
            item_declared=form.item_description.data,
            user_id=current_user.id,
            reg_point_id=reg_point.id,
            status='pending_verification'
        )
        db.session.add(new_deposit)
        db.session.commit()
        
        session.pop('scanned_reg_point_id', None)

        flash('¡Depósito registrado exitosamente! Recibirás tus puntos una vez que sea verificado.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('declare.html', form=form, reg_point_name=reg_point.name)