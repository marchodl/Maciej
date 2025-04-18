from openai import OpenAI

client  = OpenAI()
# https://platform.openai.com/docs/api-reference/responses

# compare different way to call API
# Basic text example with the Chat Completions API

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": "I have a pandas dataframe with 12 rows each for a month called df, can you give me the matplotplib cmd to draw a nice chart showing each month and the revenue"
        }
    ]
)
print(response.choices[0].message.content)

# Basic text example with the Responses API
#
response = client.responses.create(
    model="gpt-4o", 
    input="I have a pandas dataframe with 12 rows each for a month called df, can you give me the matplotplib cmd to draw a nice chart showing each month and the revenue."
)
print(response.output_text)



# --------------------------------------------------------------
# Image example
# --------------------------------------------------------------

response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "user", "content": "what teams are playing in this image?"},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": "https://www.aljazeera.com/wp-content/uploads/2022/12/SSS11261.jpg?resize=1920%2C1440",
                }
            ],
        },
    ],
)

print(response.output_text)

# --------------------------------------------------------------
# Streaming
# --------------------------------------------------------------


stream = client.responses.create(
    model="gpt-4o",
    input="Say 'double bubble bath' ten times fast.",
    stream=True,
)

# Store chunks in a list
text_chunks = []

for event in stream:
    if hasattr(event, "type") and "text.delta" in event.type:
        text_chunks.append(event.delta)
        print(event.delta, end="", flush=True)

'''
Benefits of Streaming (stream=True):
Faster Perceived Performance

Without streaming, you have to wait for the entire response to be generated before seeing anything.

With streaming, you get chunks of text as soon as they're available, making the app feel more responsive.

Better for Long Responses

If the response is long (e.g., a story, code, or detailed explanation), streaming lets users start reading or processing early instead of waiting.
'''
