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




USERNAME = '####'
PASSWORD = '####'
BANNED = 'meet video call number phone facebook instagram skype gmail email whatsapp viber snapchat see at in'
EMOJIS = '😘 ❤️ 💝 💘 ❣ 💖 😍 😘 😽 😻 😚 💋 💗 💞 💓 💕'.split()


# In[2]:


driver = webdriver.Chrome()


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
    ban = banned.split()
    ban_all = []
    for word in ban:
        ban_all.append(word)
        ban_all.append(word.capitalize())
        ban_all.append(' ' + word.capitalize())
        ban_all.append(' ' + word)
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    ids = [tokenizer(word)['input_ids'][0] for word in ban_all]
    biases = {i:-100 for i in ids}
    return biases

def translate_to_english(message):
    openai.api_key = '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'

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"Translate text into English:\n\n\n"+message,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['text'].replace('\n', '')
    
    
def reply_to_text(message, banned):
    openai.api_key = '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'

    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt = f"""reply to a text in a texting flirty manner, at least 70 characters long, you don't want to meet. You want to chat. Use emojis. \n{message} \nReply:""",
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


# In[4]:


driver.get('file://' + 'C:/Users/mariu/Desktop/Projects/Sex-Chatbot/' + 'Chat-test-1.html')


# In[5]:


message = find_message(driver.page_source)


# In[6]:


en_message = translate_to_english(message)


# In[7]:


banned = get_token_permutations(BANNED)


# In[8]:


test = reply_to_text(en_message, banned)


# In[9]:


len(test)


# In[10]:


message


# In[11]:


en_message


# In[ ]:




