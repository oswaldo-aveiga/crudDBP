
## Crear un entorno virtual

    python -m venv crud

## Activar el entorno virtual

    crud\Scripts\activate

## Instalar las dependencias necesarias

pip install -r requirements.txt

## Crear la base de datos 'contacts_db'

    crear la base de datos contacts_db;
    En el archivo app.py establecer la contraseña del usuario root de tu MySQL
    ## cambiar en esta linea 
    pp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/contacts_db'


## Ejecución del proyecto
Una vez realizada la configuración anterior, teniendo el entorno virtual activado ejecutar el archivo index.py

python index.py