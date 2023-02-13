# Task 2 uses document ID
import os
import pandas as pd
from Global_Packages import packages 


def filter_method(lock, userID, docID, data, result):
    dicts = filter(lambda x: x.get("event_type", "") == "read" and x.get("subject_doc_id", "") == docID, data)
    for dict in dicts:
        lock.acquire()
        result[dict.get("visitor_country")] = result.get(dict.get("visitor_country"), 0) + 1
        lock.release()


@packages.plot_hist
@packages.exception
def country_input(docID, filename):
    return feed_json_threadpool.json_threadpooling(0, docID, filename, filter_method)


@packages.plot_hist
@packages.exception
def continent_input(docID, filename):
    table = pd.read_csv(os.path.abspath(r"Task2/all.csv"))
    country_continent = table.set_index('alpha-2')['region'].to_dict()
    outputs = feed_json_threadpool.json_threadpooling(0, docID, filename, filter_method)
    new_outputs = {}
    # replace the country to continent
    for x in outputs:
        new_outputs[country_continent.get(x)] = outputs.get(x)
    del outputs
    return new_outputs


if __name__ == "__main__":
    continent_input("140225235449-a1029c9a9b6b2efadaecb69aab7e4dbf",
                      r"/home/salman/Documents/IP-CW2_new/IP/sample_3m_lines.json")
