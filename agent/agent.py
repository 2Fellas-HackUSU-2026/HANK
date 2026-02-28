import os
from openai import OpenAI
from pydantic import BaseModel, Field

import dotenv

dotenv.load_dotenv(dotenv_path="config/.env")


def agent(system_prompt, query, return_format):
    """
    The main function for the agent. It takes in a system prompt, a user query, and a return format.
    It then uses the OpenAI API to generate a response based on the system prompt and user query.
    The response is returned in the specified format.

    Use the following format to create the return format for the agent:

    class agent_return_format(BaseModel):
    response: str = Field(..., description="The response from the agent.")
    field: list[str] = Field(..., description="A list of fields that the agent should return.")
    """

    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
    try:
        response = client.responses.parse(
            model="gpt-4o-2024-08-06",
            input=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": query,
                },
            ],
            text_format=return_format,
        )

        return response.output_parsed

    except Exception as e:
        print(f"API Error: {e}")


if __name__ == "__main__":
    # just a test. Doens't run in production
    class agent_class(BaseModel):
        system_prompt: str = Field(...,
                                   description="The system prompt for the agent.")

        query: str = Field(...,
                           description="The user query for the agent.")

        return_format: str = Field(...,
                                   description="The format in which the agent should return the response.")

    system_prompt = "You are a helpful assistant that provides concise and accurate answers to user queries."
    query = "What is the capital of France?"
    return_format = "text"

    result = agent(system_prompt, query, agent_class)
    print(result)
