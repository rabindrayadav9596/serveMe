from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_msearch import Search
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

search2 = Search(db=db)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serveme.db'
    app.config['DEBUG'] = True
    #app.config['MSEARCH_BACKEND'] = 'whoosh'
    #app.config['MSEARCH_ENABLE'] = True

    search2.init_app(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(str(user_id))

    # blueprint for auth routes in our app
   

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint)

    from .setting import setting as setting_blueprint
    app.register_blueprint(setting_blueprint)

    from .paymentController import paymentController as paymentController_blueprint
    app.register_blueprint(paymentController_blueprint)

    from .registrationController import registrationController as registrationController_blueprint
    app.register_blueprint(registrationController_blueprint)

    from .loginController import loginController as loginController_blueprint
    app.register_blueprint(loginController_blueprint)

    from .logoutController import logoutController as logoutController_blueprint
    app.register_blueprint(logoutController_blueprint)

    from .serviceController import serviceController as serviceController_blueprint
    app.register_blueprint(serviceController_blueprint)

    from .providerController import providerController as providerController_blueprint
    app.register_blueprint(providerController_blueprint)


    from .orderController import orderController as orderController_blueprint
    app.register_blueprint(orderController_blueprint)

    

    return app
