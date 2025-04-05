
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

examples = [
    {
        "input": "List all customers from India.",
        "query": "SELECT * FROM dim_customer WHERE market = 'India';"
    },
    {
        "input": "Get distinct markets available in the database.",
        "query": "SELECT DISTINCT market FROM dim_market;"
    },
    {
        "input": "Find all products that fall under the 'Peripherals' segment.",
        "query": "SELECT * FROM dim_product WHERE segment = 'Peripherals';"
    },
    {
        "input": "How many customers are there in each market?",
        "query": "SELECT market, COUNT(DISTINCT customer) AS customer_count FROM dim_customer GROUP BY market;"
    },
    {
        "input": "Count the number of unique product variants available.",
        "query": "SELECT COUNT(DISTINCT variant) AS variant_count FROM dim_product;"
    },
    {
        "input": "Get all product codes and their categories for 'Internal HDD' category.",
        "query": "SELECT product_code, category FROM dim_product WHERE category = 'Internal HDD';"
    },
    {
        "input": "Find all customers using the 'E-Commerce' platform.",
        "query": "SELECT * FROM dim_customer WHERE platform = 'E-Commerce';"
    },
    {
        "input": "Get the number of products available in each variant.",
        "query": "SELECT variant, COUNT(*) AS product_count FROM dim_product GROUP BY variant;"
    },
    {
        "input": "Which markets belong to the APAC region?",
        "query": "SELECT market FROM dim_market WHERE region = 'APAC';"
    },
    {
        "input": "Show the list of customers along with their platform and market.",
        "query": "SELECT customer, platform, market FROM dim_customer;"
    }
]
@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embedding_model,
        vectorstore,
        k=2,
        input_keys=["input"],
    )
    return example_selector
    
# Initialize the embedding model (Google's)
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create vectorstore using FAISS (in-memory)
vectorstore = FAISS.from_texts(
    [example["input"] for example in examples],
    embedding_model,
)