import flask
import eventlet
import os
import socketio

import config
import db
import auth
import routes

HOST = "localhost"
PORT = 8080
SOCKET_IO_NAMESPACE = '/socketio'
__SECRET = 'dev'

__flask_app = None
__socketio_app = None
__app = None


def setup():
    """
    Setup the webserver environment
        Create the web server application
        handle socket communication
        create the app instance
    """
    __setup_flask()
    __setup_blueprints()
    __setup_socketio()
    __setup_app()
    __setup_db()
    routes.register_all()


def __setup_flask():
    """
    Create the flask web server
    """
    global __flask_app
    __flask_app = flask.Flask(
        __name__,
        # template_folder=cls.templateFolder,
        root_path=config.ROOT_DIR,
        static_folder='public',
        static_url_path='/public',
        instance_relative_config=True
    )
    __flask_app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=__SECRET,
        # store the database in the instance folder
        DATABASE=os.path.join(__flask_app.instance_path, 'flaskr.sqlite'),
    )


def __setup_blueprints():
    __flask_app.register_blueprint(auth.bp)
    # __flask_app.register_blueprint(blog.bp)


def __setup_socketio():
    """
    Setup the socket io server for low latency communications
    """
    global __socketio_app
    __socketio_app = socketio.Server()


def __setup_app():
    """
    Setup the flask application handler
    """
    global __app
    __app = socketio.Middleware(__socketio_app, __flask_app)


def __setup_db():
    """
    Setup the database and create a connection
    """
    with __flask_app.app_context():
        db.init_app(__flask_app)
        db.init_db()
    auth.register_user('root', 'root')


def run():
    """
    Run the web server on the port
    """
    eventlet.wsgi.server(
        eventlet.listen(('', PORT)),
        __app
    )


def shutdown():
    """
    Handle the shutdown function
    see https://stackoverflow.com/a/17053522
    """
    print('shutting down')
    shutdown_callback = flask.request.environ.get('werkzeug.server.shutdown')
    if shutdown_callback is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_callback()


def sio_handler(msg, callback=None):
    """
    Socket IO msg handler
    """
    def __register_sio_handler(message, func):
        __socketio_app.on(message, func, namespace=SOCKET_IO_NAMESPACE)

    def __decorator(func):
        return __register_sio_handler(msg, func)
    # support decorator and direct function call
    if callable(callback):
        __register_sio_handler(msg, callback)
    else:
        return __decorator


def sio_emit(msg, data, room=None, skip_sid=None):
    """
    Socket IO emit to client
    :param msg
    :param data
    :param room commonly sid
    :param skip_sid
    """
    __socketio_app.emit(msg, data, room, skip_sid, namespace='/socketio')


def add_route(path, route_callback=None):
    """
    Dynamically add a route to the web server
    Either call directly or use a decorator
    direct:    Webserver.add_route(path, callback)
    decorator: @Webserver.add_route('/index.html')
                   def asdf(): ...
    Args:
        path (str): the path to use for the template
        route_callback (def): the template handler
    """
    # add decorator support ex
    def __decorator(func):
        return __add_route_handler(path, func)

    def __add_route_handler(route_path, func):
        if type(path) is not str:
            raise TypeError('path must be str')
        elif not callable(func):
            raise ValueError('route_callback must be callable')
        __flask_app.add_url_rule(route_path, func.__name__, func)

    # support decorator and direct function call
    if callable(route_callback):
        return __add_route_handler(path, route_callback)
    else:
        return __decorator


def get_routes():
    """
    Get a list of all the registered_routes
    Returns:
        list: of registered_routes sorted alphabetically
    """
    registered_routes = []
    for rule in __flask_app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        # methods = ','.join(rule.methods)
        url = flask.url_for(rule.endpoint, **options)
        # line = urllib.unquote("{:50s} {:20s} {}".format(
        #     rule.endpoint,
        #     methods,
        #     url
        # ))
        registered_routes.append(url)
    return sorted(registered_routes)


def render(template_path, args=None):
    """
    https://stackoverflow.com/questions/9195455/how-to-document-a-method-with-parameters
    Use jinja to render an html page
    Args:
        template_path (str): the path to the template
        args (dict): key value pairs which are used in the template
    """
    if args is None:
        args = {}
    args['pages'] = get_routes()
    return flask.render_template(template_path, **args)


def flask_app_context():
    """
    Decorator
    """
    return __flask_app.app_context()
