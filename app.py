from flask.helpers import get_debug_flag

from pastebin.make_app import make_app
from pastebin.settings import DevConfig, ProdConfig

PORT = 5001
CONFIG = DevConfig if get_debug_flag() else ProdConfig
app = make_app(CONFIG)

if __name__ == "__main__":
    if app.debug:
        app.run(port=PORT, threaded=True, use_reloader=True)
    else:
        app.run(port=PORT)
