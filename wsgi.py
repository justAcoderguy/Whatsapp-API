from app.main import app

if __name__ == "__main__":
    app.run()

# gunicorn -w 4 wsgi:app