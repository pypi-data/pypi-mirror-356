
import json
from typing import Union
from user_agents import parse

class UserAgent:
    
    def __init__(self, req) -> None:
        self.req = req
        
        #dict =  
        

    def get(self) -> Union[object, None]:
        """
        Returns the user agent data as a dictionary.
        If the user agent cannot be parsed, returns an empty dictionary.
        """
        nested_data = None
        if hasattr(self.req, 'user_agent'):
            nested_data = self.req.useragent 
        else:
            ua_string = self.req.META['HTTP_USER_AGENT']

            if not ua_string and 'User-Agent' in self.req.headers:
                ua_string = self.req.headers['User-Agent']

            if not ua_string and 'user-agent' in self.req.headers:
                ua_string = self.req.headers['user-agent']
                    
            # Parse the user agent string
            if ua_string:
                nested_data = parse(ua_string)
            
        return  nested_data
    
    
    def data(self) -> Union[dict, None]:
        """
        Returns the user agent data as a dictionary.
        If the user agent cannot be parsed, returns an empty dictionary.
        """
        obj_data = self.get()
        if not obj_data:
            return None
        
        # Convert the user agent object to a dictionary
        json_data = json.loads(json.dumps(obj_data, default=lambda o: o.__dict__))
  
        return dict(json_data)