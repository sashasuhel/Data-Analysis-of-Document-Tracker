
import os
import re
import json
import sys
from functools import wraps
import itertools
import threading
import time
from matplotlib import pyplot as plt
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import PriorityQueue


################################################################################# Block 1: FEED THREADPOOL #########################################################################################
def json_threadpooling(userID, docID, filename, filter_method):
    # UserID and docID arent required everywhere but best to be used along side filter method 

    file_exists = os.path.isfile(filename)
    if file_exists:
        pattern = re.compile(r'\.json\Z')
        t = pattern.search(filename)
        if t is not None:
            filename = os.path.abspath(filename)
            result = {}
            for chunk in blocks(filename):
                threadpooling(userID, docID, chunk, filter_method, result)
            return result
        else:
            print("Wrong file type:", filename, "not a json file.")
            sys.exit(1)
    else:
        print("Cannot find file", filename, "because it does not exist.")
        sys.exit(1)

################################################################################# Block 2: FILE IO #########################################################################################
def blocks(filename, size=100000):
    count = 0
    chunk = []
    try:
        file = open(filename, 'r', encoding='utf8')
        for line in file.readlines():
            count = count + 1
            chunk.append(json.loads(line))
            if count == size:
                yield chunk
                count = 0
                chunk = []
        if len(chunk) != 0:
            yield chunk
    except IOError:
        print("\nCannot open the file ", filename)
        sys.exit(1)
    finally:
        file.close()
################################################################################# Block 3: NOTHING EXCEPTION #########################################################################################

class Salty_Exception(Exception):
    # checks the length of name

    def __str__(self):
        return "Nothing found in this file!"


def exception(func):
    @wraps(func)
    def wrapping(*args, **kwargs):
        outputs = {}
        try:
            outputs = func(*args, **kwargs)
            if len(outputs) == 0:
                raise Salty_Exception
        except Salty_Exception as e:
            print("\n", e, args[-1])
            sys.exit(1)
        finally:
            return outputs

    return wrapping
################################################################################# Block 4: PLOT BARCHART #########################################################################################

def plot_hist(func):
# plots histogram
    @wraps(func)
    def wrapping(*args, **kwargs):
        outputs = None

       # to start running a new thread
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
        # stop loading
        loading_func.join()
        if len(outputs) != 0:
            plt.figure(figsize=(12, 10), dpi=300)
            plt.bar(list(x[0:20] for x in list(outputs.keys())), list(outputs.values()), 0.6, align='center')
            plt.title(func.__name__)
            print("\nAnalyzing data duration(s):", time.time() - start_time)

            start_time = time.time()
            plt.show()
            print("Plotting data duration(s):", time.time() - start_time)

    return wrapping
################################################################################# Block 5: THREADPOOL #########################################################################################

def threadpooling(userID, docID, dataset, func, result):
   # Due to if the thread has to write into the result dictionary, it has to get the lock first. So, the number of worker
   # cannot be too many, otherwise the competition will slow down the speed.

    remain = len(dataset) % 8
    # when initialize the thread pool, creat a lock. the thread has to get this lock first and then can write the result
    lock = threading.RLock()
    with ThreadPoolExecutor() as executor:
        if remain == 0:
            # creat args iterator
            args = ((lock, userID, docID, dataset[i:i + len(dataset) // 8], result)
                    for i in range(0, len(dataset), len(dataset) // 8))
            executor.map(lambda f: func(*f), args)
        else:
            executor.submit(lambda f: func(*f), [lock, userID, docID, dataset, result])
################################################################################# BLock 6: TOPN #########################################################################################
def top_N(n, result):

    top_n = PriorityQueue(n)
    for x in result:
        if not top_n.full():
            # can add to the queue directly
            top_n.put([result.get(x), x])
        else:
            # compare the new one with the smallest one in the queue
            temp = top_n.get()
            # if greater, then we can replace it with the new one
            if result.get(x) > temp[0]:
                top_n.put([result.get(x), x])
            # if smaller or equal, then put it back
            else:
                top_n.put(temp)
    return top_n
