## redis-namespace

[![Build Status][travis-image]][travis-url] [![PyPi Version][pypi-image]][pypi-url]

[redis-namespace](https://github.com/resque/redis-namespace) for python

Redis namespace provides an interface to a namespaced subset of your [redis](https://redis.io) keyspace (e.g., keys with a common beginning), and requires the [redis-py](https://github.com/andymccurdy/redis-py).

```python
import redis
from redis_namespace import StrictRedis

redis_connection = redis.StrictRedis()
namespaced_redis = StrictRedis(namespace='ns:')
namespaced_redis.set('foo', 'bar')  # redis_connection.set('ns:foo', 'bar')

namespaced_redis.get('foo')
redis_connection.get('ns:foo')

namespaced_redis.delete('foo')
namespaced_redis.get('foo')
redis_connection.get('ns:foo')
```


### Installation

`pip install redis-namespace`


**Warning: The redis-py's version must match redis-namespace's**

Supported list

| redis-py  | redis-namespace |
| --- | --- |
| 3.0.1 | 3.0.1.1 |
| 2.10.6 | 2.10.6.1 |
| 2.10.5 | 2.10.5.2 |
| 2.10.3 | 2.10.3.1 |


[travis-url]: https://travis-ci.org/guokr/redis-namespace
[travis-image]: https://travis-ci.org/guokr/redis-namespace.svg

[pypi-url]: https://pypi.python.org/pypi/redis-namespace/
[pypi-image]: https://img.shields.io/pypi/v/redis-namespace.svg?style=flat-square