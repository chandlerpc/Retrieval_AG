# --- Imports ---
import warnings
import logging
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from transformers import logging as hf_logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Suppress Warnings and Logs ---
# Suppress Python warnings
warnings.filterwarnings("ignore")

# Set the logging level for langchain and transformers to ERROR to reduce verbosity
logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)
hf_logging.set_verbosity_error()

# --- Parameters ---
chunk_size = 500
chunk_overlap = 50
model_name = "sentence-transformers/all-distilroberta-v1"
top_k = 5

# --- Read the Document ---
try:
    with open("Selected_Document.txt", "r", encoding="utf-8") as f:
        text = f.read()
except FileNotFoundError:
    print("Error: Selected_Document.txt not found. Please run text_extractor.py first.")
    exit()

# --- Split into Chunks ---
text_splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', ' ', ''],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
chunks = text_splitter.split_text(text)
print(f"Document split into {len(chunks)} chunks.")

# --- Embed & Build FAISS Index ---
print("Loading sentence transformer model...")
# Initialize the sentence transformer model
model = SentenceTransformer(model_name)

print("Encoding chunks and building FAISS index...")
# Encode the text chunks into embeddings
embeddings = model.encode(chunks, show_progress_bar=True)

# Convert embeddings to float32 for FAISS
embeddings = np.float32(embeddings)

# Get the dimensionality of the embeddings
d = embeddings.shape[1]

# Initialize a FAISS index using the L2 distance metric
index = faiss.IndexFlatL2(d)

# Add the embeddings to the index
index.add(embeddings)
print("FAISS index built successfully.")

# --- Load the Generator Pipeline ---
print("Loading text generation model...")
# Use -1 for CPU, or 0 for the first GPU if available
generator = pipeline('text2text-generation', model='google/flan-t5-small', device=-1)
print("Models loaded and ready.")


# --- Retrieval & Answering Functions ---
def retrieve_chunks(question, k=top_k):
    """
    Encode the question, search the FAISS index, and return top k chunks.
    """
    # Encode the question into an embedding
    question_embedding = model.encode([question])
    question_embedding = np.float32(question_embedding)
    
    # Search the FAISS index for the most similar chunks
    distances, indices = index.search(question_embedding, k)
    
    # Return the text of the retrieved chunks
    retrieved_chunks = [chunks[i] for i in indices[0]]
    return retrieved_chunks

def answer_question(question):
    """
    Retrieve relevant chunks, build a prompt, call the generator, and return the answer.
    """
    # Retrieve the most relevant text chunks
    retrieved_text = retrieve_chunks(question)
    context = "\n\n".join(retrieved_text)
    
    # Build the prompt for the generator model
    prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""
    
    # Generate the answer using the pipeline
    generated_output = generator(prompt, max_length=150, num_return_sequences=1)
    
    # Extract and return the generated text
    answer = generated_output[0]['generated_text']
    return answer


# --- Interactive Loop ---
if __name__ == "__main__":
    print("\nEnter 'exit' or 'quit' to end.")
    while True:
        question = input("\nYour question: ")
        if question.lower() in ("exit", "quit"):
            break
        
        print("\nThinking...")
        answer = answer_question(question)
        print("\nAnswer:", answer)