from openai import OpenAI
import asyncio

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)
async def main() -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    ) # type: ignore


asyncio.run(main())

# def askGPT(text):
#     openai.api_key = "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"
#     response = openai.Completion.create( # type: ignore
#         engine = "text-davinci-003",
#         prompt = text,
#         temperature = 0.6,
#         max_tokens = 150
#     )
#     return print(response.choices[0].text)
  
# def main():
#     while True:
#         print('GPT: Ask me a question\n')
#         myQn = input()
#         askGPT(myQn)
#         print('\n')

# main()