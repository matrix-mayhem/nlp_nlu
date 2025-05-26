import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelFunction
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings

load_dotenv()

# Azure OpenAI configuration
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  # Replace with your Azure deployment name
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")

# Prompt for the joke
joke_prompt = input("You: ")

async def main():
    # Create kernel
    kernel = Kernel()

    chat_service = AzureChatCompletion(
        service_id="default",
        deployment_name=deployment,
        endpoint=endpoint,
        api_key=api_key
    )
    kernel.add_service(chat_service)

    joke_execution_settings = OpenAIChatPromptExecutionSettings(
        max_tokens=50,
        temperature=0.9
    )

    tell_joke_function = KernelFunction.from_prompt(
        prompt=joke_prompt,
        function_name="TellJoke",
        plugin_name="JokePlugin",
        description="Tells a short and funny joke",
        # Pass the execution settings directly
        prompt_execution_settings=joke_execution_settings
    )

    result = await kernel.invoke(tell_joke_function)

    print("yulu:", str(result))

if __name__ == "__main__":
    asyncio.run(main())