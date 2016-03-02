# python-promises

A simple package to emulate JavaScript Promise() behaviour.

The Promise object is used for deferred and asynchronous computations. A Promise represents an operation that hasn't completed yet, but is expected in the future.
[More at [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)]

## Usage

Create a new promise instance by passing a method with two parameters (resolve and reject). Once the method is executed you can either resolve the promise by passing a value to to the resolve method or reject it by passing a reason to the reject method.

**Example**

```python
from promises import Promise

def executor(resolve, reject):
    if True:
        resolve('This was awesome')
    else:
        reject('This does not work')

promise = Promise(executor)

# will execute the executor method and resolve to either "This was awesome" or "This does not work"
```

## Chaining

### .then(onFulfilled, onRejected)

You can chain promises by appending **.then()**. That way you can define onFulfilled and onRejected methods, which get called based on the resolution of the previous promise.

**Example**

```python
def onFulfilledHandler(value):
    print 'The promise was fulfilled and is "{value}"'.format(value = value)

def onRejectedHandler(reason):
    print 'The promise was rejected because of {reason}'.format(reason = reason)

promise.then(onFulfilledHandler, onRejectedHandler)

# will print: The promise was fulfilled and is "This was awesome"
```

### .catch(onRejected)

You can catch rejections by appending **.catch()** to the promise and pass an onRejected method. This way you can catch all previous rejections and resolve the promise so the following promise's onFulfilled method will get called.

**Example**

```python
def onFinishHandler(value):
    print 'The promise chain has finished'

promise.catch(onRejectedHandler).then(onFinishHandler)

# will print "The promise chain has finished"
```

## Methods

### .resolve(value)

### .reject(reason)

### .all(iterable)

Returns a promise that either resolves when all of the promises in the iterable argument have resolved or rejects as soon as one of the promises in the iterable argument rejects. If the returned promise resolves, it is resolved with an array of the values from the resolved promises in the iterable. If the returned promise rejects, it is rejected with the reason from the promise in the iterable that rejected. This method can be useful for aggregating results of multiple promises together.

**Example**
```python

promise_a = Promise.resolve('promise_a')

promise_b = Promise.reject('promise_b')

promise_c = Promise.all([promise_a, promise_b])

promise_d = Promise.all([promise_a])

# will yield in a rejected promise_c with the reason "promise_b"
# will yield in a resolved promise_d with the value "promise_a"
```

### .race(iterable)

Returns a promise that resolves or rejects as soon as one of the promises in the iterable resolves or rejects, with the value or reason from that promise.
