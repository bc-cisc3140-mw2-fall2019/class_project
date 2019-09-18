from flask import Flask, render_template, request
import json
import datetime
app = Flask(__name__, template_folder="templates")

date = datetime.datetime.now()
fakeData = [
    {
        'ID': '23290',
        'dateCreated': date
    },
    {
        'ID': '23291',
        'dateCreated': date
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', info=fakeData)


if __name__ == '__main__':
    app.run(debug=True)
