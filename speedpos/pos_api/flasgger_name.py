from flask import Flask, Blueprint, render_template, request, redirect, jsonify
from flasgger import Swagger, swag_from

app = Flask(__name__)

swagger = Swagger(app)


# swagger展现api接口方法集合，访问http://127.0.0.1:9001/apidocs/即可
@app.route('/api/publish/k8sbuildjob/', methods=['POST'])
@swag_from('login.yml')
def build():
    return jsonify({})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
