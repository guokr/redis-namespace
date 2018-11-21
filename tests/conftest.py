import pytest
#  import redis
import redis_namespace as redis
from mock import Mock

from distutils.version import StrictVersion


NS = u'ns:'
_REDIS_VERSIONS = {}


def get_version(**kwargs):
    params = {'host': 'localhost', 'port': 6379, 'db': 9}
    params.update(kwargs)
    key = '%s:%s' % (params['host'], params['port'])
    if key not in _REDIS_VERSIONS:
        client = redis.Redis(namespace=NS, **params)
        _REDIS_VERSIONS[key] = client.info()['redis_version']
        client.connection_pool.disconnect()
    return _REDIS_VERSIONS[key]


def _get_client(cls, request=None, **kwargs):
    params = {'host': 'localhost', 'port': 6379, 'db': 9}
    params.update(kwargs)
    client = cls(namespace=NS, **params)
    client.flushdb()
    if request:
        def teardown():
            client.flushdb()
            client.connection_pool.disconnect()
        request.addfinalizer(teardown)
    return client


def skip_if_server_version_lt(min_version):
    check = StrictVersion(get_version()) < StrictVersion(min_version)
    return pytest.mark.skipif(check, reason="")


def skip_if_server_version_gte(min_version):
    check = StrictVersion(get_version()) >= StrictVersion(min_version)
    return pytest.mark.skipif(check, reason="")


@pytest.fixture()
def ns():
    return NS


def with_ns(k):
    return NS+k


@pytest.fixture()
def r(request, **kwargs):
    return _get_client(redis.Redis, request, **kwargs)


@pytest.fixture()
def sr(request, **kwargs):
    return _get_client(redis.StrictRedis, request, **kwargs)
