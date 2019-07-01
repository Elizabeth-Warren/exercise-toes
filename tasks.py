from invoke import task


@task
def start(ctx, docs=False):
    ctx.run('FLASK_APP=toes_app.py FLASK_DEBUG=1 venv/bin/flask run --host=0.0.0.0')


@task
def update_dev(ctx, docs=False):
    ctx.run('zappa update dev')


@task
def update_prod(ctx, docs=False):
    ctx.run('zappa update prod')


@task
def tail(ctx, docs=False):
    ctx.run('zappa tail prod --since 1m')
