Install Libraries
Prompt:
“Write the pip install commands needed for:
beautifulsoup4, langchain, sentence-transformers, numpy, faiss-cpu, transformers, torch”

Create requirements.txt
Prompt:
“Generate a requirements.txt listing exactly those seven libraries (one per line).”

Wikipedia scraper
Prompt:
“Write a Python function called scrape_webpage(url) that uses requests to fetch [insert the URL you want to scrape], parses it with BeautifulSoup, extracts all <p> tags inside <div class='mw-parser-output'>, joins their text with blank lines, writes the result to Selected_Document.txt (UTF‑8), prints a success/failure message based on the HTTP status code, and returns the article text. Please hard‑code the URL in the function. Also include a main() function and an if __name__ == '__main__': block that calls scrape_webpage() so the script runs when executed.”

Suppress Noisy Logs
Prompt:
“Write code to import logging, transformers.logging (as hf_logging), and warnings; then set the log level of langchain.text_splitter and transformers to ERROR, and filter Python warnings. Add this to the bottom of the existing program.”

Parameters
Prompt:
“Write code to define the variables
chunk_size = 500
chunk_overlap = 50
model_name = "sentence-transformers/all-distilroberta-v1"
top_k = 5
and add it to the bottom of the existing program.”

Read the Pre‑scraped Document
Prompt:
“Write code to open Selected_Document.txt in UTF‑8 mode, read its contents into a variable text, and add it to the bottom of the existing program.”

Split into Appropriately‑sized Chunks
Prompt:
“Write code to import and use RecursiveCharacterTextSplitter (with separators ['\n\n', '\n', ' ', ''] and the above chunk_size and chunk_overlap) to split text into a list chunks, and add it to the bottom of the existing program.”

Embed & Build FAISS Index
Prompt:
“Write code to load SentenceTransformer(model_name), encode chunks (showing a hidden progress bar), convert the result to a NumPy float32 array, initialize a FAISS IndexFlatL2 with the correct dimension, add the array to it, and add this snippet to the bottom of the existing program.”

Load the Generator Pipeline
Prompt:
“Write code to import and set up a HuggingFace pipeline('text2text-generation', model='google/flan-t5-small', device=-1), assign it to generator, and add it to the bottom of the existing program.”

Retrieval & Answering Functions
Prompt:
“Write code to define:
def retrieve_chunks(question, k=top_k):
    # encode the question, search the FAISS index, return top k chunks

def answer_question(question):
    # call retrieve_chunks, build a prompt with context, call generator, and return generated_text
and add these two functions to the bottom of the existing program.”

Interactive Loop
Prompt:
“Write code to wrap an input loop under:

if __name__ == "__main__":
    print("Enter 'exit' or 'quit' to end.")
    while True:
        question = input("Your question: ")
        if question.lower() in ("exit","quit"):
            break
        print("Answer:", answer_question(question))
so that the user can keep asking until they type ‘exit’ or ‘quit’, and add it to the bottom of the existing program.”