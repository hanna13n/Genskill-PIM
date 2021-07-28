from flask import Flask
from flask_cors import CORS
from flask import jsonify

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
        conn=db.get_db()
        cursor=conn.cursor()

        cursor.execute(
            "select tagname from hashtags"
        )

        tags=cursor.fetchall()
        tags=list(tags)
        return jsonify(dict(tags=tags))
        
    
    from . import notes
    app.register_blueprint(notes.bp)
    
    return app
