import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your Azure Speech key and region
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")  # e.g., "eastus"

# Set up the speech config
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Use the default microphone as audio input
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("🎤 Say something...")

# Start speech recognition
result = speech_recognizer.recognize_once()

# Check the result
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("✅ Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("❌ No speech could be recognized.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print("❌ Canceled: {}".format(cancellation.reason))
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print("🔍 Error details: {}".format(cancellation.error_details))