# URL: http://localhost:8080/
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "8080 portundan çalışıyor"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
