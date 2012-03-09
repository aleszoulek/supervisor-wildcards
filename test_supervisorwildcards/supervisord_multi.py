#!/usr/bin/env python

import time

import test_dashvisor


def main():
    try:
        test_dashvisor.setUp()
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print 'stoping..'
        test_dashvisor.tearDown()
        print 'stoped'


if __name__ == '__main__':
    main()
