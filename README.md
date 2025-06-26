# Retrieval_AG

Document Description:


Five Deep Questions/Answers:

Question 1: What is the significance of the embedding model's dimensionality (d=768 for all-distilroberta-v1), and how does it impact the FAISS index?

Answer: The dimensionality of an embedding model is the size of the vector it produces for a given piece of text. In this case, every chunk is converted into a 768-number vector. This dimension is critical because it represents the richness of the semantic information captured. A higher dimension can potentially capture more nuanced meaning, but at the cost of computational resources. For FAISS, this d value is a fundamental parameter (IndexFlatL2(d)). It dictates the structure of the index and the space required. All vectors added to the index, including the query vector, must have this exact dimension for the similarity search (L2 distance calculation) to work.

Question 2: Explain the IndexFlatL2 search method in FAISS. What are its pros and cons compared to other index types?

Answer: IndexFlatL2 performs an exhaustive, brute-force search. When you provide a query vector, it calculates the L2 (Euclidean) distance between the query vector and every single other vector in the index. It then sorts these distances to find the "nearest" (most similar) neighbors.

Pros: It is 100% accurate, guaranteeing it will find the absolute closest vectors because it checks every possibility. It's also simple and requires no training time.
Cons: It is very slow for large datasets. Since the search complexity is linear with the number of vectors, it does not scale well to millions or billions of items. Other index types, like IndexIVFFlat, partition the data and only search a subset of vectors, making them much faster but potentially sacrificing some accuracy (i.e., they might not find the absolute best match).
Question 3: How does the relationship between chunk_size and chunk_overlap affect what context is available to the model? What's a potential risk of having zero overlap?

Answer: chunk_size determines the maximum amount of text in a single retrievable unit. chunk_overlap creates redundant information at the boundaries of adjacent chunks. This overlap is crucial for semantic continuity. For example, if a sentence that is key to understanding a concept starts at the very end of one chunk and finishes at the beginning of the next, having zero overlap would split this sentence. Neither chunk alone would have the full context. By having an overlap (e.g., 50 characters), the entire sentence is likely to be fully contained in at least one of the two chunks, making it more likely to be retrieved correctly. The risk of zero overlap is context fragmentation and the loss of critical information that spans chunk boundaries.

Question 4: Describe the prompt engineering being done in the answer_question function. Why is it important to explicitly tell the model to use only the provided context?

Answer: The prompt in answer_question is carefully structured to guide the language model's behavior. It's not just the question; it's a template that includes:

An instruction: Use the following context to answer the question.
A fallback behavior: If you don't know the answer, say you don't know.
Clearly delineated context: The retrieved chunks are formatted under a Context: heading.
The user's query: The original question is placed under a Question: heading.
This is crucial because pre-trained language models (like Flan-T5) have vast amounts of "parametric knowledge" from their training data. Without the instruction to stick to the context, the model might ignore the retrieved chunks and answer based on its pre-existing knowledge, which defeats the entire purpose of RAG. The fallback instruction helps prevent "hallucination," where the model makes up an answer when the context doesn't contain the necessary information.

Question 5: The HuggingFace pipeline is loaded with device=-1. What does this parameter do, and what is the performance implication for this RAG system?

Answer: The device=-1 parameter instructs the HuggingFace pipeline to run the model on the CPU. If a GPU were available and properly configured with CUDA, one could set device=0 (for the first GPU) to accelerate the computation. The performance implication is significant: text generation (the generator step) will be much slower on a CPU than on a GPU. For this specific application, where we generate answers one at a time in an interactive loop, the delay is often acceptable. However, in a high-throughput or production environment, running the generator model on a CPU would likely be a major bottleneck. The embedding step, while also computationally intensive, is only done once upfront.


Analysis:

Chunk_size vs overlap:
chunk_size controls the physical length of information, so if you have a chunk_size of say 50, you are breaking you document down into sections of 50 characters

chunk_overlap handles the consistency of information between sections, so if you have a chunk_overlap of 50 this will essentially say that the last 50 characters of section 1 and the first 50 of section 2 are the same

Small Chunk/Overlap:
Creates very specific, dense chunks of information. When you as a very specific question, it does a much better job at grabbing the relevant information than it does when you ask it much broader questions like when or why.

Overall this provided fairly accurate information but it really depended on how i asked the question(and the accuracy of the wiki). For instance if I asked it how many different GTR models there are, it would always tell me 2 road ready models. Which is technically true but I had to get more specific in the way i asked the question to get the list of every model.

Large Chunk/overlap:
This works the exact opposite of Small Chuck and is much better at providing broader answer. It does a better job at understanding how one section of the document relates to another so it handles open-ended questions much better.

This provided essentially the same accuracy but I did not have to be as specific. So when asked the same question as above it was able to get to the answer that i wanted much easier since it was able to view the entire document and all compare all relevent information although this would tend to provide unecessary information along with the relevant.

Suggestions:
To be entirely honest I do not have any suggestions or recommendations for the project.
