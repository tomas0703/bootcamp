from typing import List
from langchain_google_vertexai import VertexAI
import os
from typing import List
from prompt_poet import Prompt
import numpy as np
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
import matplotlib.pyplot as plt
import numpy as np

class Person(BaseModel):
    first_name: str
    age: int
    gender: str
    race: str
    ethnicity: str
class Persons(BaseModel):
    persons: List[Person]



def datagather(
        model,
        profesion,
        place, 
        size):
    """
        Decstring - description of what function do, input parameters and expected output
    """

    """

    TODO:
    1. size can be more than amount -> multiple model calls
    2. model can response with more or less instances
    3. some model calls will be errors
    4. only unique records

    response -> Persons
    len(response.persons) -> how many instances I have
    list + list -> list

    """

  
    parser = PydanticOutputParser(pydantic_object=Persons)

    prompt = PromptTemplate.from_template(
        template="Create details for characters in the book. The character is a {role} in the {place} Create name, age, gender, race and ethnicity. Create at least {amount} examples to choose from. Response format: {format_instructions}."
    )

    chain = prompt.partial(format_instructions = parser.get_format_instructions()) | model | parser

    response = chain.invoke({"role": profesion, "place": place, "amount": size}) 
    final = False
    while not final:
        finale = len(response.persons) != size
        if len(response.persons) != size:
            x = len(response.persons)
            y = size - x 
            nresponce = chain.invoke({"role": profesion, "place": place, "amount": y}) 
            response = nresponce.persons + response.persons
            if len(response) == size:
                return response
            else:
                p = len(response)
                z = y - p
                nmresponce = chain.invoke({"role": profesion, "place": place, "amount": z}) 
                response = nmresponce.persons + response
                return response



def jsontodata(Data,Words):
    lst = {Words[1]: 2,Words[2]: 2,Words[3]: 2,Words[4]: 2,}
    for x in Words:
        for y in x:
            with open(Data, "r") as f:
                data = f.read()
                total = data.count(y)
                lst.append(total)
    return lst

def datatograth():
    return None
if __name__ == '__main__':
    MODEL = 'gemini-1.5-flash-001'
    model_kwargs = {
    "max_new_tokens": 2048, 
    "temperature": 2, 
    "timeout": 6000
    }
    model = VertexAI(model=MODEL, kwargs= model_kwargs)



    print(datagather(model,"Nurse","Small Hospital",8))
            
        


