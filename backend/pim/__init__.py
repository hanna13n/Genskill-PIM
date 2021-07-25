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
        conn=db.get_db()
        cursor=conn.cursor()
        cursor.execute(
            "select tagname from hashtags"
        )
        tags=(x[0] for x in cursor.fetchall())
        tags=list(tags)
        return render_template('index.html', tags=tags)
    
    from . import notes
    app.register_blueprint(notes.bp)
    
    return app
