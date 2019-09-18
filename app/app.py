from flask import Flask, render_template, request
import json
app = Flask(__name__, template_folder="templates")


@app.route('/')
@app.route('/home')
def home():
    return "<h1>test</h1>"


if __name__ == '__main__':
    app.run(debug=True)
