import tiktoken
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
import nltk

# If running for the first time:
# nltk.download('wordnet')
# nltk.download('punkt')

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()


def chunk_gpt_tokens(text, chunk_size=200, overlap=50, model_name='text-embedding-3-small'):
    """
    Splits text into GPT tokens of size `chunk_size` with `overlap` tokens overlap.
    """

    # Initialize tokenizer for a given model
    encoding = tiktoken.encoding_for_model(model_name)

    # Encode text into token IDs
    token_ids = encoding.encode(text)

    chunks = []
    start = 0
    while start < len(token_ids):
        end = start + chunk_size
        chunk_tokens = token_ids[start:end]
        start += (chunk_size - overlap)
        # Decode token IDs back to string for the API
        chunk_text = encoding.decode(chunk_tokens)

        lemmatized_words = []
        for word in chunk_text.split():
            lemmatized = lemmatizer.lemmatize(word, wordnet.VERB)  # specifying POS
            lemmatized_words.append(lemmatized)

        lemmatized_text = ' '.join(lemmatized_words)
        # Store results (you could also store token IDs, offsets, etc.)
        chunks.append({
            "raw_text": chunk_text,
            "cleaned_text": lemmatized_text
        })
        # Safety check to avoid infinite loops
        if overlap >= chunk_size:
            break

    return chunks


# Example usage
# text = (
#     "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
#     "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
#     "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris..."
# )

# gpt_chunks = chunk_gpt_tokens(text, chunk_size=200, overlap=50)
#
# print("Number of GPT token chunks:", len(gpt_chunks))
# print("First GPT chunk (decoded as text):", gpt_chunks[0])