from app import create_app, db
from app.models import RegPoint

app = create_app()

# Esta función especial nos permite añadir datos iniciales a la BD
# desde la línea de comandos con 'flask seed'
@app.cli.command("seed")
def seed():
    """Añade datos iniciales a la base de datos."""
    print("Creando Puntos REG iniciales...")
    if not RegPoint.query.first():
        puntos_reg = [
            {'name': 'Punto REG - Centro', 'lat': -27.7834, 'lon': -64.2656, 'address': 'Av. Belgrano (S) 555'},
            {'name': 'Punto REG - Parque Aguirre', 'lat': -27.7945, 'lon': -64.2588, 'address': 'Olaechea y Urquiza'},
            {'name': 'Punto REG - Barrio 8 de Abril', 'lat': -27.7750, 'lon': -64.2810, 'address': 'Plaza 8 de Abril'},
            {'name': 'Punto REG - UNSE', 'lat': -27.8011, 'lon': -64.2501, 'address': 'Av. Belgrano (S) 1912'}
        ]
        for punto_data in puntos_reg:
            punto = RegPoint(**punto_data)
            db.session.add(punto)
        db.session.commit()
        print("Puntos REG creados.")
    else:
        print("Los Puntos REG ya existen.")
        
if __name__ == '__main__':
    # Solo para desarrollo local
    app.run(debug=True)
