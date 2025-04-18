from openai import OpenAI

client = OpenAI()

# this is new

# --------------------------------------------------------------
# Basic web search
# --------------------------------------------------------------

response = client.responses.create(
    model="gpt-4o",
    tools=[
        {
            "type": "web_search_preview",
        }
    ],
    input="What are the best restaurants in Poznan?",
)

print(response.output_text)

# '''
# --------------------------------------------------------------
# Basic web search with location
# --------------------------------------------------------------

response = client.responses.create(
    model="gpt-4o",
    tools=[
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "PL",
                "city": "Poznan",
            },
        }
    ],
    input="What are the best restaurants in Poznan?",
)

print(response.output_text)
print(response.output[1].content[0].annotations)
print(response.output[1].content[0].annotations[0].url)

# '''