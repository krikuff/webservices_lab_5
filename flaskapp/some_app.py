from flask import Flask
app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

from flask import render_template
@app.route("/data_to")
def deta_to():
    some_pars = {'user':'Ivan','color':'red'}
    some_str = 'Hello my dear friends!'
    some_value = 10
    return render_template('simple.html', some_str = some_str,
    some_value = some_value, some_pars = some_pars)

