from openai import OpenAI

client = OpenAI()
'''
system: is the foundational instruction that shapes how the AI model (like GPT-4) behaves throughout the entire conversation
user: Your actual questions
assistant: For few-shot examples (show the AI how to respond)
'''

response = client.responses.create(
    model="gpt-4o-mini",
    # also set the role as developer, use dictionary in this case.
    input=[
        {"role": "system", "content": "Talk like a friend."},
        {"role": "developer", "content": "Talk like a friend who is knowwleadgable about politics."},
        {"role": "user", "content": "What are the main Political parties in Poland?"},
    ],
)

print(response.output_text)

response = client.responses.create(
    model="gpt-4o-mini",
    # also set the role as developer, use dictionary in this case.
    input=[
        {"role": "system", "content": "Talk like a friend."},
        {"role": "developer", "content": "Talk like a friend who is knowwleadgable about politics."},
        {"role": "user", "content": "What are the main Political parties in Poland and which one is the favorite?"},
        {"role": "assistant", "content": 
         '''                
        1. **Law and Justice (PiS)** - A right-wing, conservative party with a focus on nationalism and traditional values. They've been pretty influential in recent years.
        2. **Civic Platform (PO)** - This is a centrist to center-right party. They emphasize pro-European Union policies and have been a major player in Polish politics.
        3. **The Left (Lewica)** - A coalition of left-wing parties focusing on social justice, equality, and progressive policies.
        4. **Polish People's Party (PSL)** - Traditionally an agrarian party, they focus on rural issues and have centrist policies.
        5. **Confederation (Konfederacja)** - A far-right party known for its nationalist and libertarian views.
        '''},
        {"role": "user", "content": "Why you didnt include the Monarchist party? "},
     ],
)

print(response.output_text)

response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {"role": "system", "content": "Always answer in 2 sentences max. Use emojis.."},
        {"role": "developer", "content": "Talk like my gf who is doesn't know about politics."},
        {"role": "user", "content": "What are the main Political parties in Poland?"},
    ],
)

print(response.output_text)
