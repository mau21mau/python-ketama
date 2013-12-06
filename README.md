python-ketama
=============

Implementation of Ketama consistent hash algorithm with Python

1. **custom_memcached.py**
⋅⋅* Holds the implementation of a memcache.Client subclass called CustomMemcacheClient.
2. **consistent_hash.py**
⋅⋅* Holds the implementation of the consistent hash algorithm for ketama. The class is called HashRing and it is an adaptation from [Amir Salihefendic](http://amix.dk/blog/post/19367)
3. **test.py**
..* Holds a simple test script that uses the CustomMemcacheClient. To run the test you just need to make sure that you have the memcache manager and python-memcached client module installed.

To install the memcached and python-memcached run the following commands:

> sudo apt-get install memcached
> pip install python-memcached

After install Memcached you just need to run the "test.py" on the terminal. If you want to specify the algorithm to test you have to pass it as parameter like this:

To test KETAMA:
> python test.py -k

To test MODULO (the default algorithm used by the original memcache.Client superclass):
> python test.py -m

If you don't specify any argument it will take KETAMA by default.

