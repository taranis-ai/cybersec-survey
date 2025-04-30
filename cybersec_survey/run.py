# run.py

from cybersec_survey.app import app
from cybersec_survey.config import Config
from werkzeug.debug import DebuggedApplication


def main():
    if Config.DEBUG:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)


if __name__ == "__main__":
    main()
