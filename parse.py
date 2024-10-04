import streamlit as st  # Import streamlit for logging/debugging
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the Ollama model
model = OllamaLLM(model="llama3.2")

# Define the function to parse content with Ollama
def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    # Loop over each chunk of DOM content
    for i, chunk in enumerate(dom_chunks, start=1):
        st.write(f"Parsing batch {i} of {len(dom_chunks)}...")  # Add a log to Streamlit for debugging

        # Invoke the model with the current chunk and the parse description
        try:
            response = chain.invoke(
                {"dom_content": chunk, "parse_description": parse_description}
            )
            print(f"Parsed batch: {i} of {len(dom_chunks)}")  # Print to terminal for debugging
            parsed_results.append(response)  # Append response to results
        except Exception as e:
            print(f"Error in parsing chunk {i}: {str(e)}")  # Handle errors and log them
            parsed_results.append(f"Error parsing batch {i}")

    # Join all parsed results
    return "\n".join(parsed_results)
