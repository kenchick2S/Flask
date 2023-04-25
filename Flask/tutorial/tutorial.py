import flask
app = flask.Flask(__name__)

# http://127.0.0.1:5000
@app.route("/")
@app.route("/hello")
def hello():
    return __name__

# http://127.0.0.1:5000/data/appInfo/FlaskSE
@app.route('/data/appInfo/<name>', methods=['GET'])
def queryDataMessageByName(name):
    print("type(name) : ", type(name))
    return 'String => {}'.format(name)

# http://127.0.0.1:5000/data/appInfo/id/5
@app.route('/data/appInfo/id/<int:id>', methods=['GET'])
def queryDataMessageById(id):
    print("type(id) : ", type(id))
    return 'int => {}'.format(id)

# http://127.0.0.1:5000/data/appInfo/version/1.01
@app.route('/data/appInfo/version/<float:version>', methods=['GET'])
def queryDataMessageByVersion(version):
    print("type(version) : ", type(version))
    return 'float => {}'.format(version)

if __name__ == '__main__':
    app.run()