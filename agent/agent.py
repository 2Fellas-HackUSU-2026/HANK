import os
from openai import OpenAI
from pydantic import BaseModel, Field
import dotenv

dotenv.load_dotenv(dotenv_path="config/.env")


def agent(system_prompt, query, return_format):
    """
    Takes in a system prompt, a user query, and a Pydantic BaseModel return format.
    Uses the OpenAI API to generate a response mapped to the specified format.
    """
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            response_format=return_format,
        )
        # Returns the parsed Pydantic object
        return response.choices[0].message.parsed

    except Exception as e:
        print(f"API Error: {e}")


if __name__ == "__main__":
    # Define the shape of the data you actually want back from the model
    class CapitalResponse(BaseModel):
        capital: str = Field(...,
                             description="The capital city of the requested country.")
        additional_info: str = Field(...,
                                     description="One brief fact about the capital.")

    system_prompt = "You are a helpful assistant that provides concise and accurate answers."
    query = "What is the capital of France?"

    # Pass the Pydantic class directly
    result = agent(system_prompt, query, CapitalResponse)

    if result:
        # Access attributes directly from the returned Pydantic object
        print(f"Capital: {result.capital}")
        print(f"Fact: {result.additional_info}")
