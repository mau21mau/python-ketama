import random
import string
from sys import argv
from custom_memcached import MemcacheClient

def random_key(size):
    """ Generates a random key
    """
    return ''.join(random.choice(string.letters) for _ in range(size))


def run_consistent_hash_test(client_obj):
    # We have 500 keys to split across our servers
    keys = [random_key(100) for i in range(500)]

    print(
        "\n/////////// CONSISTENT HASH ALGORITHM \"%s\" //////////////"
        "" % client_obj.hash_algorithm.upper()
    )

    print("\n->Starting with %s servers:" % len(client_obj.servers))
    str_servers = ""
    for server in client_obj.servers:
        str_servers += "%s:%s, " % (server.address[0], server.address[1])
    print("******************************************************************")
    print(str_servers)
    print("******************************************************************")

    # Clear all previous keys from memcache
    client_obj.flush_all()

    # Distribute the keys over the servers
    for key in keys:
        client_obj.set(key, 1)

    print(
        "\n%d keys distributed for %d server(s)\n"
        "" % (len(keys), len(client_obj.servers))
    )

    # Check how many keys come back
    valid_keys = client_obj.get_multi(keys)
    print(
        "%s percent of keys matched, before adding extra servers.\n" \
        "" %((len(valid_keys) / float(len(keys))) * 100)
    )

    # Add 5 new extra servers
    interval_extra_servers = range(19, 24)
    extra_servers = ['127.0.0.1:112%d' % i for i in interval_extra_servers]
    for server in extra_servers:
        client_obj.add_server(server)

    # Check how many keys come back after adding the extra servers
    valid_keys = client_obj.get_multi(keys)
    print (
        "Added %d new server(s).\n%s percent of keys still matched" \
        "" % (len(interval_extra_servers),
        (len(valid_keys) / float(len(keys))) * 100)
    )

    print("\n***************************************************************"
          "****\n")

if __name__ == '__main__':
    # We have 8 running memcached servers
    algorithm = "ketama"
    
    
    if "-k" in argv or "-m" in argv:
        if argv[1] == "-m":
            algorithm = "modulo"
    else:
        print "To specify the algorithm to test pass \"-k\" for Ketama or \"-m\"for Modulo."
        print "Otherwise it will run the test with the default algorithm \"Ketama\"."

    interval_servers = range(11, 19)
    servers = ['127.0.0.1:112%d' % i for i in interval_servers]
    """
    Init our subclass. The hash_algorithm paramether can be "modulo"<-
    (default) or "ketama" (the new one).
    """
    client = MemcacheClient(servers=servers, hash_algorithm=algorithm)
    run_consistent_hash_test(client)
