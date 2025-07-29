from openai import AsyncOpenAI


class OpenaAIService:
    def __init__(self, api_key: str, business_url: str, language: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.business_name = business_url
        self.language = language


    async def get_link_descriptions(self, url: str, system_prompt: str = None, model_name: str = None):
        default_system_prompt = (
            f"I will provide you with a link from {self.business_name}\n\n"
            "I want you to make into chunk that I can use to store in vector DB. "
            "Formulate short text, that it would be an answer to user question, "
            "if user is looking for that link or the products/info inside the link. "
            "And Also add a question, to which the text below it would be the answer "
            "with link included.\n\n"
            f"Use {self.language} language. Don't add any explanations or reasoning."
        )
        
        prompt = system_prompt or default_system_prompt
        model_name = model_name or "gpt-4.1-mini"

        response = self.client.responses.create(
        model=model_name,
        input=[
            {
            "role": "system",
            "content": [
                {
                "type": "input_text",
                "text": prompt
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "input_text",
                "text": url
                }
            ]
            }
        ],
        text={
            "format": {
            "type": "text"
            }
        },
        reasoning={},
        tools=[],
        temperature=0.3,
        max_output_tokens=2048,
        top_p=1,
        store=False
        )

        return {" " : response.output_text}
