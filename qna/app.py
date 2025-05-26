from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models
from dotenv import load_dotenv
import os

load_dotenv()
# Replace with your Azure endpoint and key
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

credential = AzureKeyCredential(key)
client = QuestionAnsweringClient(endpoint, credential)

# Replace with your knowledge base project name and deployment name
project_name = os.getenv("QNA_PROJECT_NAME")
deployment_name = os.getenv("QNA_DEPLOYMENT_NAME")

# Example user question
question = "can I use it on mac?"

# Send question to the knowledge base
output = client.get_answers(
    question=question,
    project_name=project_name,
    deployment_name=deployment_name
)

# Show the top answer
if output.answers:
    print(f"Answer: {output.answers[0].answer}")
else:
    print("No answer found.")
