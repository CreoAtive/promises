import logging
import time

from promises import Promise

def main():
    start_time = time.time()

    def first_test_promise_executor(resolve, reject):
        time.sleep(5)

        resolve('first promise')

    def second_test_promise_executor(resolve, reject):
        time.sleep(4)

        resolve('second promise')

    def third_test_promise_executor(resolve, reject):
        time.sleep(3)

        resolve('third promise')

    def handleSuccess(name, *args):
        logging.info('{name} resolved after {seconds}, value: {value}'.format(name = name, seconds = time.time() - start_time, value = args))

    def handleFailure(name, *args):
        logging.warning('{name} rejected after {seconds}, reason: {reason}'.format(name = name, seconds = time.time() - start_time, reason = args))

    logging.info('start test')

    first_test_promise = Promise(first_test_promise_executor)

    second_test_promise = Promise(second_test_promise_executor)

    third_test_promise = Promise(third_test_promise_executor)

    all_promise = Promise.all([first_test_promise, second_test_promise, third_test_promise]).then(lambda *args: handleSuccess('all_promise', *args), lambda *args: handleFailure('all_promise', *args))

    race_promise = Promise.race([first_test_promise, second_test_promise, third_test_promise]).then(lambda *args: handleSuccess('race_promise', *args), lambda *args: handleFailure('race_promise', *args))

    logging.info('finish test after {} seconds'.format(time.time() - start_time))

if __name__ == '__main__':
    main()
