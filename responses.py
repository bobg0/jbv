from random import choice, randint
import openai
# from openai import OpenAI
import os


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=f"{user_input}",
    #     max_tokens=2048,
    #     temperature=0.5,
    # )

    openai.api_key = os.getenv('OPENAI_API_KEY')
    print(openai.api_key,  os.getenv('OPENAI_API_KEY'))

    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"{user_input}"
            }
        ]
    )
    # print(completion.choices[0].message)
    return completion.choices[0].message.content
