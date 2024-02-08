import streamlit as st
import requests
import openai
import json

# Initialize OpenAI & Exa client

def fetch_context_dria(query, contract_id):
    """Fetch context from a Dria API using the query and contract_id."""
    response_1 = requests.post(
        "https://search.dria.co/hnsw/search",
        headers={'x-api-key': dria_key, 'Content-Type': 'application/json'},
        json={
            "rerank": True,
            "top_n": 10,
            "contract_id": contract_id,
            "query": query
        }
    )
    print(response_1.text)
   
    r1 = response_1.json()
    print(response_1)
    print("Response 1:", r1)
    c1 = [i["metadata"] for i in r1["data"]]
    contexts = " Sentence: ". join(c1[0:3]) 
    return contexts


    
def get_llm_response(context, query):
    """Get a response from the LLM using the context and query."""
    messages = [
        {"role": "system", "content": f"""Answer the query by using the Contexts and your existing knowledge. If context is not providing relevant information you can rely on your knowledge.
         
         Contexts: {context} """},
        {"role": "user", "content": f"Prompt: {query}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",  # Replace with your model
        messages=messages
    )
    return response.choices[0].message['content'] if response else "No response from LLM."

def get_llm_response_2(query):
    """Get a response from the LLM using the context and query."""
    messages = [
        {"role": "system", "content": f"Query: {query}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",  # Replace with your model
        messages=messages
    )
    return response.choices[0].message['content'] if response else "No response from LLM."


def get_llm_response_3(llm_response_1,llm_response_2,query):
    """Get a response from the LLM using the context and query."""
    messages = [
        {"role": "system", "content": f"""Tell me which of the below answers is better response for the query. Tell the winner by using a phrase similar to "The winner response is 'Response Name' because 'The reason'". 
         
         GPT+Dria Answer: {llm_response_1}
         GPT Answer: {llm_response_2}
         """},
        {"role": "user", "content": f"Prompt: {query}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",  # Replace with your model
        messages=messages
    )
    return response.choices[0].message['content'] if response else "No response from LLM."


# Streamlit App
st.title("GTP empowered by On-Chain AI Memory")

# User inputs a query
col1, col2, col3 = st.columns(3)
with col1:
 user_contract_id = st.text_input("Enter the contract ID of the Knowledge:")

with col2:
 dria_key = st.text_input("Enter your Dria API Key:")
    
with col3:
 openai.api_key = st.text_input("Enter your OpenAI API Key:")


user_query = st.text_input("Enter your query:")
submit_button = st.button("Submit")

if submit_button and user_query and user_contract_id:
    # Fetch context using the query
    context = fetch_context_dria(user_query, user_contract_id)
    
    # Display retrieved context (optional)
    st.subheader("Context Retrieved from Dria:")
    # Context dropdown menu
    with st.expander("View Dria Context"):
            st.write(context)
             

    llm_response_1 = get_llm_response(context, user_query)
    llm_response_2 = get_llm_response_2(user_query)
    
    col1, col2 = st.columns(2)

    with col1:
       st.subheader("GPT + Dria Response:")
       st.write(llm_response_1)

    with col2:
       st.subheader("GPT Response:")
       st.write(llm_response_2)
    

    llm_response_3 = get_llm_response_3(llm_response_1, llm_response_2, user_query)
    st.subheader("Winner:")
    st.write(llm_response_3)









