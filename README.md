python-ketama
=============

This repo is an implementation example of Ketama consistent hash algorithm with Python, for the Python memcached client. This implementation aims to allow adding nodes of memcached server at runtime.
If you want to understand a bit more about the issues around the consistent hashing, these are some good references:

* [Tom White](http://www.tom-e-white.com/2007/11/consistent-hashing.html)
* [The Simple Magic of Consistent Hashing](http://www.paperplanes.de/2011/12/9/the-magic-of-consistent-hashing.html)

1. **custom_memcached.py**
    * Holds the implementation of a memcache.Client subclass called CustomMemcacheClient.
2. **consistent_hash.py**
    * Holds the implementation of the consistent hash algorithm for ketama. The class is called HashRing and it is an adaptation from [Amir Salihefendic](http://amix.dk/blog/post/19367)
3. **test.py**
    * Holds a simple test script that uses the CustomMemcacheClient. To run the test you just need to make sure that you have the memcache manager and python-memcached client module installed.

To install the memcached and memcached run the following commands:

memcached:
> sudo apt-get install memcached

python-memcached:
> pip install python-memcached

After install Memcached you just need to run the "test.py" on the terminal. If you want to specify the algorithm to test you have to pass it as parameter like this:

To test KETAMA:
> python test.py -k

To test MODULO (the default algorithm used by the original memcache.Client superclass):
> python test.py -m

If you don't specify any argument it will take KETAMA by default.

