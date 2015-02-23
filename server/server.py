#!/usr/bin/python
from flask import *

app = Flask(__name__)

@app.route('/')
def hello_world(name=None): 
    return render_template('base.html',name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)

