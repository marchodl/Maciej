import json
from typing import List

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

# 2 ways using
# a json schema
# pythandic

# --------------------------------------------------------------
# Using a JSON Schema
# --------------------------------------------------------------

# --------------------------------------------------------------
# Using a Pydantic model (and simple response format)
# --------------------------------------------------------------

"""
https://news.ycombinator.com/item?id=43336251
"""

# second method using pythndic model

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: List[str]


response = client.responses.parse(
    model="gpt-4o",
    input="Alice and Bob are going to a science fair on Friday",
    instructions="Extract the event information",
    text_format=CalendarEvent,
)

response_model = response.output[0].content[0].parsed

print(type(response_model))
print(response_model.model_dump_json(indent=2))
print(response_model.name)