'''
Created on Mar 2, 2016

@author: jiangdu
'''

_city = "New york"
_street = "Someset"


def set_city(value):
    global _city
    _city = value
    _street = "Ok"
    print("vars() =", vars())


def get_city():
    return _city


def get_street():
    return _street


if __name__ == '__main__':
    pass
