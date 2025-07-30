from agentc_core.config import Config


def register_blueprints(app):
    # TODO: app.register_blueprint(find.blueprint)
    # TODO: app.register_blueprint(index.blueprint)
    # TODO: app.register_blueprint(publish.blueprint)

    from .clean import blueprint as clean_blueprint
    from .env import blueprint as env_blueprint
    from .status import blueprint as status_blueprint
    from .version import blueprint as version_blueprint

    app.register_blueprint(clean_blueprint)
    app.register_blueprint(env_blueprint)
    app.register_blueprint(status_blueprint)
    app.register_blueprint(version_blueprint)


def cmd_web(cfg: Config = None, *, host_port: str, debug: bool = True):
    import flask

    app = flask.Flask(__name__)

    app.config["ctx"] = cfg

    register_blueprints(app)

    a = host_port.split(":")
    if len(a) >= 2:
        host, port = a[0], a[-1]  # Ex: "127.0.0.1:5555"
    else:
        host, port = "127.0.0.1", a[-1]  # Ex: "5555".

    app.run(host=host, port=port, debug=debug)
