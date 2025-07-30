import os
import json
import requests
import jsonpickle
from datetime import date
import logging
from typing import Optional
   
class FinancialPeriodDetails:
    def __init__(self, year: int, month: int, week: int, quarter: int):
        self.year = year
        self.month = month
        self.week = week
        self.quarter = quarter
    def __repr__(self):
        return f"FinancialPeriodDetails(year={self.year}, month={self.month}, week={self.week}, quarter={self.quarter})"

class CalendarAssistant:

    class GetCalendarDetailsRequest:
        def __init__(self,UseDate,CalendarName):      
          self.UseDate = UseDate
          self.CalendarName = CalendarName
        def toJSON(self):
          return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    class GetCalendarDetailsResponse:
        def __init__(self,dateDetails):      
          self.dateDetails = dateDetails
        def toJSON(self):
          return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    class DateDetails:
        def __init__(self,year:int,month:int,week:int,quarter:int,yearseq:int,monthseq:int,weekseq:int,quarterseq:int,yearid:int,monthid:int,weekid:int,quarterid:int,date:date):      
          self.year = year
          self.month = month
          self.week = week
          self.quarter = quarter
          self.yearseq = yearseq
          self.monthseq = monthseq
          self.weekseq = weekseq
          self.quarterseq = quarterseq
          self.yearid = yearid
          self.monthid = monthid
          self.quarterid = quarterid
          self.weekid = weekid
          self.date = date
        def toJSON(self):
          return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, tenant: str, calendar_name: str, server: str = "inmydata.com", logging_level=logging.INFO, log_file: Optional[str] = None ):
        self.tenant = tenant
        self.calendar_name = calendar_name
        self.server = server

        # Create a logger specific to this class/instance
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}.{tenant}")
        self.logger.setLevel(logging_level)
        
        # Avoid adding multiple handlers if this gets called multiple times
        if not self.logger.handlers:
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

            if log_file:
                handler = logging.FileHandler(log_file)
            else:
                handler = logging.StreamHandler()

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.propagate = False  # Prevent propagation to the root logger
        
        try:
           self.api_key = os.environ['INMYDATA_API_KEY']
        except KeyError:
           self.api_key = ""
           self.logger.warning("Environment variable INMYDATA_API_KEY not set. API requests to the inmydata platform will fail.")

        self.logger.info("CalendarAssistant initialized.")

    def get_financial_periods(self, input_date: date) -> FinancialPeriodDetails:
        """Returns the financial period (year, month, week, quarter) for the given date."""
        cd = self.__get_calendar_details(input_date)
        if cd is None:
            raise ValueError("Calendar details not found for the given date.")
        return FinancialPeriodDetails(cd.dateDetails.year, cd.dateDetails.month, cd.dateDetails.week, cd.dateDetails.quarter)

    def get_week_number(self, input_date: date) -> int:
        """Week number (1–53) in the current financial year."""
        cd = self.__get_calendar_details(input_date)
        if cd is None:
            raise ValueError("Calendar details not found for the given date.")
        return cd.dateDetails.week

    def get_financial_year(self, input_date: date) -> int:
        """Returns the financial year (based on the anniversary of the custom start date)."""
        cd = self.__get_calendar_details(input_date)
        if cd is None:
            raise ValueError("Calendar details not found for the given date.")
        return cd.dateDetails.year

    def get_quarter(self, input_date: date) -> int:
        """Returns the quarter (1–4) in the current financial year."""
        cd = self.__get_calendar_details(input_date)
        if cd is None:
            raise ValueError("Calendar details not found for the given date.")
        return cd.dateDetails.quarter

    def get_month(self, input_date: date) -> int:
        """Returns the pseudo-month (1–12) as 4-week periods in the financial year."""
        cd = self.__get_calendar_details(input_date)
        if cd is None:
            raise ValueError("Calendar details not found for the given date.")
        return cd.dateDetails.month

    def __get_auth_token(self):        
        return os.environ['INMYDATA_API_KEY'] 
    
    def __get_calendar_details(self,input_date:date):
        result = None
        caldetreq = self.GetCalendarDetailsRequest(input_date,self.calendar_name)
        input_json_string  = jsonpickle.encode(caldetreq, unpicklable=False)
        if input_json_string is None:
            raise ValueError("input_json_string is None and cannot be loaded as JSON")
        myobj = json.loads(input_json_string)
        headers = {'Authorization': 'Bearer ' + self.__get_auth_token(),
                'Content-Type': 'application/json'}
        url = 'https://' + self.tenant + '.' + self.server + '/api/developer/v1/ai/getcalendardetails'
        x = requests.post(url, json=myobj,headers=headers)
        if x.status_code == 200:     
            response_json = json.loads(x.text)
            datedetailsdict = response_json["value"]["dateDetails"]
            datedetails = self.DateDetails(datedetailsdict["year"],datedetailsdict["month"],datedetailsdict["week"],datedetailsdict["quarter"],
                                      datedetailsdict["yearseq"],datedetailsdict["monthseq"],datedetailsdict["weekseq"],datedetailsdict["quarterseq"],
                                      datedetailsdict["yearid"],datedetailsdict["monthid"],datedetailsdict["weekid"],datedetailsdict["quarterid"],
                                      datedetailsdict["date"])
            result = self.GetCalendarDetailsResponse(datedetails)            
        return result