#import hashlib.md5 as md5
from hashlib import md5

"""
Author: Amir Salihefendic
Source: http://amix.dk/blog/post/19367
Adapted for: Mauricio Domingos dos Santos Junior
"""


class HashRing(object):

    def __init__(self, nodes=None, replicas=3):
        """Manages a hash ring.

        `nodes` is a list of objects that have a proper __str__ representation.
        `replicas` indicates how many virtual points should be used pr. node,
        replicas are required to improve the distribution.
        """
        self.replicas = replicas

        self.ring = dict()
        self._sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        """Adds a `node` to the hash ring (including a number of replicas).
        """
        for i in xrange(0, self.replicas):
            """This will ensure that a server with a bigger weight will have
            more copies into the ring increasing it's probability to be retrieved.
            """
            for x in range(0, node.weight):
                key = self.gen_key(
                    '%s:%s:%s:%s' % (node.address[0],
                    node.address[1], i, node.weight)
                )

                if key not in self.ring:
                    self.ring[key] = node
                    self._sorted_keys.append(key)

        self._sorted_keys.sort()

    def remove_node(self, node):
        """Removes `node` from the hash ring and its replicas.
        """
        for i in xrange(0, self.replicas):
            for x in range(node.weight):
                key = self.gen_key(
                    '%s:%s:%s:%s' % (node.address[0],
                    node.address[1], i, node.weight)
                )

                if key in self.ring:
                    del self.ring[key]
                    self._sorted_keys.remove(key)

    def get_node(self, string_key):
        """
        Given a string key a corresponding node in the hash ring is returned.

        If the hash ring is empty, `None` is returned.
        """
        return self.get_node_pos(string_key)[0]

    def get_node_pos(self, string_key):
        """Given a string key a corresponding node in the hash ring is returned
        along with it's position in the ring.

        If the hash ring is empty, (`None`, `None`) is returned.
        """
        if not self.ring:
            return None, None

        key = self.gen_key(string_key)

        nodes = self._sorted_keys
        for i in xrange(0, len(nodes)):
            node = nodes[i]
            if key <= node:
                return self.ring[node], i

        return self.ring[nodes[0]], 0

    def get_nodes(self, string_key):
        """Given a string key it returns the nodes as a generator that can hold
        the key.

        The generator is never ending and iterates through the ring
        starting at the correct position.
        """
        if not self.ring:
            yield None, None

        node, pos = self.get_node_pos(string_key)
        for key in self._sorted_keys[pos:]:
            if key in self.ring:
                yield self.ring[key]

        for key in self._sorted_keys[:pos]:
            if key in self.ring:
                yield self.ring[key]

    @staticmethod
    def gen_key(key):
        """Given a string key it returns a long value,
        this long value represents a place on the hash ring.

        md5 is currently used because it mixes well.
        """
        m = md5()
        m.update(key)
        return long(m.hexdigest(), 16)
