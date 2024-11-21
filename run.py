from app import create_app

# Only if the run.py script is launched, launch the app.
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)