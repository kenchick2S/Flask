from flask import Flask, render_template
app = Flask(__name__)

# http://127.0.0.1:5000/text
@app.route('/text')
def text():
    return '<html><body><h1>Hello World</h1></body></html>'

# http://127.0.0.1:5000/home
@app.route('/home')
def home():
    return render_template('home.html')

# http://127.0.0.1:5000/page/text
@app.route('/page/text')
def pageText():
    return render_template('page.html', text="Python Flask !")

# http://127.0.0.1:5000/page/app
@app.route('/page/app')
def pageAppInfo():
    appInfo = {  # dict
        'id': 5,
        'name': 'Python - Flask',
        'version': '1.0.1',
        'author': 'Enoxs',
        'remark': 'Python - Web Framework'
    }
    return render_template('page.html', appInfo=appInfo)

# http://127.0.0.1:5000/page/data
@app.route('/page/data')
def pageData():
    data = {  # dict
        '01': 'Text Text Text',
        '02': 'Text Text Text',
        '03': 'Text Text Text',
        '04': 'Text Text Text',
        '05': 'Text Text Text'
    }
    return render_template('page.html', data=data)

# http://127.0.0.1:5000/static
@app.route('/static')
def staticPage():
    return render_template('static.html')

if __name__ == '__main__':
    app.run()