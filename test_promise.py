import logging
import time

from promises import Promise

def main():
    start_time = time.time()

    def first_test_promise_executor(resolve, reject):
        time.sleep(2)

        resolve('first promise')

    def second_test_promise_executor(resolve, reject):
        time.sleep(4)

        resolve('second promise')

    def handleSuccess(name):
        logging.info('{name} resolved after {seconds}'.format(name = name, seconds = time.time() - start_time))

    def handleFailure(name):
        logging.warning('{name} rejected after {seconds}'.format(name = name, seconds = time.time() - start_time))

    logging.info('start test')

    first_test_promise = Promise(first_test_promise_executor)

    second_test_promise = Promise(second_test_promise_executor)

    third_test_promise = Promise.all([first_test_promise, second_test_promise]).then(lambda *args: handleSuccess('third_test_promise'), lambda *args: handleFailure('third_test_promise'))

    fourth_test_promise = Promise.race([first_test_promise, second_test_promise]).then(lambda *args: handleSuccess('fourth_test_promise'), lambda *args: handleFailure('fourth_test_promise'))

    logging.info('finish test after {} seconds'.format(time.time() - start_time))

if __name__ == '__main__':
    main()
