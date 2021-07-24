from flask import Flask, render_template
from flask_cors import CORS


def create_app():
    app = Flask("pim")
    CORS(app)
    app.config.from_mapping(
        DATABASE="pim"
    )

    from . import db
    db.init_app(app)
    
    
    @app.route("/")
    def index():
        return render_template('index.html')
    
    from . import notes
    app.register_blueprint(notes.bp)
    
    return app
