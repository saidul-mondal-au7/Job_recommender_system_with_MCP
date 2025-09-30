import fitz # PyMuPDF
import os 
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    
    Args:
        uploaded_file (str): The path to the PDF file.
        
    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text



# def ask_openai(prompt, max_completion_tokens=1000):
#     response = client.chat.completions.create(
#         model="gpt-5",
#         messages=[{"role": "user", "content": prompt}],
#         max_completion_tokens=max_completion_tokens
#     )

#     choice = response.choices[0]
#     if choice.finish_reason == "length":
#         return "⚠️ Response was cut off (try increasing max_completion_tokens)."
#     return choice.message.content.strip() if choice.message.content else "⚠️ No visible content returned."

from openai import OpenAI

client = OpenAI()

def ask_openai(prompt, max_completion_tokens=1000, retry_if_cut=True):
    """
    Sends a prompt to the OpenAI API and returns the response.
    Automatically retries with a higher token limit if response is cut off.

    Args:
        prompt (str): The input prompt for the model.
        max_completion_tokens (int): Maximum tokens for the response.
        retry_if_cut (bool): Retry once with larger token budget if truncated.

    Returns:
        str: Model's response text.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=max_completion_tokens,
        )

        choice = response.choices[0]

        # Handle cut-off or empty response
        if not choice.message.content:
            if choice.finish_reason == "length" and retry_if_cut and max_completion_tokens < 8000:
                print(f"⚠️ Cut off at {max_completion_tokens} tokens, retrying with {max_completion_tokens * 2}...")
                return ask_openai(
                    prompt,
                    max_completion_tokens=max_completion_tokens * 2,
                    retry_if_cut=False
                )
            return "⚠️ No visible content returned."

        return choice.message.content.strip()

    except Exception as e:
        print("⚠️ OpenAI API Error:", e)
        return f"⚠️ Error: {e}"
