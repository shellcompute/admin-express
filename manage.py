import click
from app import create_app, db, models


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, models=models)


@app.teardown_appcontext
def shutdown_session(exception=None):
    # print('session closed.')
    # db.session.remove()
    pass


# @click.argument("name")
@app.cli.command('account-init')
def init_admin():
    """initiate admin account"""
    print('initiating admin account')
    from app.models import init_admin
    init_admin()

    from app.views import collect_views
    collect_views()

    click.echo('admin\'s account and roles created, please change the password asap.')


if __name__ == '__main__':
    # db.create_all()
    app.run(host='0.0.0.0', port=31008)
