call C:\ProyectosDjango\Tienda_venv\Scripts\activate.bat
call python manage.py makemigrations
call python manage.py makemigrations core
call python manage.py migrate
call python manage.py migrate core