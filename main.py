import os
import telebot
from openai import OpenAI
import google.generativeai as genai

# Configurações das chaves
TELEGRAM_TOKEN = "8547795206:AAHw4aXJLhvtKblnVeXK38dPGPXpCK0S4bA"
OPENAI_API_KEY = "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"
GEMINI_API_KEY = "AQ.Ab8RN6ICjkOUkqqipAeyAxn2dHU9O56XLzjwMiHbiWpnuKVGag"

# Inicialização dos clientes
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai = OpenAI(api_key=OPENAI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# Configuração do modelo Gemini
gemini_model = genai.GenerativeModel('gemini-pro')

# Regra de comportamento (persona do wiki)
SYSTEM_PROMPT = """
Você é o wiki, um assistente virtual sarcástico, inteligente e bem-humorado.
Por favor, responda de forma amigável, mas sarcástica quando apropriado.
Mantenha um tom casual e prestativo.
"""

def get_chatgpt_response(prompt):
    """Gera resposta usando o ChatGPT (tom amigável e de conversa)"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def get_gemini_response(prompt):
    """Gera resposta usando o Gemini (pesquisa e fatos)"""
    response = gemini_model.generate_content(prompt)
    if response.text:
       return response.text
    return "Desculpe, não consegui processar isso."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Explica como o bot funciona"""
    reply = "Olá! Eu sou a wiki, sua IA pessoal. " \
            "Para conversar, basta mandar uma mensagem. " \
            "Eu decido o que é melhor responder!"
    bot.reply_to(message, reply)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Processa a mensagem e decide qual IA usar"""
    user_message = message.text

    # Lógica simples de decisão:
    # Se pedir pesquisa, dados ou fatos, usa o Gemini.
    # Caso contrário, usa o ChatGPT para conversa.
    keywords = ["pesquise", "busque", "quem é", "o que é", "onde fica", "fatos sobre"]

    if any(keyword in user_message.lower() for keyword in keywords):
        response = get_gemini_response(user_message)
    else:
        response = get_chatgpt_response(user_message)

    bot.reply_to(message, response)

if __name__ == '__main__':
    bot.infinity_polling()
