import importlib
import os

from quart import Quart, jsonify

app = Quart(__name__)

# Get all endpoints
for file in os.listdir("render"):
    if file.endswith(".py"):
        lib = importlib.import_module(f"render.{file[:-3]}")
        app.register_blueprint(getattr(lib, "blueprint"))


for blpr in app.iter_blueprints():
    print(blpr)


@app.route('/')
def home():
    # TODO: automate this
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


app.run()
