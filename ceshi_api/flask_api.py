from flask import Flask, request, session, jsonify

USERNAME = 'admin'
PASSWORD = '123456'
app = Flask(__name__)
app.secret_key = 'pithy'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'Invalid username'
        elif request.form['password'] != PASSWORD:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return jsonify({'code': 200, 'msg': 'success'})
    return jsonify({'code': 401, 'msg': error}), 401


@app.route('/info', methods=['get'])
def info():
    if not session.get('logged_in'):
        return jsonify({'code': 401, 'msg': 'please login !!'})
    return jsonify({'code': 200, 'msg': 'success', 'data': 'info'})


if __name__ == '__main__':
    app.run(debug=True)
