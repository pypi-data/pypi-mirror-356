import base64
import os
import json
import requests
import pandas as pd
from io import StringIO, BytesIO
import jsonpickle
import gzip
from enum import Enum
import logging
from typing import Optional

class ConditionOperator(Enum):
   Equals = 0
   NotEquals = 1
   GreaterThan = 2
   LessThan = 3
   GreaterThanOrEqualTo = 4
   LessThanOrEqualTo = 5
   StartsWith = 6
   Like = 7
   NotStartsWith = 8
   NotLike = 9
   Contains = 10
   NotContains = 1

class LogicalOperator(Enum):
   And = 0
   Or = 1
   AndNot = 2

class AIDataFilter:
    def __init__(self, Field:str, ConditionOperator:ConditionOperator, LogicalOperator:LogicalOperator, Value, StartGroup:int, EndGroup:int, CaseInsensitive:bool):      
        self.Field = Field
        self.ConditionOperator = ConditionOperator
        self.LogicalOperator = LogicalOperator
        self.Value = Value
        self.StartGroup = StartGroup
        self.EndGroup = EndGroup
        self.CaseInsensitive = CaseInsensitive
    def to_dict(self):
        return {
            "Field": self.Field,
            "ConditionOperator": self.ConditionOperator.value,
            "LogicalOperator": self.LogicalOperator.value,
            "Value": self.Value,
            "StartGroup": self.StartGroup,
            "EndGroup": self.EndGroup,
            "CaseInsensitive": self.CaseInsensitive
        }
    
class AIDataSimpleFilter:
    def __init__(self, Field:str, Value):
        self.Field = Field
        self.Value = Value
    def to_dict(self):
        return {
            "Field": self.Field,
            "Value": self.Value
        }

class StructuredDataDriver:
    class AIDataAPIRequest:
        def __init__(self, Subject: str, Fields: list[str], Filters: list['AIDataFilter']):      
            self.Subject = Subject
            self.Fields = Fields
            self.Filters = Filters  # List of AIDataFilterUsed
        def to_dict(self):
            return {
                "Subject": self.Subject,
                "Fields": self.Fields,
                "Filters": [f.to_dict() for f in self.Filters]
            }

    class AIDataAPIResponse:
        def __init__(self,noRows,fileSize,csvDataString,columnNamesandTypes):      
          self.noRows = noRows
          self.fileSize = fileSize
          self.csvDataString = csvDataString
          self.columnNamesandTypes = columnNamesandTypes
        def toJSON(self):
          return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, tenant: str, server:str ="inmydata.com", logging_level=logging.INFO, log_file: Optional[str] = None ):
        
        self.server = server
        self.tenant = tenant

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

        self.logger.info("StructuredDataDriver initialized.")

        pass

    def get_data(self, subject: str, fields: list[str], filters: list[AIDataFilter]):
            result = None
            aidatareq = self.AIDataAPIRequest(subject,fields,filters)
            input_json_string  = jsonpickle.encode(aidatareq.to_dict(), unpicklable=False)
            self.logger.info("Executing " + str(input_json_string))
            if input_json_string is None:
                raise ValueError("input_json_string is None and cannot be loaded as JSON")
            myobj = json.loads(input_json_string)
            headers = {'Authorization': 'Bearer ' + self.api_key,
                    'Content-Type': 'application/json'}
            url = 'https://' + self.tenant + '.' + self.server + '/api/developer/v1/ai/data'
            x = requests.post(url, json=myobj,headers=headers)
            if x.status_code == 200:    
                decoded_response = jsonpickle.decode(x.text)
                if isinstance(decoded_response, dict):
                    value = decoded_response.get("value")
                else:
                    raise ValueError("Decoded response is not a dictionary. Actual type: {}".format(type(decoded_response)))
                if value is None:
                    raise ValueError("Response does not contain 'value' or it is None")
                value_json = jsonpickle.encode(value)
                if value_json is None:
                    raise ValueError("value_json is None and cannot be loaded as JSON")
                aidataresp = self.AIDataAPIResponse(**json.loads(value_json))
                if aidataresp.noRows > 0:            
                  buff = BytesIO(base64.standard_b64decode(aidataresp.csvDataString))
                  with gzip.GzipFile(fileobj=buff) as gz:
                    decompressed_data = gz.read()    
                    data = StringIO(decompressed_data.decode('utf-8'))
                    result = pd.read_csv(filepath_or_buffer = data)
            return result

    def get_data_simple(self,subject:str,fields:list[str],simplefilters:list[AIDataSimpleFilter], caseSensitive: Optional[bool] = True):
            filters = []
            # Ensure caseSensitive is always a bool
            case_insensitive = bool(caseSensitive) if caseSensitive is not None else True
            for simpleFilter in simplefilters:           
              filter = AIDataFilter(Field=simpleFilter.Field,ConditionOperator=ConditionOperator.Equals,LogicalOperator=LogicalOperator.And,Value=simpleFilter.Value,StartGroup=0,EndGroup=0, CaseInsensitive=case_insensitive)
              filters.append(filter)
            return self.get_data(subject,fields,filters)
    