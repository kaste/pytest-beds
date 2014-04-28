import os, sys
import pytest

def pytest_addoption(parser):
    group = parser.getgroup("testbeds", "Google App Engine testbeds plugin")
    group.addoption('--no-gae', action='store_true',
                    default=False, help='Disable this plugin.')

    group.addoption('--sdk-path', action='store', metavar='PATH',
                    help="Specify the PATH to the Appengine SDK. "
                         "By default the plugin assumes it can just import dev_appserver. "
                         "If that fails it looks for the GAE environment variable."
                    )

    group.addoption('--project-root', action='store', metavar='PATH',
                    default="./",
                    help="Specify the path to your app.yaml file. "
                         "By default assumes the current path."
                    )

    group.addoption('--noisy-tasklets', action='store_true', default=False,
                    help="By default the plugin hides the traceback of the "
                         "(mostly internal) eventloop stuff that ndb.tasklets "
                         "introduce. "
                         "Setting this options will show you the full noisy "
                         "tracebacks again."
                    )


def fix_sys_path(SDK):
    if SDK:
        sys.path.insert(0, SDK)

    import dev_appserver
    dev_appserver.fix_sys_path()

def mute_noisy_tasklets():
    from google.appengine.ext import ndb
    ndb.utils.DEBUG = False
    ndb.utils.__tracebackhide__ = True
    ndb.tasklets.__tracebackhide__ = True
    ndb.context.__tracebackhide__ = True


def pytest_configure(config):
    if config.option.no_gae:
        return

    sdk_path = config.getvalue('sdk_path')
    if sdk_path is None:
        try:
            import dev_appserver
        except ImportError:
            try:
                sdk_path = os.environ['GAE']
            except KeyError:
                raise pytest.UsageError(
                    "Can't find the App Engine SDK. Either set an environment "
                    "variable 'GAE' to the path or use the --sdk-path option.")

    fix_sys_path(sdk_path)

    if not config.option.noisy_tasklets:
        mute_noisy_tasklets()


from .fixtures import *


