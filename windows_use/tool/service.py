from pydantic import BaseModel

class Tool:
    def __init__(self, name: str|None=None, description: str|None=None, args_schema:BaseModel|None=None):
        self.name = name
        self.description = description
        self.args_schema = {k:{term:content for term,content in v.items() if term not in ['title']} for k,v in args_schema.model_json_schema().get('properties').items() if k not in ['title']}
        self.function = None

    def __call__(self, function):
        if self.name is None:
            self.name = function.__name__
        if self.description is None:
            self.description = function.__doc__
        self.function = function
        return self
    
    def invoke(self, *args, **kwargs):
        return self.function(*args, **kwargs)