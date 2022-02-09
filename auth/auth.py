"""
  This is for the authentication for the server
"""

import requests
import datetime


class LogInClass:

    def __init__(self,email,password):
        self.token = None
        self.email = email
        self.password=password
        self.valid_till=None


    def authenticate(self):
        pass


   def getToken(self):
       if self.token is None:
           return None
       elif self.token.valid_till < datetime.datetime.now().timestamp():
           return None
       return self.token




