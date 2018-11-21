# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from redis import __version__ as redis_version
from ._version import __version__ as current_version

if not redis_version.startswith('.'.join(current_version.split('.')[:-1])):
    raise Exception('Version mismatch! redis version: %s, redis-namespace version: %s' % (redis_version, current_version))

import redis
from redis.client import Token, Pipeline as _Pipeline, PubSub as _PubSub, EMPTY_RESPONSE
from redis.connection import ConnectionPool
from redis.exceptions import ResponseError
from redis._compat import nativestr, basestring, bytes


NAMESPACED_COMMANDS = {
    "append": ['first'],
    "bitcount": ['first'],
    "bitfield": ['first'],
    "bitop": ['exclude_first'],
    "bitpos": ['first'],
    "blpop": ['exclude_last', 'first'],
    "brpop": ['exclude_last', 'first'],
    "brpoplpush": ['exclude_last'],
    # "debug": ['exclude_first'],
    "bzpopmax": ['exclude_last', 'first'],
    "bzpopmin": ['exclude_last', 'first'],
    "decr": ['first'],
    "decrby": ['first'],
    "del": ['all'],
    "dump": ['first'],
    "exists": ['all'],
    "expire": ['first'],
    "expireat": ['first'],
    "eval": ['eval_style'],
    "evalsha": ['eval_style'],
    "geoadd": ['first'],
    "geohash": ['first'],
    "geopos": ['first'],
    "geodist": ['first'],
    "georadius": [None],
    "georadiusbymember": [None],
    "get": ['first'],
    "getbit": ['first'],
    "getrange": ['first'],
    "substr": ['first'],
    "getset": ['first'],
    "hset": ['first'],
    "hsetnx": ['first'],
    "hget": ['first'],
    "hincrby": ['first'],
    "hincrbyfloat": ['first'],
    "hmget": ['first'],
    "hmset": ['first'],
    "hdel": ['first'],
    "hexists": ['first'],
    "hlen": ['first'],
    "hkeys": ['first'],
    "hscan": ['first'],
    "hscan_each": ['first'],
    "hstrlen": ['first'],
    "hvals": ['first'],
    "hgetall": ['first'],
    "incr": ['first'],
    "incrby": ['first'],
    "incrbyfloat": ['first'],
    "keys": ['first', 'all'],
    "lindex": ['first'],
    "linsert": ['first'],
    "llen": ['first'],
    "lpop": ['first'],
    "lpush": ['first'],
    "lpushx": ['first'],
    "lrange": ['first'],
    "lrem": ['first'],
    "lset": ['first'],
    "ltrim": ['first'],
    "mapped_hmset": ['first'],
    "mapped_hmget": ['first'],
    "mapped_mget": ['all', 'all'],
    "mapped_mset": ['all'],
    "mapped_msetnx": ['all'],
    "memory usage": ['first'],
    "mget": ['all'],
    "monitor": ['monitor'],
    "move": ['first'],
    "mset": ['alternate'],
    "msetnx": ['alternate'],
    "object": ['exclude_first'],
    "persist": ['first'],
    "pexpire": ['first'],
    "pexpireat": ['first'],
    "pfadd": ['first'],
    "pfcount": ['all'],
    "pfmerge": ['all'],
    "psetex": ['first'],
    "psubscribe": ['all'],
    "pttl": ['first'],
    "pubsub channels": [None, 'all'],
    "pubsub numsub": ['all', 'all'],
    "publish": ['first'],
    "punsubscribe": ['all'],
    "rename": ['all'],
    "renamenx": ['all'],
    "restore": ['first'],
    "rpop": ['first'],
    "rpoplpush": ['all'],
    "rpush": ['first'],
    "rpushx": ['first'],
    "sadd": ['first'],
    "scard": ['first'],
    "scan": ['scan_style', 'second'],
    "scan_each": ['scan_style', 'all'],
    "sdiff": ['all'],
    "sdiffstore": ['all'],
    "set": ['first'],
    "setbit": ['first'],
    "setex": ['first'],
    "setnx": ['first'],
    "setrange": ['first'],
    "sinter": ['all'],
    "sinterstore": ['all'],
    "sismember": ['first'],
    "smembers": ['first'],
    "smove": ['exclude_last'],
    "sort": ['sort'],
    "spop": ['first'],
    "srandmember": ['first'],
    "srem": ['first'],
    "sscan": ['first'],
    "sscan_each": ['first'],
    "strlen": ['first'],
    "subscribe": ['all'],
    "sunion": ['all'],
    "sunionstore": ['all'],
    "ttl": ['first'],
    "type": ['first'],
    "unlink": ['all'],
    "unsubscribe": ['all'],
    "zadd": ['first'],
    "zcard": ['first'],
    "zcount": ['first'],
    "zincrby": ['first'],
    "zinterstore": ['exclude_options'],
    "zlexcount": ['first'],
    "zpopmax": ['first'],
    "zpopmin": ['first'],
    "zrange": ['first'],
    "zrangebylex": ['first'],
    "zrangebyscore": ['first'],
    "zrank": ['first'],
    "zrem": ['first'],
    "zremrangebyrank": ['first'],
    "zremrangebylex": ['first'],
    "zremrangebyscore": ['first'],
    "zrevrange": ['first'],
    "zrevrangebylex": ['first'],
    "zrevrangebyscore": ['first'],
    "zrevrank": ['first'],
    "zscan": ['first'],
    "zscan_each": ['first'],
    "zscore": ['first'],
    "zunionstore": ['exclude_options'],
    "[]": ['first'],
    "[]=": ['first']
}
TRANSACTION_COMMANDS = {
    "discard": [],
    "exec": [],
    "multi": [],
    "unwatch": ['all'],
    "watch": ['all'],
}
HELPER_COMMANDS = {
    "auth": [],
    "disconnect!": [],
    "echo": [],
    "ping": [],
    "time": [],
}
ADMINISTRATIVE_COMMANDS = {
    "bgrewriteaof": [],
    "bgsave": [],
    "config": [],
    "dbsize": [],
    "flushall": [],
    "flushdb": [],
    "info": [],
    "lastsave": [],
    "quit": [],
    "randomkey": [],
    "save": [],
    "script": [],
    "select": [],
    "shutdown": [],
    "slaveof": [],
}

