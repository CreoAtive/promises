import logging
import json

logging.basicConfig(level=logging.DEBUG)

logging.getLogger('requests').setLevel(logging.WARNING)

from threading import Thread
from threading import Event

promise_counter = 0

class Promise(object):

    def __init__(self, resolver = None, deferred = None, name = ''):
        global promise_counter

        self._name = name
        self._event = Event()
        self._rejected = False
        self._result = None
        self._id = promise_counter

        promise_counter = promise_counter + 1

        if deferred:
            self._deferred = deferred
        else:
            self._deferred = self.resolver(resolver)

    def resolver(self, resolver):
        def deferredTask():
            try:
                resolver(self.resolve, self.reject)
            except Exception as e:
                self.reject(e.message)

        #Thread(target = deferredTask).start()
        deferredTask()

        return self

    def resolve(self, value):
        #logging.info('resolve: {}'.format(value))

        self._rejected = False
        self._result = value
        self._event.set()

    def reject(self, reason):
        #logging.info('reject: {}'.format(reason))

        self._rejected = True
        self._result = reason
        self._event.set()

    def toJson(self):
        return {
            'name': self._name,
            'result': self._result,
            'rejected': self._rejected
        }

    def then(self, onFulfilled = None, onRejected = None, name = ''):
        promise = self.__class__(None, self, name)

        #self._deferred._event.wait()

        value = self._result

        #logging.info('then: {0}, {1}'.format(result, self._deferred._rejected))

        #logging.info('self - id: {id}, result: {result}, rejected: {rejected}'.format(id = self._id, result = self._result, rejected = self._rejected))

        try:
            if self._rejected:
                # the current promise has been rejected
                # all following onFulfilled methods will be skipped
                if onRejected:
                    # there is a method for handling onRejected
                    # call method with current value as argument
                    result = onRejected(self._result)

                    if result != None:
                        # the result is not none
                        # set new promise to resolve to result value
                        promise.resolve(result)
                    else:
                        # the result is none, nothing was returned
                        # set new promise to resolve to current value
                        promise.resolve(self._result)
                else:
                    # there is no method for handling onRejected
                    # set new promise to reject with current value
                    promise.reject(self._result)
            else:
                # the current promise has not been rejected
                # all following onRejected methods will be skipped
                if onFulfilled:
                    # there is a method for handling onFulfilled
                    # call method with current value as argument
                    result = onFulfilled(self._result)

                    if result != None:
                        # the result is not none
                        # set new promise to resolve to result value
                        promise.resolve(result)
                    else:
                        # the result is none, nothing was returned
                        # set new promise to resolve to current value
                        promise.resolve(self._result)
                else:
                    # there is no method for handling onFulfilled
                    # set new promise to resolve to current value
                    promise.resolve(self._result)
        except Exception as e:
            # there has been an error along the way
            # set new promise to reject with error message
            promise.reject(e.message)

        #logging.info('New Promise: {}'.format(json.dumps(promise.toJson())))

        return promise

        try:
            if self._rejected:
                if onRejected:
                    logging.info(value)
                    result = onRejected(value)

                    if result:
                        promise.resolve(result)
                    else:
                        promise.resolve(value)
                else:
                    promise.reject(value)
            else:
                if onFulfilled:
                    result = onFulfilled(value)

                    if result:
                        promise.resolve(result)
                    else:
                        promise.resolve(value)
                else:
                    promise.resolve(value)
        except Exception as e:
            promise.reject(e.message)

        return promise

    def catch(self, onRejected):
        #logging.info('catch')

        return self.then(None, onRejected, True)
