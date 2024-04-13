import openai
from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
# print(os.getenv("OPENAI_API_KEY"))


client = OpenAI()
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content":
      ""},
    {"role": "user", "content":
      "Say hello in 15 differents languages."}
  ]
)

print(completion.choices[0].message)

