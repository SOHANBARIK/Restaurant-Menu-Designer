# import os
# import streamlit as st # Included since you imported it
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI # Use ChatOpenAI from the correct package
# from langchain_core.messages import HumanMessage # Used to format the chat prompt
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain # LLMChain is a chain that combines an LLM with a prompt template to create a single callable unit.
# from langchain.chains import SimpleSequentialChain
# from langchain.chains import SequentialChain

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate  # ✅ FIXED HERE
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain


# Load environment variables (like your OpenRouter API key)
load_dotenv()

# Get the API key from the environment
# OpenRouter uses the same "Bearer" token format as OpenAI, 
# so we can just pass the key.
OPENROUTER_API_KEY = os.getenv("API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("API_KEY not found in environment variables.")

# This is the base URL for OpenRouter's OpenAI-compatible endpoint
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# These headers are recommended by OpenRouter for analytics and identification
# Replace "YOUR_APP_NAME" with the name of your project
# You can also set a "HTTP-Referer" with your site URL
CUSTOM_HEADERS = {
    "X-Title": "YOUR_APP_NAME" 
}

# 1. Initialize the ChatOpenAI class
llm = ChatOpenAI(
    # 2. REQUIRED: Specify the model you want to use via OpenRouter
    # Example: "openai/gpt-3.5-turbo", "google/gemini-pro", "mistralai/mistral-7b-instruct"
    model='openai/gpt-3.5-turbo', 
    
    # 3. Pass your OpenRouter API key
    openai_api_key=OPENROUTER_API_KEY,
    
    # 4. Point the class to OpenRouter's base URL
    base_url=OPENROUTER_BASE_URL,
    
    # 5. Pass your custom headers
    default_headers=CUSTOM_HEADERS,
    
    # You can still set other parameters
    temperature=0.6,
    
)
# THE ABOVE WAS SETUP CODE FOR YOUR LLM
# name=llm("What is the capital of India?")
# print(name)

response = llm.invoke([HumanMessage(content="What is the capital of India?")])
# print(response)
#print(response.content)


# Chat models expect a list of messages, not just a raw string.
# We wrap our query in a HumanMessage object.

# prompt_messages = [
#     HumanMessage(content="What Today's {chain}?")
# ]

def generate_restaurant_name_and_items(cuisine):
    #Chain 1: Restaurant Name
    prompt_template_name= PromptTemplate( # it's a dictionary
        input_variables=['cuisine'],
        template="I want to open a restaurant that serves {cuisine} food. Suggest only one fancy name for this? Provide only one answer"
    )
    p=prompt_template_name.format(cuisine="Indian")
    print(p)
    # st.write(p)

    from langchain.chains import LLMChain # LLMChain is a chain that combines an LLM with a prompt template to create a single callable unit.
    name_chain=LLMChain(llm=llm,prompt=prompt_template_name,output_key="restaurant_name")
    restaurant_name=name_chain.run("American") # we used the output of first chain as input to the second chain
    # print(result)
    # st.write(result)
    #Chain 2: Menu Items
    prompt_template_items= PromptTemplate( # it's a dictionary
        input_variables=['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma seperated list."
    )# Here suggest some is used so plural
    food_item_chain=LLMChain(llm=llm,prompt=prompt_template_items,output_key="menu_items")

    
    chain = SimpleSequentialChain(chains=[name_chain,food_item_chain])#,verbose=True) will show the intermediate steps
    menu_items=chain.run("Mexican")

    overall_chain=SequentialChain(
        chains=[name_chain,food_item_chain],
        input_variables=["cuisine"],
        output_variables=["restaurant_name","menu_items"])#,verbose=True)
    response=overall_chain({"cuisine":cuisine})
    #print(response)
    return response

if __name__=="__main__":
    print(generate_restaurant_name_and_items("Chinese"))
