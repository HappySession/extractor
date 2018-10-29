import happy
import happy.forecast.gfs
import happy.forecast.ww3
import sys
import schedule
import time
import os
import logging


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.info('Started')

    #schedule.every().day.at("09:48").do(happy.forecast.ww3.run, offset=0)
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
    #gfs.run("00", "25")
    happy.forecast.ww3.run(0)

    logging.info('Finished')


if __name__ == '__main__':
    main()
