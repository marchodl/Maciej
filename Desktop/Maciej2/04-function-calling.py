from openai import OpenAI
import requests
import json
from pydantic import BaseModel, Field
from typing import List


client = OpenAI()

def get_weather(latitude: float, longitude: float) -> dict:
    """Get current weather for given coordinates (temperature_2m, wind_speed_10m)."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,wind_speed_10m"
    )
    return response.json()["current"]


tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
             "latitude": {
                    "type": "number",
                    "description": "Latitude in decimal degrees (e.g., 48.8566 for Paris)"
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude in decimal degrees (e.g., 2.3522 for Paris)"
                }
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    }
}]

system_prompt = "You are a helpful weather assistant."
history = [
        {"role": "system", "content":system_prompt},
        {"role": "user", "content": "What is the weather like in Paris today?"}
]
response = client.responses.create(
    model="gpt-4.1",
    input=history,
    tools=tools
)

# print(response.output)



# print(response.output)
# print(response.output[0].model_dump_json(indent=2))
# print(response.output[1].model_dump_json(indent=2))


# --------------------------------------------------------------
# Step 2: Model decides to call function(s)
# --------------------------------------------------------------
# print(completion)

# --------------------------------------------------------------
# Step 3: Execute get_weather function
# --------------------------------------------------------------
def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)

args = json.loads(response.output[0].arguments)
name = response.output[0].name
# print(args)
result = call_function(name,args)
print(history)

history.append({
    "type": "function_call_output", 
    "call_id": response.output[0].id, 
    "output": str(result)
})


response_2 = client.responses.create(
    model="gpt-4.1",
    input=history,
    # tools=tools,
)
print(response_2.output_text)

'''
class WeatherResponse(BaseModel):
    temperature: float = Field(
        description="The current temperature in celsius for the given location."
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )


response = client.responses.parse(
    model="gpt-4o",
    input=history,
    # instructions="Give me the weather in Paris",
    text_format=WeatherResponse,
)

print(response)
response_model = response.output[0].content[0].parsed

print(response_model)

# print(response_model.temperature)
# print(response_model.response)

'''