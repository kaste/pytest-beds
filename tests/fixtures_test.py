import pytest
always = pytest.mark.usefixtures


from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import deferred


class User(ndb.Model):
    name = ndb.StringProperty()



class TestNdb:
    def test_by_default_always_consistent(self, ndb):
        hk = User(name='herrkaste')
        hk.put()

        users = User.query().fetch()

        assert users == [hk]

    def test_slow_ndb_eventual_not_consistent(self, slowndb):
        hk = User(name='herrkaste')
        hk.put()

        users = User.query().fetch()

        assert users != [hk]

    def test_dynamically_change_to_not_consistent(self, ndb):
        hk = User(name='herrkaste')
        hk.put()
        users = User.query().fetch()
        assert users == [hk]

        ndb.set_consistent_probability(0)
        User(name='frauludewig').put()

        users = User.query().fetch()
        assert users == [hk]


class TestUser:
    def test_anonymous(self, anonymous):
        user = users.get_current_user()
        assert user is anonymous

    def test_login(self, login):
        login(1, 'hk')
        user = users.get_current_user()
        assert user is not None

    def test_logout(self, login):
        login(1, 'hk')
        login.logout()
        user = users.get_current_user()
        assert user is None


messages = []

@pytest.fixture
def clear_messages(request):
    def _clear():
        messages[:] = []
    request.addfinalizer(_clear)


def work(message):
    messages.append(message)

def more_work():
    messages.append('work')
    deferred.defer(work, 'and more_work')

@always('clear_messages')
class TestTaskqueue:
    def test_run_deferreds(self, deferreds):
        deferred.defer(work, 'hello')

        deferreds.consume()

        assert messages == ['hello']

    def test_run_next_deferred(self, deferreds):
        deferred.defer(more_work)

        deferreds.tick()
        assert messages == ['work']

        deferreds.tick()
        assert messages == ['work', 'and more_work']


    def testC(self, channel):
        pass


