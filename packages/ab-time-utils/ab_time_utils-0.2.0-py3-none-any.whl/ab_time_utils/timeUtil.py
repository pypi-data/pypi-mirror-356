import calendar
import datetime
import time


class timeUtil:

    SOURCE_1 = '%Y-%m-%d %H:%M:%S'
    SOURCE_2 = '%Y%m%d'
    SOURCE_3 = '%Y-%m-%d'
    SOURCE_4 = '%Y%m%d%H%M%S'
    SOURCE_5 = '%Y/%m/%d'
    SOURCE_6 = '%H:%M'
    SOURCE_7 = '%H'
    SOURCE_8 = '%M'
    SOURCE_9 = '%Y'  # 年
    SOURCE_10 = '%m'  # 月
    SOURCE_11 = '%d'  # 日
    SOURCE_12 = '%H:%M:%S'

    # 获取当前日期的时间戳：13位 #
    @staticmethod
    def getCurrentTemp13():
        return int(round(time.time() * 1000))

    @staticmethod
    def stempToTime(stemp, str):
        dateArray = datetime.datetime.utcfromtimestamp(stemp)
        return dateArray.strftime(str)

    # 日期字符串转时间戳
    @staticmethod
    def dateTimeStrToStamp(dateTimeStr, fmtStr):
        return int(time.mktime(time.strptime(dateTimeStr,fmtStr)))

    @staticmethod
    def dateTimeToStamp(dateTime):
        return int(time.mktime(dateTime.timetuple()))

    @staticmethod
    def getTime(dateStr, str):
        if dateStr:
            return datetime.datetime.strptime(dateStr, str)
        else:
            return None

    @staticmethod
    def fmtTime(str, date):
        if date:
            return datetime.datetime.strftime(date, str)
        else:
            return ''

    @staticmethod
    def fmtTimeH(str, date):
        if date:
            return datetime.time.strftime(date, str)
        else:
            return ''

    @staticmethod
    def currentTime(str):
        return datetime.datetime.now().strftime(str)

    @staticmethod
    def getMonthFirstDay(str):
        year = datetime.date.today().year
        month = datetime.date.today().month
        # 获取当月的第一天
        firstDay = datetime.date(year=year, month=month, day=1)
        return datetime.datetime.strftime(firstDay, str)

    @staticmethod
    def getMonthLastDay(str):
        year = datetime.date.today().year
        month = datetime.date.today().month
        # 获取当月的总天数
        monthRange = calendar.monthrange(year, month)
        lastDay = datetime.date(year=year, month=month, day=monthRange[1])
        return datetime.datetime.strftime(lastDay, str)

    # 获取两个日期之间的所有月 #
    @staticmethod
    def getBetweenMonth(begin_date, end_date):
        date_list = []
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m")
            date_list.append(date_str)
            begin_date = timeUtil.add_months(begin_date, 1)
        return date_list

    @staticmethod
    def add_months(dt, months):
        month = dt.month + 1
        year = dt.year
        if month == 13:
            month = 1
            year = year + 1

        return dt.replace(year=year, month=month)

    # 获取两个日期之间的天数
    @staticmethod
    def getBetweenDay(begin_date, end_date):
        return (begin_date - end_date).days

    # 获取指定月份的最后一天
    @staticmethod
    def get_last_day(year, month):
        # 获取指定月的总天数
        month_range = calendar.monthrange(year, month)
        last_day = datetime.date(year=year, month=month, day=month_range[1])
        return datetime.datetime.strftime(last_day, "%d")

    # 获取图表的开始时间
    @staticmethod
    def getChartStartTime():
        return datetime.datetime.strptime("06:25:00",'%H:%M:%S')

    # 获取图表的结束时间
    @staticmethod
    def getChartEndTime():
        return datetime.datetime.strptime("17:50:00",'%H:%M:%S')

    # 获取当前日期的时间戳：10位 #
    @staticmethod
    def getCurrentTemp10():
        return int(time.time())