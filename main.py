import openai
import dotenv
import json


prompt = "Generate 3 sentences in Chinese using the character 我."

config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']
#openai.api_key_path = ".env"
curr_char = '我'
SAVED_OUTPUT = "data/saved_output.json"
dictionary = []  # list of dictionaries


def reload_dictionary():
    global dictionary
    with open(SAVED_OUTPUT, "r") as file:
        dictionary = json.load(file)
    #print(type(dictionary))
    #print(dictionary)


def add_character(character):
    global dictionary
    # Be sure to check if it exists first
    new_dict = {
        'character': character,
        'examples': []
    }
    dictionary.append(new_dict)
    with open(SAVED_OUTPUT, "w") as file:
        #json.dumps(MarksList, indent=4)
        print(json.dumps(dictionary, indent=4, ensure_ascii=False))
        file.write(json.dumps(dictionary, indent=4, ensure_ascii=False))


def check_if_character_exists(character):
    global dictionary
    for index in dictionary:
        if index['character'] == character:
            print("Character exists!")
            return
    add_character(character)


def add_character_example(character, example):
    global dictionary
    # Update
    for index, dic in enumerate(dictionary):
        if dic['character'] == character:
            dictionary[index]['examples'].append(example)
            print(dictionary)
            with open(SAVED_OUTPUT, "w") as file:
                print(json.dumps(dictionary, indent=4, ensure_ascii=False))
                file.write(json.dumps(dictionary, indent=4, ensure_ascii=False))
            reload_dictionary()
            return


def check_if_example_exists(character, example):
    global dictionary
    for index in dictionary:
        if index['character'] == character:
            #print("Character exists!")
            for ex in index['examples']:
                if ex == example:
                    return
    add_character_example(character, example)


reload_dictionary()
#check_if_character_exists("abc")
check_if_example_exists("abc", "Hello World!")

#
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-0613",
#     #prompt=prompt
#     messages=[{"role": "user", "content": f'Generate 3 sentences in Chinese using the character {curr_char}.'}]
# )
#
# print(response)
#
# print(response['choices'][0]['message']['content'])
#
# output_to_parse = response['choices'][0]['message']['content']
# examples = output_to_parse.split('\n')
# for example in examples:
#     example = example[3:]
#     # Read csv, check if example already exists, if not then add to list
#     # sorted by character, and then check if sentence exists
#     print(example)
#
# print("a")
# print(examples)

