import logging

logging.basicConfig(level=logging.DEBUG)

logging.getLogger('requests').setLevel(logging.WARNING)

import promises
import requests

import time

def requestPromiseTest():
    def makeRequest(resolve, reject):
        logging.info('makeRequest')

        #time.sleep(2)

        #resolve('foobar')

        r = requests.get('http://jsonplaceholder.typicode.com/posts')

        if r.status_code == 200:
            resolve(r)
        else:
            reject(r.status_code)

    def handleSuccess(response):
        logging.info('handleSuccess')

        return response.json()

    def handleFailure(reason):
        logging.info('handleFailure: {}'.format(reason))

    def printData(data):
        logging.info('printData: {}'.format(data))

    def finish(*args):
        logging.info('finish: {}'.format(args))

    promise = promises.Promise(makeRequest, None, 'Original').then(handleSuccess, None, 'handleSuccess').then(printData, None, 'printData').then(None, handleFailure, 'handleFailure').then(finish, None, 'finish')

    print 'foo'

def main():
    requestPromiseTest()

if __name__ == '__main__':
    main()
