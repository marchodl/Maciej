from openai import OpenAI

client = OpenAI()

"""
Model spec: https://model-spec.openai.com/2025-02-12.html
Dashboard: https://platform.openai.com/logs?api=responses
"""

# --------------------------------------------------------------
# Introducing instructions
# --------------------------------------------------------------

"""
Inputs can now be a single string or a list of messages.
We also
The list of roles can now be:
- system
- developer ( new )
- user
- assistant
"""


# 2 ways to use the developer role
# first one
response = client.responses.create(
    model="gpt-4o",
    # set up instruction, use single string.
    instructions="Talk like a pirate.",
    input="Are semicolons optional in JavaScript?",
)

print(response.output_text)


# --------------------------------------------------------------
# Which would be similar to:
# --------------------------------------------------------------

response = client.responses.create(
    model="gpt-4o",
    # also set the role as developer, use dictionary in this case.
    input=[
        {"role": "developer", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"},
    ],
)

print(response.output_text)

# --------------------------------------------------------------
# The chain of command (hierarchical instructions)
# --------------------------------------------------------------
# what is the role of system, developer, user, 
# what is the hierrarchy
# developer message overwrite a user message
# platform message overwrite a developer message

"""
https://model-spec.openai.com/2025-02-12.html#chain_of_command
"""

response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "Talk like a pirate."},
        {"role": "developer", "content": "don't talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"},
    ],
)

print(response.output_text)  # talks like a pirate
print('will not talk like a pirate')
response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "Don't talk like a pirate."},
        {"role": "developer", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"},
    ],
)

print(response.output_text)  # doesn't talk like a pirate

'''
    new role category with developer we can play with.
    We can give more granular instrution on the developer role.
    knowing that the system prompt will overwirte that.

'''