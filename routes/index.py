import WebServer


@WebServer.add_route('/')
def index():
    routes = WebServer.get_routes()
    return WebServer.render('index.html', {
        'routes': routes
    })
