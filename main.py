import openai
import dotenv
import json
import pandas as pd
from random import choice

# Start Setup
config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']
#openai.api_key_path = ".env"
#curr_word = '我'
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
    # print(type(dictionary))
    # print(dictionary)


def add_word(character):
    global dictionary
    # Be sure to check if it exists first
    new_dict = {
        'character': character,
        'examples': []
    }
    dictionary.append(new_dict)
    with open(SAVED_OUTPUT, "w") as file:
        #json.dumps(MarksList, indent=4)
        #print(json.dumps(dictionary, indent=4, ensure_ascii=False))
        file.write(json.dumps(dictionary, indent=4, ensure_ascii=False))


def check_if_word_exists(character):
    global dictionary
    for index in dictionary:
        if index['character'] == character:
            print("Character exists!")
            return True
    return False
    # add_character(character)


def get_examples(character):
    global dictionary
    example_list = []
    for index in dictionary:
        # print(index)
        if index['character'] == character:
            example_list = index['examples']
    return example_list


def add_example(character, example):
    global dictionary
    # Update
    for index, dic in enumerate(dictionary):
        if dic['character'] == character:
            dictionary[index]['examples'].append(example)
            #print(dictionary)
            with open(SAVED_OUTPUT, "w") as file:
                #print(json.dumps(dictionary, indent=4, ensure_ascii=False))
                file.write(json.dumps(dictionary, indent=4, ensure_ascii=False))
            reload_dictionary()
            return


def example_exists(character, example):
    global dictionary
    for index in dictionary:
        if index['character'] == character:
            # print("Character exists!")
            for ex in index['examples']:
                if ex == example:
                    return True
    return False
    # add_example(character, example)


def chatgpt_query(word):
    prompt = f"Generate 3 sentences in Chinese using {word}."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        prompt=prompt
        # messages=[{"role": "user", "content": f'Generate 3 sentences in Chinese using the character {word}.'}]
    )
    print(response)
    print(response['choices'][0]['message']['content'])

    output_to_parse = response['choices'][0]['message']['content']
    chatgpt_examples = output_to_parse.split('\n')

    for example in chatgpt_examples:
        example = example[3:]
        print(example)
        if check_if_word_exists(word):
            # if so, get examples
            if example_exists(word, example):
                add_example(word, example)
            examples = get_examples(word)
            print(examples)
            return examples
        else:
            add_word(word)
            add_example(word, example)


def app():
    global to_learn
    reload_dictionary()  # Need this function ran every time the program starts

    current_entry = choice(to_learn)
    character = current_entry['Chinese']
    meaning = current_entry['English']
    frequency = current_entry['Frequency Count'] / total
    frequency = f'{frequency:.9f}%'

    # Testing
    print(current_entry)
    print(character)
    print(meaning)
    print(frequency)

    chatgpt_query(character)

    # Present examples to user


def main():
    app()


if __name__ == "__main__":
    main()
