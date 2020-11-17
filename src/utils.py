from datetime import date
import calendar
import logging

def custom_logger():
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', 
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S%z')

def recurGet_core(d, ks):
    head, *tail = ks
    return recurGet(d.get(head, {}), tail) if tail else d.get(head)

def recurGet(d, ks):
    result = recurGet_core(d, ks)
    if result == '':
        result = None
    return result

def dt2ts(dt, addone=False):
    """Converts a datetime object to UTC timestamp

    naive datetime will be considered UTC.

    optional: add 1 to timestamp
    """
    timestamp = calendar.timegm(dt.utctimetuple())
    if addone:
        timestamp = timestamp + 1
    return timestamp
