"""Shared configuration for Lab 18."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", OPENAI_API_KEY)

def get_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI
    import os
    keys = [
        os.getenv("GOOGLE_API_KEY1"),
        os.getenv("GOOGLE_API_KEY2"),
        os.getenv("GOOGLE_API_KEY3"),
        os.getenv("GOOGLE_API_KEY4")
    ]
    keys = [k for k in keys if k]
    if not keys:
        keys = [os.getenv("GOOGLE_API_KEY")]
    
    
    # Monkey-patch to fix Ragas temperature bug
    original_agenerate = ChatGoogleGenerativeAI._agenerate
    original_generate = ChatGoogleGenerativeAI._generate
    
    async def patched_agenerate(self, messages, stop=None, run_manager=None, **kwargs):
        kwargs.pop("temperature", None)
        return await original_agenerate(self, messages, stop=stop, run_manager=run_manager, **kwargs)
        
    def patched_generate(self, messages, stop=None, run_manager=None, **kwargs):
        kwargs.pop("temperature", None)
        return original_generate(self, messages, stop=stop, run_manager=run_manager, **kwargs)
        
    ChatGoogleGenerativeAI._agenerate = patched_agenerate
    ChatGoogleGenerativeAI._generate = patched_generate
    
    llms = [ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=k, max_retries=0) for k in keys]
    return llms[0].with_fallbacks(llms[1:])

# --- Qdrant ---
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "lab18_production"
NAIVE_COLLECTION = "lab18_naive"

# --- Embedding ---
EMBEDDING_MODEL = "BAAI/bge-m3"
EMBEDDING_DIM = 1024

# --- Chunking ---
HIERARCHICAL_PARENT_SIZE = 2048
HIERARCHICAL_CHILD_SIZE = 256
SEMANTIC_THRESHOLD = 0.85

# --- Search ---
BM25_TOP_K = 20
DENSE_TOP_K = 20
HYBRID_TOP_K = 20
RERANK_TOP_K = 3

# --- Paths ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_SET_PATH = os.path.join(os.path.dirname(__file__), "test_set.json")
