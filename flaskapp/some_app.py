print("Hello, world! from printf")

from flask import Flask

app = Flask(__name__)


# dec to print
@app.route("/")
def hello():
    return "<html><head></head><body>Hello World from some_app</body></html>"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
