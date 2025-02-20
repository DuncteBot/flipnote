import importlib
import os

from quart import Quart, jsonify, abort, request

api_keys = os.getenv('API_KEYS', 'hello_world').split(',')

app = Quart(__name__)

# Get all endpoints
for file in os.listdir('render'):
    if file.endswith('.py'):
        lib = importlib.import_module(f"render.{file[:-3]}")
        app.register_blueprint(getattr(lib, 'blueprint'))


# for blpr in app.iter_blueprints():
#     print(blpr)

no_auth_paths = ['/', '/filter']


@app.before_request
async def before():
    # check for a blueprint, makes sure we have a route
    if request.blueprint is not None and request.path not in no_auth_paths:
        if 'Authorization' not in request.headers:
            abort(401, 'Not Authorized')
            return
        auth_header = request.headers.get('Authorization')

        if auth_header not in api_keys:
            abort(401, 'Not Authorized')


@app.route('/')
def home():
    # TODO: automate this
    # text in function can be obtained via __doc__
    return jsonify({
        "endpoints": [
            "GET /achievement?text=text[&icon=int]",
            "GET /challenge?text=text[&icon=int]",
            "GET /amiajoke?image=url",
            "GET /bad?image=url",
            "GET /calling?text=text",
            "GET /captcha?text=text",
            "GET /didyoumean?top=text&bottom=text",
            "GET /drake?top=text&bottom=text",
            "GET /facts?text=text",
            "GET /filter",
            "GET /floor?image=url&text=text",
            "GET /fml",
            "GET /jokeoverhead?image=url",
            "GET /trash?face=url&trash=url",
            "GET /pornhub?text=text&text2=text",
            "GET /salty?image=url",
            "GET /scroll?text=text",
            "GET /shame?image=url",
            "GET /ship?user=url&user2=url",
            "GET /what?image=url"
        ],
        "original": {
            "created_by": "AlexFlipnote",
            "repo": "https://github.com/AlexFlipnote/alex_api_archive",
        }
    })


if __name__ == "__main__":
    app.run()
