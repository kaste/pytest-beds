import pytest
fixture = pytest.fixture


@fixture
def bed(request):
    from google.appengine.ext import testbed
    bed = testbed.Testbed()
    bed.activate()
    request.addfinalizer(lambda: teardown_bed(bed))
    return bed

def teardown_bed(bed):
    bed.deactivate()


@fixture
def mailer(bed):
    from google.appengine.ext import testbed

    bed.init_mail_stub(show_mail_body=False)
    mailer = bed.get_stub(testbed.MAIL_SERVICE_NAME)
    return mailer


@fixture
def channel(bed):
    from google.appengine.ext import testbed

    bed.init_channel_stub()
    channel = bed.get_stub(testbed.CHANNEL_SERVICE_NAME)
    return channel


@fixture
def urlfetch(bed):
    from google.appengine.ext import testbed

    bed.init_urlfetch_stub()
    urlfetch = bed.get_stub(testbed.URLFETCH_SERVICE_NAME)
    return urlfetch


@fixture
def memcache(bed):
    bed.init_memcache_stub()

    from google.appengine.api import memcache
    return memcache


@fixture
def taskqueue(bed, pytestconfig, monkeypatch):
    from google.appengine.ext import testbed
    import taskqueue_stub

    project_root = pytestconfig.getvalue('project_root')
    bed.init_taskqueue_stub(root_path=project_root)
    taskqueue = bed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
    monkeypatch.setattr(taskqueue, 'get_filtered_tasks',
                        taskqueue_stub.get_filtered_tasks)
    return taskqueue


@fixture
def deferreds(taskqueue):
    from .taskqueue_stub import TaskqueueStub
    return TaskqueueStub(taskqueue)


@fixture
def blobstore(bed):
    bed.init_blobstore_stub()
    bed.init_files_stub()
    from google.appengine.ext import blobstore
    return blobstore


@fixture
def search(bed):
    bed.init_search_stub()
    from google.appengine.api import search
    return search


@fixture
def app_identity(bed):
    bed.init_app_identity_stub()
    from google.appengine.api import app_identity
    return app_identity


@fixture
def ndb_(bed, memcache, monkeypatch):
    from google.appengine.datastore import datastore_stub_util
    policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy()
    bed.init_datastore_v3_stub(consistency_policy=policy)

    from google.appengine.ext import ndb
    monkeypatch.setattr(ndb, 'set_consistent_probability',
                        lambda p: policy.SetProbability(p), raising=False)
    return ndb


@fixture
def ndb(ndb_):
    ndb_.set_consistent_probability(1)
    return ndb_


@fixture
def slowndb(ndb_):
    ndb_.set_consistent_probability(0)
    return ndb_


@fixture
def users(bed):
    bed.setup_env(overwrite=True, **{})
    bed.init_user_stub()

anonymous = users


@fixture
def login(bed, users):
    def decorated(id='', email='', admin=False, domain='google'):
        data = dict(
            user_id=str(id),
            user_email=email,
            user_is_admin=repr(int(admin)),
            auth_domain=domain
        )
        bed.setup_env(overwrite=True, **data)

    decorated.logout = lambda: decorated()

    return decorated


del pytest, fixture