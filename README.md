# python-promises

A simple package to emulate JavaScript Promise() behaviour.

The Promise object is used for deferred and asynchronous computations. A Promise represents an operation that hasn't completed yet, but is expected in the future.

## usage

Create a new promise instance by passing a method with two parameters (resolve and reject). Once the method is executed you can either resolve the promise by passing a value to to the resolve method or reject it by passing a reason to the reject method.

**example**

```python
def executor(resolve, reject):
    if 1 == 2:
        resolve(3)
    else:
        reject('This does not work')

promise = Promise(executor)
```

## chaining

You can chain promises by appending a **.then()** method. That way you can define onFulfilled and onRejected methods, which get called based on the resolution of the previous promise.

**example**

```python
def onFulfilledHandler(value):
    print 'The promise was fulfilled and is {value}'.format(value = value)

def onRejectedHandler(reason):
    print 'The promise was rejected because of {reason}'.format(reason = reason)

promise.then(onFulfilledHandler, onRejectedHandler)
```
