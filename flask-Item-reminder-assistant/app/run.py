from flask import *
import config2
from models import db
from flask_cors import *
app = Flask(__name__)
CORS(app, supports_credentials = True)
app.config.from_object(config2)
db.init_app(app)

from api_0 import api as api_1
app.register_blueprint(api_1, url_prefix='/api/v1')
from main1 import main
app.register_blueprint(main)

if __name__ == '__main__':
    app.run()