COMMANDS = {}
for cs in [NAMESPACED_COMMANDS, TRANSACTION_COMMANDS, HELPER_COMMANDS, ADMINISTRATIVE_COMMANDS]:
    COMMANDS.update(cs)


def get_handling(command_name):
    handling = COMMANDS.get(command_name.lower(), [])
    if not handling:
        return None, None
    if len(handling) == 1:
        return handling[0], None
    elif len(handling) == 2:
        return handling[0], handling[1]
    return None, None


def args_with_namespace(ns, *original_args):
    args = list(original_args)
    if not ns or len(args) < 2:
        return original_args
    command_name = args.pop(0)
    before, _ = get_handling(command_name)
    if not before:
        return original_args
    if before == 'first':
        args[0] = add_namespace(ns, args[0])
    elif before == 'all':
        args = add_namespace(ns, args)
    elif before == 'exclude_first':
        args[1:] = add_namespace(ns, args[1:])
    elif before == 'exclude_last':
        args[:-1] = add_namespace(ns, args[:-1])
    elif before == 'exclude_options':
        args[0] = add_namespace(ns, args[0])
        numkeys = args[1]
        args[2:2 + numkeys] = add_namespace(ns, args[2:2 + numkeys])
    elif before == 'alternate':
        new_args = []
        for i, k in enumerate(args):
            if i % 2 == 0:
                new_args.append(add_namespace(ns, k))
            else:
                new_args.append(k)
        args = new_args
    elif before == 'sort':
        # TODO
        pass
    elif before == 'eval_style':
        numkeys = args[1]
        args[2:2+numkeys] = add_namespace(ns, args[2:2 + numkeys])
    elif before == 'scan_style':
        is_custom_match = False
        for i, a in enumerate(args):
            if isinstance(a, (basestring, bytes, Token)) and str(a).lower() == 'match':
                args[i+1] = add_namespace(ns, args[i + 1])
                is_custom_match = True
                break
        if not is_custom_match:
            args.insert(1, 'match')
            args.insert(2, add_namespace(ns, '*'))

    args.insert(0, command_name)
    return tuple(args)


def response_rm_namespace(ns, command_name, response):
    if not ns or not response:
        return response
    _, after = get_handling(command_name)
    if after == 'all':
        response = rm_namespace(ns, response)
    elif after == 'first':
        response[0] = rm_namespace(ns, response[0])
    elif after == 'second':
        response[1] = rm_namespace(ns, response[1])
    return response


def add_namespace(ns, key):
    if not ns or not key:
        return key
    if isinstance(key, list):
        return [add_namespace(ns, k) for k in key]
    elif isinstance(key, dict):
        return {add_namespace(ns, k): v for k, v in key.items()}
    elif isinstance(key, basestring):
        return '{}{}'.format(ns, key)
    elif isinstance(key, bytes):
        return '{}{}'.format(ns, nativestr(key))
    return key


