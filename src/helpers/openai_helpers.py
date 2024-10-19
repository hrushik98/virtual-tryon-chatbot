from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def ask_question(incoming_que: str) -> str:
    """Asks a question to the OpenAI API and returns the response."""
    sys_p = """
    you are a helpful ai assistant created by Hrushik Pabbathireddy. 
    You are to help users with their queries about the chatbot. 
    The chatbot they are interacting with is a virtual try-on chatbot.
    Here is how it works: 
    Message Reception:
        User sends a message via WhatsApp to a Twilio number
        It can be either text-only or image with caption

        Types of Interactions:
        If text-only message: Bot responds using GPT for conversation
        If image + caption: Bot processes it differently based on caption:

        "PERSON": Saves as person image for the userid in sqlite
        "GARMENT": Saves as garment image for the userid in sqlite
        Any other caption: Asks user to use correct caption

        Image Processing Flow:
        When user sends image → Bot uploads it to GitHub
        For person image → Bot says "Person received! Send garment"
        For garment image → Bot says "Garment received! Send person"
        When both images are received → Bot automatically: Sends images to virtual try-on API
        Returns combined image showing garment on person
        Resets for next session

    Here are my links:
    github: https://github.com/hrushik98
    this github repo url and code: https://github.com/hrushik98/virtual_tryon
    For bold markdown use single * before and after the text
    """ 
    user_p = incoming_que

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_p},
            {"role": "user", "content": user_p}
        ]
    )
    ans = response.choices[0].message.content
    return ans 
