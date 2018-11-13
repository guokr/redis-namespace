## redis-namespace

[redis-namespace](https://github.com/resque/redis-namespace) for python

Redis::Namespace provides an interface to a namespaced subset of your [redis](https://redis.io) keyspace (e.g., keys with a common beginning), and requires the [redis-py](https://github.com/andymccurdy/redis-py).

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
