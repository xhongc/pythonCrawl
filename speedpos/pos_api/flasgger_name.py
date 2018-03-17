import random
from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)
swagger = Swagger(app)

@swag_from('index.yml')
@app.route('/api/<string:language>/', methods=['GET'])
def index(language):
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query查询参数 formDate表单参数 body（json参数） path路径参数
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """

    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic",
        "simple", "powerful", "amazing",
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )


app.run(debug=True)