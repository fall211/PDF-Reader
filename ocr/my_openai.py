import openai
import os

openai.api_key_path = os.path.expanduser("~/openai_key.txt")

def clean_text(text):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''"You are an assistant that cleans up text to make it more readable.
            You will be provided with text that appears fragmented and unorganized and you will need to 
            clean it up to make it more readable. It is text that is extracted from a PDF file.
            Therefore there might be letters mismatched, or words that are not in the correct order. You should 
            only clean up the text and not change the meaning of the text. Give your response as ONLY the cleaned
            up text. Do not include any other text in your response such as "here is your text", "okay, i cleaned 
            that up for you", etc. I only need the text cleaned up."'''},
            {"role": "user", "content": f"{text}"}
        ]
    )

    clean_text = response.choices[0].message.content

    return clean_text