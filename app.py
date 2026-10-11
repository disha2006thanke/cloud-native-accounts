
from service import create_app
from service.models import init_db

app = create_app()


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=False)
