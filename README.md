/REGroup/
|-- app/
|   |-- __init__.py         # Inicializa la aplicación y extensiones
|   |-- models.py           # Define los modelos de la base de datos (User, Deposit, etc.)
|   |-- forms.py            # (Sin cambios mayores, lo mantenemos)
|   |-- routes.py           # Contendrá las rutas principales (dashboard, mapa, etc.)
|   |-- auth.py             # Contendrá las rutas de autenticación (login, register, logout)
|   |-- templates/
|   |   |-- base.html
|   |   |-- check_email.html
|   |   |-- dashboard.html
|   |   |-- login.html
|   |   |-- map.html
|   |   |-- register.html
|   |   |-- terms.html
|   |-- static/
|       |-- style.css
|       |-- img/
|           |-- logo.jpg
|           |-- REGroup.jpg
|
|-- migrations/             # Carpeta para migraciones de la base de datos
|-- run.py                  # El nuevo punto de entrada para ejecutar la app
|-- requirements.txt        # Dependencias actualizadas
|-- instance/
|   |-- database.db         # Aquí se guardará tu base de datos SQLite