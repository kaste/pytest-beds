Convenience plugin on top of the testbed the Google Appengine (GAE) SDK already provides.

.. image:: https://travis-ci.org/kaste/pytest-beds.svg?branch=master
    :target: https://travis-ci.org/kaste/pytest-beds

Install
=======

``pip install pytest-beds``

After that the plugin is enabled by default. You can use specific fixtures (see below) to activate the Testbed and stub specific services.


Options
=======

``--no-gae``
    Disable the plugin, esp. do not change the python paths and try to import dev_appserver.

``--sdk-path PATH``
    The plugin assumes it can just ``import dev_apserver``. If that fails it looks up the SDK path in the environment variable ``GAE``. Otherwise, you can specify the path to the SDK by using the ``--sdk-path PATH`` option.

``--project-root PATH``
    Secondly, the plugin assume that your current path is the projects root folder, t.i. the dirctory which holds the app.yaml. You can specify a different path using ``--project-root PATH``.

``--noisy-tasklets``
    By default the plugin shortens the tracebacks when using ndb tasklets, so they don't include the eventloop's internal noise.
    Use this switch to make ndb noisy again.


Fixtures
========

The plugin provides fixtures to stub the different services. Usage is therefore simple and straightforward::

    # Say, if you create a Foo you hit the database and put some work on queue
    def test_foo(ndb, taskqueue):
        foo = Foo.create()

        assert Foo.query().fetch() == [foo]

List of builtin fixtures::

    bed
    mailer
    channel
    urlfetch
    memcache
    taskqueue
    blobstore
    ndb
    users


Users
-----

There are two fixtures ``anonymous`` and ``login`` to handle the users-stub.

``anonymous``
    Prepares the user stub so that ``users.get_current_user()`` will return None

``login``
    Prepares the user stub and returns a function to login actual users::

        def test_login(login):
            # at this point users.get_current_user() will return None

            login(id=1, email='foo@gmail.com')
            # now users.get_current_user() will return a user

            login.logout()
            # now users.get_current_user() will return None again


Deferreds
---------

The ``deferreds`` fixture inits the taskqueue stub, but returns a useful object, so you can actually run the deferred functions::

    def test_work(deferreds):
        deferred.defer(work, 'to be done')

        deferreds.consume()

        assert 'work has been done'




