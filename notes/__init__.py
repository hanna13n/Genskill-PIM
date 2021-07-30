from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from flask import jsonify

def create_app():
    app = Flask(__name__,static_folder="./frontend/build",static_url_path="/")
    CORS(app)
    app.config.from_mapping(
        DATABASE_URL="postgres://kstmushzcdgcpt:6bb2555f8a584aeb831597b814143bc49a07773f6b4f1a40913966f7148686ff@ec2-34-195-143-54.compute-1.amazonaws.com:5432/dg82d6od9h4fk"
    )

    from . import db
    db.init_app(app)
    
    
    @app.route("/tags")
    @cross_origin()
    def index():
        conn=db.get_db()
        cursor=conn.cursor()

        cursor.execute(
            "select tagname from hashtags"
        )

        tags=cursor.fetchall()
        tags=list(tags)
        return jsonify(dict(tags=tags))

    @app.route('/')
    @cross_origin()
    def serve():
        return send_from_directory(app.static_folder,'index.html')  
    
    from . import notes
    app.register_blueprint(notes.bp)
    
    return app
