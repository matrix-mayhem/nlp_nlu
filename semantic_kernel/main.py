import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments
from services import Service
from service_settings import ServiceSettings

import pathlib


# Load environment variables
load_dotenv()

# Validate required environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

for var, val in {
    "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
    "AZURE_OPENAI_KEY": AZURE_OPENAI_KEY,
    "AZURE_OPENAI_API_VERSION": AZURE_OPENAI_API_VERSION,
    "AZURE_OPENAI_DEPLOYMENT_NAME": AZURE_OPENAI_DEPLOYMENT_NAME,
}.items():
    if not val:
        raise ValueError(f"{var} is not set in .env")

# Initialize Kernel
kernel = Kernel()
kernel.remove_all_services()

# Add Azure OpenAI service
kernel.add_service(
    AzureChatCompletion(
        service_id="default",
        deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=AZURE_OPENAI_API_VERSION
    )
)

# Load the plugin
plugin = kernel.add_plugin(parent_directory="prompt_templates", plugin_name="FunPlugin")

# Access the function with new method
joke_function = plugin["Joke"]

# Prepare arguments (v1.31.0 expects a KernelArguments object or dict)
args = KernelArguments({
    "input": "time travel to a dinosaur age",
    "style": "super silly"
})

# Invoke the function
async def tell_me_a_joke():
    try:
        result = await kernel.invoke(joke_function, args)
        print("Joke:", str(result))
    except Exception as e:
        print("Error during invocation:", e)

if __name__ == "__main__":
    asyncio.run(tell_me_a_joke())
