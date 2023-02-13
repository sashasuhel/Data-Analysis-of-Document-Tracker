
import itertools
import sys
import threading
import time
from functools import wraps

import graphviz


def alsoLikesGraph(func):
    @wraps(func)
    def wrapping(*args, **kwargs):
        outputs = None

        def loading():
            loading = itertools.cycle(['.', '.', '.', '.'])
            while outputs is None:
                sys.stdout.write(next(loading))
                sys.stdout.flush()
                sys.stdout.write('\b')
                time.sleep(0.1)

        print("Start analyzing data...", end="")
        loading_func = threading.Thread(target=loading)
        loading_func.start()
        start_time = time.time()
        outputs = func(*args, **kwargs)
        loading_func.join()
        print("\nAnalyzing data duration(s):", time.time() - start_time)
        # generates a .dot source file, and a .ps result file
        w = graphviz.Digraph(filename='Also_likes.dot', format="ps")
        start_time = time.time()
        for x in outputs:
            # if given userID is one of the keys
            if x == args[0]:
                # generate a reader node first
                w.node(x[-4:], shape='box', style='filled', fillcolor='green', fontcolor='black')
                for d in outputs.get(x):
                    # find the given docID and create an edge between given userID and docID nodes
                    if d == args[1]:
                        w.node(d[-4:], style='filled', fillcolor='green', fontcolor='black')
                        w.edge(x[-4:], d[-4:])
            else:
                # generate all reader and doc nodes, and linked each other
                w.node(x[-4:], shape='box')
                for d in outputs.get(x):
                    if d == args[1]:
                        w.node(d[-4:], style='filled', fillcolor='green', fontcolor='black')
                    else:
                        w.node(d[-4:])
                    w.edge(x[-4:], d[-4:])

        w.view()
        print("Plotting data duration(s):", time.time() - start_time)

    return wrapping


if __name__ == "__main__":
    graphviz.render('dot', 'pdf',
                    r"/home/salman/Documents/IP-CW2_new/IP/Also_likes.dot")
