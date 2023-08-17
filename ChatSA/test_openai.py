import openai
openai.api_key = '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'

while True:
    msg = input()
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=msg,
        max_tokens=128,
        temperature=0.5
    )

    completed_text = response['choices'][0]['text']
    print(completed_text)