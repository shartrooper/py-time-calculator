def add_time(start, duration,weekday=''):

    class Clock:
        def __init__(self,time,hour,minutes,meridiem,weekday):
            self.time=time
            self.hour=int(hour)
            self.minutes=int(minutes)
            self.meridiem=meridiem
            self.weekday=weekday.lower()
            
        def updateTime(self):
            hour=self.hour
            minutes=self.minutes
            if not hour:
                hour='00'
            if not minutes:
                minutes='00'
            if len(str(minutes))<2:
                minutes='0'+str(minutes)
            self.time= str(hour)+':'+str(minutes)
    
    class Days:
        def __init__(self,hours,minutes,weekday):
            self.__hour=hours
            # totalDays = (hours+(minutes/60))/24
            self.__totalDays=(hours+int(minutes/60))/24
            self.__weekday=weekday.capitalize()
            if self.getTotal() and self.__weekday:
                self.__determineNextDayWeek()
        def __determineNextDayWeek(self):
            weekdayList=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            for day in range(self.getTotal()):
                for i,weekday in enumerate(weekdayList):
                    if weekday == self.__weekday:
                        idx=i+1
                        if idx == 7:
                            self.__weekday=weekdayList[0]
                        else:
                            self.__weekday=weekdayList[idx]
                        break

        def currentWeekday(self):
            return self.__weekday

        def getTotal(self):
            return int(self.__totalDays)
    
    class AdvanceTime:
        def __init__(self,clock,days,duration):
            self.__clock=clock
            self.__days=days
            self.__duration= duration
        def __advanceTimeClockwise(self):
            switchMiddayPeriod={'AM':'PM','PM':'AM'}
            while self.__duration.time != '00:00':
                addHours=0
                addMinutes=0
                if self.__duration.hour < 12:
                    addHours=self.__duration.hour
                    addMinutes=self.__duration.minutes
                    self.__duration.hour=0
                    self.__duration.minutes=0
                    self.__duration.updateTime()
                else:
                    self.__duration.hour-=12
                    self.__duration.updateTime()
                    self.__clock.meridiem=switchMiddayPeriod[self.__clock.meridiem]
                    continue
                self.__clock.hour+=addHours
                self.__clock.minutes+=addMinutes
                if self.__clock.minutes>=60:
                    self.__clock.minutes-=60
                    self.__clock.hour+=1
                if self.__clock.hour>=12:
                    if self.__clock.hour>12:
                        self.__clock.hour-=12
                    self.__clock.meridiem=switchMiddayPeriod[self.__clock.meridiem]
            self.__clock.updateTime()
        def result(self):
            self.__advanceTimeClockwise()
            daystr=''
            weekdaystr=self.__days.currentWeekday()
            if self.__days.getTotal() == 1:
                daystr=' (next day)'
            if self.__days.getTotal() > 1:
                daystr=f" ({self.__days.getTotal()} days later)"
            if weekdaystr:
                weekdaystr=f", {self.__days.currentWeekday()}"
            return f"{self.__clock.time} {self.__clock.meridiem}{weekdaystr}{daystr}"
    
    clockStart=None
    timeDuration=None
    #Error handling and Clock Class instantiation
    try:
        if ':' not in start or ':' not in duration:
            return Exception('Error: invalid time format')
        if 'AM' not in start and 'PM' not in start:
            return Exception('Error: undefined 12-clock midday period (AM/PM)')
        
        startHour,rest=start.split(':')
        startMin,meridiem=rest.split()
        durationHour,durationMin=duration.split(':')
        
        if int(startHour)>12:
            return Exception('Error: starting time hour must be in 12-clock format')
        if ( len(startMin)== 1 or int(startMin) >= 60) or (len(durationMin) == 1 or int(durationMin) >= 60):
            return Exception('Error: some argument\'s minutes are not within clock format range (00 to 60)')
        
        clockStart= Clock(start,startHour,startMin,meridiem,weekday)
        timeDuration= Clock(duration,durationHour,durationMin,'','')
    except Exception as err:
        raise err
    
    twentyfourHourClock=clockStart.hour
    #transform to 24hr format for total days calculation
    if clockStart.meridiem == 'AM' and twentyfourHourClock == 12:
        twentyfourHourClock=0
    elif clockStart.meridiem == 'PM' and twentyfourHourClock < 12:
        twentyfourHourClock=clockStart.hour+12

    new_time=AdvanceTime(clockStart,Days(timeDuration.hour+twentyfourHourClock,timeDuration.minutes+clockStart.minutes,clockStart.weekday),timeDuration)
    return new_time.result()