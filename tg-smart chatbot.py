import telebot

import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n =1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str:
    for q in knowledge_base['questions']:
        if q['question'] == question:
            return q['answer']

knowledge_base: dict = load_knowledge_base('knowledge_base.json')

BOT_TOKEN = '7171912786:AAGU7yZt1T-mid4buNWkcCfvA9VP9E7nWvk'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def reply(message):
    user_input: str = message.text.lower()

    best_match: str | None = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])

    if best_match:
        answer: str = get_answer_for_question(best_match, knowledge_base)
        bot.reply_to(message, f'{answer}')
        print(user_input)
        return

    else:
        bot.reply_to(message, 'I don\'t know the answer. Can you teach me? \n\nType the answer or "skip" to skip:')
        print(user_input)

    def handle_answer(msg):
        global new_answer
        new_answer = msg.text.lower()
        print(new_answer)
        # Process the new answer here, you can add further logic if needed
        if new_answer != 'skip':
            knowledge_base['questions'].append({'question': user_input, 'answer': new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            bot.reply_to(msg,'Thank you, I learned a new response')
        else:
            print('user skipped')
    # Register the handle_answer function to be called on the next user message
    bot.register_next_step_handler(message, handle_answer)


bot.infinity_polling()