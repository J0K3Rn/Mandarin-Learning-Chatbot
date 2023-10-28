import openai
import dotenv
import json
import pandas as pd
from random import choice
from flask import Flask, render_template, request
import pinyin


# Start Setup
app = Flask(__name__)
config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']
SAVED_OUTPUT = "data/saved_output.json"
dictionary = []  # list of dictionaries

# Read csv and convert to dictionary
try:
    df = pd.read_csv('data/chinese_words.csv')
except FileNotFoundError:
    print("File not found!")
    exit(1)

to_learn = df.to_dict(orient="records")
total = 69740745  # Accumulation of all Frequency Count in the CSV <Calculated manually>
# End Setup


def reload_dictionary():
    global dictionary
    with open(SAVED_OUTPUT, "r") as file:
        dictionary = json.load(file)


def add_word(character):
    global dictionary
    # Be sure to check if it exists first
    new_dict = {
        'character': character,
        'examples': []
    }
    dictionary.append(new_dict)
    with open(SAVED_OUTPUT, "w") as file:
        file.write(json.dumps(dictionary, indent=4, ensure_ascii=False))


def check_if_word_exists(character):
    global dictionary
    for index in dictionary:
        if index['character'] == character:
            print("Character exists!")
            return True
    print("Character does not exist!")
    return False


def get_examples(character):
    global dictionary
    example_list = []
    for index in dictionary:
        if index['character'] == character:
            example_list = index['examples']
    return example_list


def add_example(character, example):
    global dictionary
    for index, dic in enumerate(dictionary):
        if dic['character'] == character:
            dictionary[index]['examples'].append(example)
            with open(SAVED_OUTPUT, "w") as file:
                file.write(json.dumps(dictionary, indent=4, ensure_ascii=False))
            reload_dictionary()
            return


def example_exists(character, example):
    global dictionary
    for index in dictionary:
        if index['character'] == character:
            # print("Character exists!")
            print("index examples:")
            print(index["examples"])
            for ex in index['examples']:
                if ex == example:
                    print("Example exists!")
                    return True
    print("Example does not exist!")
    return False


def chatgpt_query(word):
    # prompt = f"Generate 3 sentences in Chinese using {word}."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        #prompt=prompt
        messages=[{"role": "user", "content": f'Generate 3 sentences in Chinese using {word}.'}]
    )
    print(response)
    print(response['choices'][0]['message']['content'])

    output_to_parse = response['choices'][0]['message']['content']
    chatgpt_examples = output_to_parse.split('\n')
    print(chatgpt_examples)

    for example in chatgpt_examples:
        example = example[3:]
        print(example)
        if check_if_word_exists(word):
            # if so, get examples
            if not example_exists(word, example):
                add_example(word, example)
        else:
            add_word(word)
            add_example(word, example)
    examples = get_examples(word)
    print(examples)
    return examples


@app.route('/')
def main():
    global to_learn
    reload_dictionary()  # Need this function ran every time the program starts

    current_entry = choice(to_learn)
    character = current_entry['Chinese']
    meaning = current_entry['English']
    character_pinyin = pinyin.get(character, delimiter=" ")
    frequency = current_entry['Frequency Count'] / total
    frequency = f'{frequency:.9f}%'

    # Debug
    print(f'Current entry: {current_entry}')
    print(f'Current character: {character}')
    print(f'Character meaning: {meaning}')
    print(f'Character frequency: {frequency}')

    # Ask ChatGPT to generate some examples
    examples = chatgpt_query(character)
    examples_pinyin = [pinyin.get(example, delimiter=" ") for example in examples]
    print(examples_pinyin)
    # Present examples to user
    return render_template('index.html', character=character, character_pinyin=character_pinyin, meaning=meaning, examples=examples, examples_pinyin=examples_pinyin, frequency=frequency)
    #return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
