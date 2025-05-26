import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
'''List of Models'''
# client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

# models = client.models.list()
# for model in models.data:
#     print(model.id)

'''AzureOpenAI check'''
import os
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()
client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY")
)

try:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), # Use the deployment name for the model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "faster animal."}
        ]
    )
    print(response.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")