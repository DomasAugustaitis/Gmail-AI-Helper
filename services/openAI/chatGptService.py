import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "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"

def summariseEmail(emailBody):
    # Set the model and prompt
    model_engine = "text-davinci-003"
    green_intro = "Summarise the following email with 3 words: "
    prompt = green_intro + emailBody
    #prompt = green_intro + message

    # Set the maximum number of tokens to generate in the response
    max_tokens = 1024

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Print the response
    print(completion.choices[0].text)

    #return completion.choices[0].text