# URL: http://localhost:8081/
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "8081 portundan çalışıyor"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
