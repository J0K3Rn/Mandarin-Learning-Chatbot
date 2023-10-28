# Mandarin-Learning-Chatbot

Use ChatGPT to assist in your language studies! Uses ChatGPT to generate sentences with 1000 of the most commonly used words in Chinese (Mandarin). English translations, pinyin, and text to speech examples are provided for easy review! 

Note: To run this project, you need an OpenAI account: https://openai.com

Previous iteration of this project was Bardarin, however Bards API is third party and sometimes malfunctions. https://github.com/J0K3Rn/Bardarin

Built upon many aspects from my Chinese-Flash-Cards repository: https://github.com/J0K3Rn/Chinese-Flash-Cards

Todo:
- Make pinyin toggleable
- Make english toggleable
- Add pronunciations using google speech
- implement a refresh button to pick a new word
- implement a highlight-translate for each character: https://stackoverflow.com/questions/4712310/javascript-how-to-detect-if-a-word-is-highlighted
How to run:
- Download repository
- Open downloaded repository with a command line interface
- run `pip install openai python-dotenv pandas flask pinyin googletrans==4.0.0-rc1`
- Create an OpenAI account
- Create a secret key and copy it from https://platform.openai.com/account/api-keys
- Create a .env file in the root of this project folder
- Open up the .env file with a text editor
- Add `OPENAI_API_KEY=<Add your secret key here>` to the .env
- That's it!
- Run the program with `python main.py`
- Open a web browser and go to `127.0.0.1:5000` 

Main Page:

![alt text](https://github.com/J0K3Rn/Mandarin-Learning-Chatbot/blob/main/screenshots/main_page.png?raw=true) 
