#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import openai
from transformers import GPT2TokenizerFast
import random
import deepl




USERNAME = '####'
PASSWORD = '####'
BANNED = 'meet video call number phone facebook instagram skype gmail email whatsapp viber snapchat see at in'.split()
BLACKLIST = 'SMS nr numer pastas gmail email pašt pasimat FACETIME'.split()
EMOJIS = '😘 ❤️ 💝 💘 ❣ 💖 😍 😘 😽 😻 😚 💋 💗 💞 💓 💕 😊 🥰 ✨ 🥺 🔥 🙏'.split()
GPT_KEY = 'xxx'
DEEPL_KEY = 'xxx'
MALE = ['as ', 'ęs ', 'is ', 'as,', 'ęs,', 'is,', 'as.', 'ęs.', 'is.']
FEMALE = ['a ', 'usi ', 'i ', 'a,', 'usi,', 'i,', 'a.', 'usi.', 'i.']


# In[2]:


driver = webdriver.Chrome()
translator = deepl.Translator(DEEPL_KEY)


# In[3]:


def login(USERNAME, PASSWORD):
    driver.get('http://agents.moderationinterface.com/login')
    username_input = driver.find_element(by=By.NAME, value='username')
    password_input = driver.find_element(by=By.NAME, value='password')
    login_button = driver.find_element(by=By.ID, value='login-submit')
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    login_button.click()
    
def find_message(html):
    soup = BeautifulSoup(html)
    return soup.find("div", {"class": "timeline-body"}).text

def get_token_permutations(banned):
    ban_all = []
    for word in banned:
        ban_all.append(word)
        ban_all.append(word.capitalize())
        ban_all.append(' ' + word.capitalize())
        ban_all.append(' ' + word)
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    ids = [tokenizer(word)['input_ids'][0] for word in ban_all]
    biases = {i:-100 for i in ids}
    return biases    
    
def translate_to_english(message):
    message = translator.translate_text(message, target_lang="EN-US").text
    return message

def translate_to_lithuanian(message):
    message = translator.translate_text(message, target_lang="EN-US").text
    return message

def reply_to_text(message, banned):
    openai.api_key = GPT_KEY
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt = f"""reply to a text in a texting flirty manner, at least 70 characters long, you don't want to meet. You want to chat. Use emojis. Text:\n{message} \nReply:""",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    logit_bias= banned
    )
    return response['choices'][0]['text'].replace('\n', '')
 
def reply_to_first(banned):
    openai.api_key = GPT_KEY
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt="Write a flirty text as a woman, you want to chat with him:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    logit_bias= banned
    )
    return response['choices'][0]['text'].replace('\n', '')
    
    
def fill_reply(reply):
    reply = reply.replace('  ', ' ')
    while len(reply)<72:
        reply = reply + ' ' + random.choice(EMOJIS)
        reply = reply.replace('  ', ' ')
    return reply

def final_filter(text, blacklist):
    for word in blacklist:
        text = text.replace(word, ' ')
    return text


def get_reply(message):
    if message == '[Please reactivate the user!]':
        reply = reply_to_first(BANNED)
    else:
        message = translate_to_english(message)
        reply = reply_to_text(message, BANNED)
    reply = translator.translate_text(reply, target_lang="LT").text
    reply = feminize(reply)
    reply = final_filter(reply, BLACKLIST)
    reply = fill_reply(reply)
    return reply

    
def feminize(message):
    for f, m in zip(FEMALE, MALE):
        message = message.replace(m, f)
    return message

def send_reply(reply):
    text_input = driver.find_element(by=By.XPATH, value='//*[@id="chat-windows-message-textarea"]')
    driver.execute_script(f"document.getElementsByName('message')[0].value='{reply}'")
    send_button = driver.find_element(by=By.XPATH, value='/html/body/app-root/block-ui/ng-component/div/ng-component/div/div/div/div/div[2]/div/form/div[2]/div/div/div/div[2]/div/button[2]')
    send_button.click()
    


# In[4]:


BANNED = get_token_permutations(BANNED)


# In[5]:


driver.get('file://' + 'C:/Users/mariu/Desktop/Projects/Sex-Chatbot/' + 'Chat-test-1.html')


# In[ ]:




