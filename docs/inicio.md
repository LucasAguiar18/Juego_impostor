# Crear entorno virtual
python3 -m venv venv

# Activar entorno
# En Linux/Mac
source venv/bin/activate
# En Windows (PowerShell)
venv\Scripts\activate

# Instalar dependencias dentro del entorno
pip install -r requirements.txt

# Guardar las dependencias instaladas
pip freeze > requirements.txt

🚀 Cómo probar

Instalar dependencias:

pip install -r requirements.txt


Ejecutar:

python run.py


En otra terminal, exponer con ngrok:

ngrok http 5000


Compartí el link público de ngrok con tus amigos → todos verán el lobby y podrán conectarse