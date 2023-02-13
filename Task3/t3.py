
# Task 3, shows the raw useragent string and extract the browser from it.

from Global_Packages import packages
import re


def extract_browser(string):
    """
    Take idea from these two websites. The basic idea is there is regular pattern that which browser will pretend as
    what browser. For example, Chrome usually pretend it as Safari, so if there is a "Chrome" substring in the useragent,
    the browser probably is Chrome rather than Safari. However, we can put Safari under the Chrome, because there is no
    other browser pretend itself as Safari anymore, So, if there is "Safari" substring and no "Chrome" substring, we
    could say the browser is Safari.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent
    https://stackoverflow.com/questions/9847580/how-to-detect-safari-chrome-ie-firefox-and-opera-browser

    Parameters:
        string - this is the raw useragent string

    Returns:
        what kind of the browser in the useragent
    """

    Opera = re.compile('Opera')
    Chrome = re.compile('Chrome')
    Chromium = re.compile('Chromium')
    Safari = re.compile('Safari')
    Firefox = re.compile('Firefox')
    IE = re.compile('MSIE')
    Seamonkey = re.compile('Seamonkey')

    if Opera.search(string):
        answer = "Opera"
    elif Chrome.search(string):
        answer = "Chrome"
    elif Chromium.search(string):
        answer = "Chromium"
    elif Safari.search(string):
        answer = "Safari"
    elif Firefox.search(string):
        answer = "Firefox"
    elif IE.search(string):
        answer = "IE"
    elif Seamonkey.search(string):
        answer = "Seamonkey"
    else:
        answer = "Other"
    return answer


def filter_method_all(lock, userID, docID, data, result):
    # count different types of useragent.
    dicts = filter(lambda x: x.get("event_type", "") == "read", data)
    for dic in dicts:
        lock.acquire()
        result[dic.get("visitor_useragent")] = result.get(dic.get("visitor_useragent"), 0) + 1
        lock.release()


def filter_method(lock, userID, docID, data, result):
    # just like filter_method_all did, except we apply extract_browser function here.
    dicts = filter(lambda x: x.get("event_type", "") == "read", data)
    for dic in dicts:
        lock.acquire()
        result[extract_browser(dic.get("visitor_useragent"))] = \
            result.get(extract_browser(dic.get("visitor_useragent")), 0) + 1
        lock.release()


@packages.plot_hist
@packages.exception
def input_total_browser(filename):
    """
    Time complexity: N
    Space complexity: N
    """
    return feed_json_threadpool.json_threadpooling(0, 0, filename, filter_method_all)


@packages.plot_hist
@packages.exception
def input_browser(filename):
    return feed_json_threadpool.json_threadpooling(0, 0, filename, filter_method)


if __name__ == "__main__":
    input_browser(
        r"/home/salman/Documents/IP-CW2_new/IP/issuu_cw2.json")
