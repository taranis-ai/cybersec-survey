# run.py

from cybersec_survey.app import app
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run the Flask app")
    parser.add_argument("--host", default="127.0.0.1", help="Host address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5006, help="Port to run on (default: 5006)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
