import os

from openai import AzureOpenAI

import project_parser

client = AzureOpenAI(
  azure_endpoint = os.environ["ENDPOINT"],
  api_key= os.environ["API_KEY"],
  api_version="2024-02-01"
)

content = project_parser.get_content()

response = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": content,
    }],
    model="gpt-4o-mini",
)

print(response.choices[0].message.content)