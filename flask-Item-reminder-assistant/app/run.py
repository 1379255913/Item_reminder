from flask import *
import config2
from models import db
app = Flask(__name__)
app.config.from_object(config2)
db.init_app(app)

from api_0 import api as api_1
app.register_blueprint(api_1, url_prefix='/api/v1')
from main1 import main
app.register_blueprint(main)

if __name__ == '__main__':
    app.run()