def rm_namespace(ns, key):
    if not ns:
        return key
    if isinstance(key, list):
        return [rm_namespace(ns, k) for k in key]
    elif isinstance(key, dict):
        return {rm_namespace(ns, k): v for k, v in key.items()}
    elif isinstance(key, (basestring, bytes)):
        return key[len(ns):]
    return key


class StrictRedis(redis.StrictRedis):

    @classmethod
    def from_url(cls, url, db=None, namespace='', **kwargs):
        connection_pool = ConnectionPool.from_url(url, db=db, **kwargs)
        return cls(connection_pool=connection_pool, namespace=namespace)

    def __init__(self, namespace='', *args, **kwargs):
        super(StrictRedis, self).__init__(*args, **kwargs)
        self._namespace = namespace

    def execute_command(self, *args, **options):
        args = args_with_namespace(self._namespace, *args)
        return super(StrictRedis, self).execute_command(*args, **options)

    def parse_response(self, connection, command_name, **options):
        try:
            response = connection.read_response()
        except ResponseError:
            if EMPTY_RESPONSE in options:
                return options[EMPTY_RESPONSE]
            raise
        response = response_rm_namespace(self._namespace, command_name, response)
        if command_name in self.response_callbacks:
            return self.response_callbacks[command_name](response, **options)
        return response

    def pipeline(self, transaction=True, shard_hint=None):
        return Pipeline(
            self.connection_pool,
            self.response_callbacks,
            transaction,
            shard_hint,
            namespace=self._namespace)

    def pubsub(self, **kwargs):
        return PubSub(self.connection_pool, namespace=self._namespace, **kwargs)

    def sort(self, name, start=None, num=None, by=None, get=None,
             desc=False, alpha=False, store=None, groups=False):
        args = [name, by, store]
        name, by, store = add_namespace(self._namespace, args)
        if get:
            if isinstance(get, (basestring, bytes)):
                get = add_namespace(self._namespace, get)
            elif isinstance(get, (list, tuple)):
                get = [add_namespace(self._namespace, i) if i != '#' else i for i in get]
        return super(StrictRedis, self).sort(
            name, start, num, by, get, desc, alpha, store, groups)

    def georadius(self, name, longitude, latitude, radius, unit=None,
                  withdist=False, withcoord=False, withhash=False, count=None,
                  sort=None, store=None, store_dist=None):
        args = [name, store, store_dist]
        name, store, store_dist = add_namespace(self._namespace, args)
        return super(StrictRedis, self).georadius(
            name, longitude, latitude, radius, unit, withdist, withcoord, withhash, count,
            sort, store, store_dist)

    def georadiusbymember(self, name, member, radius, unit=None,
                          withdist=False, withcoord=False, withhash=False,
                          count=None, sort=None, store=None, store_dist=None):
        args = [name, store, store_dist]
        name, store, store_dist = add_namespace(self._namespace, args)
        return super(StrictRedis, self).georadiusbymember(
            name, member, radius, unit, withdist, withcoord, withhash,
            count, sort, store, store_dist)


Redis = StrictRedis


class PubSub(_PubSub):
    def __init__(self, connection_pool, shard_hint=None,
                 ignore_subscribe_messages=False, namespace=''):
        super(PubSub, self).__init__(
            connection_pool, shard_hint, ignore_subscribe_messages)
        self._namespace = namespace

    def execute_command(self, *args, **kwargs):
        args = args_with_namespace(self._namespace, *args)
        return super(PubSub, self).execute_command(*args, **kwargs)

    def handle_message(self, response, ignore_subscribe_messages=False):
        message_type = nativestr(response[0])
        if message_type == 'pmessage':
            response[1] = rm_namespace(self._namespace, response[1])  # pattern
            response[2] = rm_namespace(self._namespace, response[2])  # channel
        elif message_type == 'pong':
            pass
        else:
            response[1] = rm_namespace(self._namespace, response[1])  # channel
        return super(PubSub, self).handle_message(response, ignore_subscribe_messages)


class Pipeline(_Pipeline, StrictRedis):

    def __init__(self, connection_pool, response_callbacks, transaction,
                 shard_hint, namespace=''):
        super(Pipeline, self).__init__(
            connection_pool, response_callbacks, transaction, shard_hint)
        self._namespace = namespace

    def execute_command(self, *args, **kwargs):
        args = args_with_namespace(self._namespace, *args)
        return super(Pipeline, self).execute_command(*args, **kwargs)
