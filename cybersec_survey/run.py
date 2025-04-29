# run.py

from cybersec_survey.app import app
from cybersec_survey.config import Config


def main():
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)


if __name__ == "__main__":
    main()
