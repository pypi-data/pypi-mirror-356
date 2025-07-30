from typing import Optional
from dataclasses import dataclass
from enum import Enum
from datetime import date
from io import StringIO
from signalrcore.hub_connection_builder import HubConnectionBuilder
import json
import pandas as pd
import os
import aiohttp
import logging

class Model(Enum):
    gpt4 = 0
    o3mini = 1

class AIQuestionOutputTypeEnum(Enum):
    text = 0
    data = 1
    chart = 2

class AITypeEnum(Enum):
    azureopenai = 0
    openai = 1    

@dataclass
class Answer:
    answer: str

@dataclass
class QuestionResponse:
    def __init__(self, answer: str, dataFrame: pd.DataFrame):
      self.answer = answer
      self.dataFrame = dataFrame
    def toJSON(self):
      return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ConversationalDataDriver:
    callbacks = None

    class AIQuestionAPIRequest:
        def __init__(self, Subject,Question,Date,Model,OutputType,AIType,SkipZeroQuestion,SkipGeneralQuestion,SummariseComments):
          self.Subject = Subject
          self.Question = Question
          self.Date = Date
          self.model = Model
          self.outputtype = OutputType
          self.aitype = AIType
          self.SkipZeroQuestion = SkipZeroQuestion
          self.SkipGeneralQuestion = SkipGeneralQuestion
          self.SummariseComments = SummariseComments
        def toJSON(self):
          return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    class AIQuestionAPIResponse:
        def __init__(self, answer,answerDataJson):
          self.answer = answer
          self.answerDataJson = answerDataJson
        def toJSON(self):
          return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    class AIQuestionStatus:
        def __init__(self, ConversationID,User,StatusMessage,StatusCommand,Sequence):
          self.ConversationID = ConversationID
          self.User = User
          self.StatusMessage = StatusMessage
          self.StatusCommand = StatusCommand
          self.Sequence = Sequence
        def toJSON(self):
          return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, tenant: str, server:str ="inmydata.com", logging_level=logging.INFO, log_file: Optional[str] = None):
        self.server = server
        self.tenant = tenant
        self.hub_connection = HubConnectionBuilder()\
            .with_url("https://" + tenant + "." + server + "/datahub",
                options={"access_token_factory": self.api_key})\
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 5,
                "max_attempts": 5
            })\
            .build()
        self.hub_connection.on("AIQuestionStatus", self.__process_server_message)
        self.hub_connection.start()
        self.hub_connection.on_open(lambda: self.logger.info("Connection opened"))
        
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

        self.logger.info("ConversationalDataDriver initialized.")
        pass

    async def get_answer(self, question: str, subject: Optional[str] = None) -> Answer:
        self.logger.info("query_for_answer question: " + question)        
        answer = await self.__get_answer(subject, question)
        self.logger.info("query_for_answer answer: " + str(answer))    
        return Answer(answer=answer if answer is not None else "")

    async def get_data_frame(self, question: str, subject: Optional[str] = None) -> Optional[pd.DataFrame]:
        airesp = await self.__get_answer_object(subject,question,AIQuestionOutputTypeEnum.data.value)
        if airesp is not None and hasattr(airesp, 'answerDataJson') and airesp.answerDataJson:
            return pd.read_json(StringIO(airesp.answerDataJson))
        else:
            self.logger.info("No answer data available.")
            return None
        
    async def get_answer_and_data_frame(self, question: str, subject: Optional[str] = None) -> Optional[QuestionResponse]:
        airesp = await self.__get_answer_object(subject,question,AIQuestionOutputTypeEnum.data.value)
        if airesp is not None and hasattr(airesp, 'answerDataJson') and airesp.answerDataJson:
            return QuestionResponse(answer=airesp.answer, dataFrame=pd.read_json(StringIO(airesp.answerDataJson)))
        else:
            self.logger.info("No answer data available.")
            return None
        
    def on(self, event_name, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if event_name not in self.callbacks:
            self.callbacks[event_name] = [callback]
        else:
            self.callbacks[event_name].append(callback)

    async def __get_answer_object(self, subject,question,outputtype = AIQuestionOutputTypeEnum.text.value):
        aireq = self.AIQuestionAPIRequest(subject,question,date.today().strftime("%m/%d/%Y"),Model.o3mini.value,outputtype,AITypeEnum.azureopenai.value, True, True, True)
        headers = {'Authorization': 'Bearer ' + self.api_key,
             'Content-Type': 'application/json'}
        self.logger.debug("AIQuestionAPIRequest")
        self.logger.debug(aireq.toJSON())
        x = await self.__post_request('https://' + self.tenant + '.' + self.server + '/api/developer/v1/ai/question', data=json.loads(aireq.toJSON()),headers=headers)
        self.logger.debug("Post request to inmydata complete")
        self.logger.debug(x)
        if x is not None:                
            return self.AIQuestionAPIResponse(x['answer'], x['answerDataJson'])
        else:
            self.logger.warning("Unsuccessful request")
        return None

    async def __get_answer(self, subject, question):
        airesp = await self.__get_answer_object(subject,question)
        if airesp is not None:
            return airesp.answer
        else:
            return None
    
    def __process_server_message(self, message):
        aiqs = self.AIQuestionStatus(**json.loads(message[0]))
        self.__trigger("ai_question_update", aiqs.StatusMessage)

    def __trigger(self, event_name, event_data):
        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self, event_data)
    
    async def __post_request(self, url, data, headers=None):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=data) as response:
                response_data = await response.json()
                return response_data
