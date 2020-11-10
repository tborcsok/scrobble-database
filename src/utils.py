from datetime import date
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
