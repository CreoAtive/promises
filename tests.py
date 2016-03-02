import logging

logging.basicConfig(level=logging.DEBUG)

logging.getLogger('requests').setLevel(logging.WARNING)

import promises
import requests

import time

def requestPromiseTest():
    def executor(resolve, reject):
        time.sleep(2)

        resolve('foobar')

    def resolve():
        time.sleep(2)

        return 'foobar'

    def handleSuccess(*args):
        logging.info('handleSuccess')

    def handleFailure(*args):
        logging.info('handleFailure: {}'.format(args))

    def finish(*args):
        logging.info('finish')

    first_promise = promises.Promise.resolve(resolve).then(handleSuccess, handleFailure).then(finish)

    def secondPromiseSuccess(*args):
        logging.info('secondPromiseSuccess')

        time.sleep(2)

    def secondPromiseFailure(*args):
        logging.info('secondPromiseFailure {}'.format(args))

    def secondFinish(*args):
        logging.info('secondFinish')

    second_promise = promises.Promise.resolve(first_promise).then(secondPromiseSuccess, secondPromiseFailure).then(secondFinish)

    logging.info('foo')

    third_promise = promises.Promise.race([first_promise, second_promise]).then(lambda *args: logging.info('thirdPromiseSuccess'), lambda *args: logging.warning('thirdPromiseFailure'))

def main():
    requestPromiseTest()

if __name__ == '__main__':
    main()
