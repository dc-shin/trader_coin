from operator import index
from Collector import *
from datetime import timezone, datetime

def main():
    print('######## Collector app started ########')

    end_time = datetime(2022, 2, 1, tzinfo=timezone.utc).timestamp()
    Collector.instance().collect_all_candle(5, end_time)

if __name__ == '__main__':
	main()
