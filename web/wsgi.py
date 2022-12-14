from hhrr_app import create_app
import os

app = create_app()
# docker run -p 5000:5000 flask-app
# docker run -p 5000:5000 -e FLASK_APP=agriculture_app -e FLASK_DEBUG=False flask_app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
