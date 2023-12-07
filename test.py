
import json

from openai import OpenAI
client = OpenAI(api_key="")

response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  # response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You know everything about php and linux and webdevelopment to output JSON."},
    # {"role": "user", "content": "Who won the world series in 2020?"},
    # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "how to become a good developer"}
  ]
)

# pretty_json = json.dumps(response, indent=4, sort_keys=True)
# print(pretty_json)
# print(response)
print(response.choices[0].message.content)