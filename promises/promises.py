import traceback
import logging
import json

logging.basicConfig(level=logging.DEBUG)

logging.getLogger('requests').setLevel(logging.WARNING)

from threading import Thread
from threading import Event

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, group = None, target = None, *args, **kwargs):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()
        self._target = target
        self._args = args

    def run(self):
        if not self.isStopped():
            pass

    def stop(self):
        self._stop.set()

    def isStopped(self):
        return self._stop.isSet()

class Promise(object):

    def __init__(self, resolver = None):
        self._event = Event()
        self._rejected = False
        self._result = None

        if resolver:
            self.resolver(resolver)

    def resolver(self, resolver):
        def deferredTask():
            try:
                resolver(self._resolve, self._reject)
            except Exception as e:
                self._reject(e.message)

                traceback.print_exc()

        Thread(target = deferredTask).start()

    def _resolve(self, value):
        # set promise to resolved
        # set result to value
        self._rejected = False
        self._result = value
        self._event.set()

    def _reject(self, reason):
        # set promise to rejected
        # set result to reason
        self._rejected = True
        self._result = reason
        self._event.set()

    def wait(self):
        return self._event.wait()

    def result(self):
        return self._result

    def isRejected(self):
        return self._rejected

    def toJson(self):
        # return a dict containing the current state of the promise
        return {
            'result': self._result,
            'rejected': self._rejected
        }

    def then(self, onFulfilled = None, onRejected = None):
        promise = self.__class__()
        catch = False

        if not onFulfilled and onRejected:
            catch = True

        def deferredTask():
            try:
                self.wait()

                if self._rejected:
                    # the current promise has been rejected
                    # all following onFulfilled methods will be skipped
                    if onRejected:
                        # there is a method for handling onRejected
                        # call method with current value as argument
                        result = onRejected(self.result())

                        if result != None:
                            # the result is not none
                            if catch:
                                # set new promise to resolve to result value
                                promise._resolve(result)
                            else:
                                # this is not an attempt to catch and resolve
                                # set new promise to reject with current value
                                promise._reject(result)
                        else:
                            # the result is none, nothing was returned
                            if catch:
                                # set new promise to resolve to current value
                                promise._resolve(self.result())
                            else:
                                # this is not an attempt to catch and resolve
                                # set new promise to reject with current value
                                promise._reject(self.result())
                    else:
                        # there is no method for handling onRejected
                        # set new promise to reject with current value
                        promise._reject(self.result())
                else:
                    # the current promise has not been rejected
                    # all following onRejected methods will be skipped
                    if onFulfilled:
                        # there is a method for handling onFulfilled
                        # call method with current value as argument
                        result = onFulfilled(self.result())

                        if result != None:
                            # the result is not none
                            # set new promise to resolve to result value
                            promise._resolve(result)
                        else:
                            # the result is none, nothing was returned
                            # set new promise to resolve to current value
                            promise._resolve(self.result())
                    else:
                        # there is no method for handling onFulfilled
                        # set new promise to resolve to current value
                        promise._resolve(self.result())
            except Exception as e:
                # there has been an error along the way
                # set new promise to reject with error message
                promise._reject(e.message)

                traceback.print_exc()

        Thread(target = deferredTask).start()
        #deferredTask()

        return promise

    def catch(self, onRejected):
        # sugar for then(None, onRejected)
        return self.then(None, onRejected)

    @staticmethod
    def resolve(value):
        promise = Promise()

        def deferredTask():
            if isinstance(value, Promise):
                value.wait()

                if value._rejected:
                    promise._reject(value._result)
                else:
                    promise._resolve(value._result)
            elif hasattr(value, '__call__'):
                # the value is callable
                try:
                    result = value()
                except Exception as e:
                    # the called method raises an Exception
                    # reject promise
                    promise._reject(e.message)

                    traceback.print_exc()
                else:
                    # resolve promise with return value from method
                    promise._resolve(result)
            else:
                # resolve promise with value
                promise._resolve(value)

        Thread(target = deferredTask).start()

        return promise

    @staticmethod
    def reject(reason):
        promise = Promise()

        promise._reject(reason)

        return promise

    @staticmethod
    def all(promises):
        new_promise = Promise()
        new_promise_results = []

        def deferredTask():
            for index, promise in enumerate(promises):
                promise.wait()

                if promise.isRejected():
                    new_promise._reject(promise.result())

                    break
                else:
                    new_promise_results.append(promise.result())

            if not new_promise.isRejected():
                new_promise._resolve(new_promise_results)

        Thread(target = deferredTask).start()

        return new_promise

    @staticmethod
    def race(promises):
        threads = []
        new_promise = Promise()

        def deferredTask(promise):
            promise.wait()

            if promise.isRejected():
                new_promise._reject(promise.result())
            else:
                new_promise._resolve(promise.result())

        for index, promise in enumerate(promises):
            threads.append(Thread(target = deferredTask, args = (promise, )).start())

        return new_promise
