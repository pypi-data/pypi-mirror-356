import os

import dotenv
dotenv.load_dotenv(verbose=True, override=True, dotenv_path='.env.tasks')

from invoke import task




@task
def clean(c):
    """
    Remove build artifacts
    """
    c.run("rm -fr build/")
    c.run("rm -fr dist/")
    c.run("rm -fr *.egg-info")


@task(help={'bumpsize': 'Bump either for a "feature" or "breaking" change'})
def release(c, bumpsize=''):
    """
    Package and upload a release
    """
    clean(c)
    if bumpsize:
        bumpsize = '--' + bumpsize

    c.run("bumpversion {bump} --no-input".format(bump=bumpsize))

    import djmypypi2
    c.run("python setup.py sdist bdist_wheel")
    c.run("twine upload dist/*")

    c.run('git tag -a {version} -m "New version: {version}"'.format(version=djmypypi2.__version__))
    c.run("git push --tags")
    c.run("git push origin master")


@task
def publish(c):
    clean(c)
    c.run('uv build')
    env = {}
    if os.environ.get('UV_PUBLISH_URL'):
        env['UV_PUBLISH_URL'] = os.environ['UV_PUBLISH_URL']
    if os.environ.get('UV_PUBLISH_USERNAME'):
        env['UV_PUBLISH_USERNAME'] = os.environ['UV_PUBLISH_USERNAME']
    if os.environ.get('UV_PUBLISH_PASSWORD'):
        env['UV_PUBLISH_PASSWORD'] = os.environ['UV_PUBLISH_PASSWORD']
    if os.environ.get('UV_INSECURE_HOST'):
        env['UV_INSECURE_HOST'] = os.environ['UV_INSECURE_HOST']
    c.run('uv publish --color=always')
