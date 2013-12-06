import random
import string
import re
import memcache
from consistent_hash import HashRing

class CustomMemcacheClient(memcache.Client):
    """ A memcache subclass. It currently allows you to add a new host at run
    time.
    """
    available_algorithms = ['ketama', 'modulo']
    hash_algorithm_index = 0

    def __init__(self, hash_algorithm='ketama', *args, **kwargs):
        super(CustomMemcacheClient, self).__init__(*args, **kwargs)

        if hash_algorithm in self.available_algorithms:
            self.hash_algorithm_index = self.available_algorithms.index(
                hash_algorithm)

            if hash_algorithm == 'ketama':
                self.consistent_hash_manager = HashRing(nodes=self.servers)
            else:
                self.consistent_hash_manager = None
        else:
            raise Exception(
                "The algorithm \"%s\" is not implemented for this client. The "
                "options are \"%s\""
                "" % (hash_algorithm, " or ".join(self.available_algorithms))
            )

    def _get_server(self, key):
        """ Returns the most likely server to hold the key
        """

        if self.hash_algorithm  == 'ketama':
            """ Basic concept of the Implementation of ketama algorithm
            e.g. ring = {100:server1, 110:server2, 120:server3, 140:server4}
            If the hash of the current key is 105, it server will be the next
            bigger integer in the ring which is 110 (server2)
            If a server is added on position 108 the key will be now allocated
            to it and not to server 110. Otherwise if the server on position
            110 is removed the key will now belong to de server 120.
            If there's no bigger integer position in the ring then the hash of
            the key, it will take the first server from the ring.
            """
            # The variable "servers" is the list of the servers in the ring
            # starting from the next bigger integer to the hash of the key,
            # till it finds the one that holds the key
            servers_generator = self.consistent_hash_manager.get_nodes(key)
            for server in servers_generator:
                if server.connect():
                    #print server.address[1]
                    return server, key
            return None, None

        else:
            return super(CustomMemcacheClient, self)._get_server(key)

    def add_server(self, server):
        """ Adds a host at runtime to client
        """

        # Uncomment this to protect the Client from adding a server in case
        # there's no reliable consistent hash algorithm such as MODULO
        """
        if not self.consistent_hash_manager:
            raise Exception("The current consistent hash algorithm (\"%s\") is"
                            " not reliable for adding a new server"
                            "" % self.hash_algorithm)
        """

        # Create a new host entry
        server = memcache._Host(
            server, self.debug, dead_retry=self.dead_retry,
            socket_timeout=self.socket_timeout,
            flush_on_reconnect=self.flush_on_reconnect
        )
        # Add this to our server choices 
        self.servers.append(server)

        """This for statement will ensure that a server with a bigger weight
        will have more copies into the buckets increasing it's probability to
        be retrieved.
        """
        for i in range(server.weight):
            self.buckets.append(server)

        # Adds this node to the circle
        if self.consistent_hash_manager:
            self.consistent_hash_manager.add_node(server)

    @property
    def hash_algorithm(self):
        return self.available_algorithms[self.hash_algorithm_index]
