
from Global_Packages import packages
import time


def filter_method(lock, userID, docID, data, result):
    """ this time we will find pagereadtime event rather than read event."""
    dicts = filter(lambda x: x.get("event_type", "") == "pagereadtime", data)
    for dict in dicts:
        lock.acquire()
        result[dict.get("visitor_uuid")] = result.get(dict.get("visitor_uuid"), 0) + dict.get("event_readtime")
        lock.release()


def reader_list(filename):
    print("Start analyzing data...")
    start_time = time.time()
    result = feed_json_threadpool.json_threadpooling(0, 0, filename, filter_method)
    print("\nAnalyzing data duration(s):", time.time() - start_time)
    start_time = time.time()
    string_display = "Task4:\n"
    if len(result) == 0:
        string_display = string_display + "Not found any readers in the file" + filename
    top_10 = topn.top_N(10, result)
    i = top_10.qsize()
    while not top_10.empty():
        temp = top_10.get()
        string_display = string_display + ("Ranking:" + str(i) + "\tUser:" + temp[1] + "\tReading time (mins):" + str(temp[0]/60000))
        string_display = string_display + "\n"
        i = i - 1
    print(string_display)
    # usually the sorting time will be less than 1 second
    print("Sorting data duration(s):", time.time() - start_time)
    return string_display


if __name__ == "__main__":
    reader_list(r"/home/salman/Documents/IP-CW2_new/IP/sample_3m_lines.json")
