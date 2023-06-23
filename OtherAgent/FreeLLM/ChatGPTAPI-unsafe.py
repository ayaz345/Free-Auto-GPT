
from revChatGPT.V1 import Chatbot
import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import pydantic
import os
from langchain import PromptTemplate, LLMChain
from time import sleep



class ChatGPT(LLM):
    
    history_data: Optional[List] = []
    token : Optional[str]
    chatbot : Optional[Chatbot] = None
    call : int = 0
    conversation : Optional[str] = ""
    prev_message : str = ""
    
    #### WARNING : for each api call this library will create a new chat on chat.openai.com
    
    
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if self.token is None:
            raise ValueError("Need a token , check https://chat.openai.com/api/auth/session for get your token")
        if self.conversation == "":
            self.chatbot = Chatbot(config={"access_token": self.token})
        elif self.prev_message == "":
            self.chatbot = Chatbot(config={"access_token": self.token}, conversation_id=self.conversation)
        else:
            self.chatbot = Chatbot(config={"access_token": self.token}, conversation_id=self.conversation, parent_id=self.prev_message)
        response = ""
        if self.call >= 45:
            raise ValueError("You have reached the maximum number of requests per hour ! Help me to Improve. Abusing this tool is at your own risk")
        sleep(2)
        for data in self.chatbot.ask( prompt , conversation_id=self.conversation, parent_id=self.prev_message):
            response = data["message"]
            FullResponse = data

        self.conversation = FullResponse["conversation_id"]
        self.prev_message = FullResponse["parent_id"]
        self.call += 1

        #add to history
        self.history_data.append({"prompt":prompt,"response":response})    

        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "ChatGPT", "token": self.token}


#llm = ChatGPT(token = "YOUR_TOKEN") #for start new chat
#llm = ChatGPT(token = "YOUR-TOKEN", conversation = "Add-XXXX-XXXX-Convesation-ID") #for use a chat already started

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("Can you resume your previus answer?")) #now memory work well
