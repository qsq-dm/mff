from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from thirdparty.wechat import wechat

server_verify       = Blueprint('server_verify', __name__,
                        template_folder='templates')

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class TodoItem(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(TodoItem, '/todos/<int:id>')
app.register_blueprint(api_bp)

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)



from flask_inputs import Inputs
from wtforms.validators import DataRequired

class CustomerInputs(Inputs):
    rule = {
        'id': [DataRequired()]
    }
    
    
    