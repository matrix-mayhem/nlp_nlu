from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()
# Replace with your Azure Cognitive Services credentials
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# Authenticate
credential = AzureKeyCredential(key)
client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

# Sample input
documents = [
    "I love working with Python and Azure!",
    "The weather is terrible today.",
    "Let's build something amazing with AI."
]

# Language Detection
language_result = client.detect_language(documents=documents)
print("\n🔤 Language Detection:")
for doc in language_result:
    print(f"Text: {doc.id}, Language: {doc.primary_language.name}")

# Sentiment Analysis
sentiment_result = client.analyze_sentiment(documents=documents)
print("\n😊 Sentiment Analysis:")
for doc in sentiment_result:
    print(f"Text: {doc.id}, Sentiment: {doc.sentiment}, Scores: {doc.confidence_scores}")

# Key Phrase Extraction
key_phrase_result = client.extract_key_phrases(documents=documents)
print("\n🔑 Key Phrases:")
for doc in key_phrase_result:
    print(f"Text: {doc.id}, Key Phrases: {doc.key_phrases}")
