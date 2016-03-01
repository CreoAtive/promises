from threading import Thread
from threading import Event

class Deferred(object):

    def __init__(self):
        self._event = Event()
        self._rejected = False
        self._result = None

    def resolve(self, value):
        self._rejected = False
        self._result = value
        self._event.set()

    def reject(self, reason):
        self._rejected = True
        self._result = reason
        self._event.set()

    def promise(self, catch = False):
        promise = Promise(None, self)

        return promise


class Promise(object):

    def __init__(self, resolver = None, deferred = None):
        self._deferred = deferred

        if hasattr(resolver, '__call__'):
            self._deferred = self.resolver(resolver)

    def resolver(self, resolver):
        defer = Deferred()

        def task():
            try:
                resolver(defer.resolve, defer.reject)
            except Exception as e:
                defer.reject(e.message)

        Thread(target = task).start()

        return defer

    def then(self, onFulfilled = None, onRejected = None, catch = False):
        defer = Deferred()

        def task():
            try:
                self._deferred._event.wait()

                result = self._deferred._result

                if self._deferred._rejected:
                    if onRejected:
                        result = onRejected(self._deferred._result)

                    defer.reject(result)
                else:
                    if onFulfilled:
                        result = onFulfilled(self._deferred._result)

                    defer.resolve(result)

            except Exception as e:
                defer.reject(e.message)

        Thread(target = task).start()

        return defer.promise()

    def catch(self, onRejected):
        return self.then(None, onRejected, True)

    def wait(self):
        self._deferred._event.wait()

    @staticmethod
    def all(*args):
        for promise in args:
            promise.wait()
