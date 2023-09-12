import openai
openai.api_key = '' # get your own key

# parameters
source = 'file1'
destination = 'file2'
prompt = "You will be provided with exerpts from a [insert language] novel, and your task is to translate it into English."
max_characters = 8000

# token calculating tools
def curr_tokens(messages):
    return sum([len(m["content"]) for m in messages])
def enough_tokens(messages, new_question):
    new_tokens = len(new_question)
    if (max_characters - curr_tokens(messages) - new_tokens) > 1.5 * new_tokens:
        return True
    return False

# file prep
file_read = open(source, 'r', encoding='utf-8-sig')
file_write = open(destination, 'a')
lines = file_read.readlines()
lines = map(lambda x: x.strip(), lines)
lines = list(filter(lambda x: x, lines))

# initialize messages
messages = [ {"role": "system", "content": prompt} ]

i = 0
while i < len(lines):
    
    # make a long paragraph
    message = ""
    lines_read = 0
    while lines_read < 8 and i < len(lines):
        line = lines[i] + '\n\n'
        message += line
        i += 1
        lines_read += 1

    if message:
        while not enough_tokens(messages, message):
            print("popping")
            messages.pop(1) # remove first prompt
            messages.pop(1) # remove first response
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
            # max_tokens = 10000
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        file_write.write(reply)
        print("progress: " + i * 100 / len(lines) + "%")
    

file_read.close()
file_write.close()


