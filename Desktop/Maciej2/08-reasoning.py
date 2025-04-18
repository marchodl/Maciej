from openai import OpenAI

client = OpenAI()

"""
https://platform.openai.com/docs/guides/reasoning?api-mode=responses
"""

prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

response = client.responses.create(
    model="o3-mini",
    # plugin reasoning parameter, control the effort.
    # depending on effort it cost more, higher token, higher token
    reasoning={"effort": "medium"},
    input=[{"role": "user", "content": prompt}],
)

print(response.output_text)