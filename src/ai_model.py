import os
import openai
from dotenv import load_dotenv
from loguru import logger
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI as LlamaOpenAI

#load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

logger.add("logs/app.log", rotation="10 MB", level="DEBUG")

service_context = ServiceContext.from_defaults(
    llm=LlamaOpenAI(model="gpt-4")
)

# Build index
def build_food_index(data_path: str = "data") -> VectorStoreIndex:
    try:
        documents = SimpleDirectoryReader(data_path).load_data()
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        logger.info("Food Knowledge Index built successfully.")
        return index
    except Exception as e:
        logger.error(f"Error building Food Knowledge Index: {str(e)}")
        return None

# Ask question from index
def query_nutrition_knowledge(question: str) -> str:
    try:
        index = build_food_index()
        if not index:
            return "Failed to build the index. Please check the logs for more details."
        query_engine = index.as_query_engine()
        response = query_engine.query(question)
        logger.info(f"Query executed: {question}")
        return str(response)
    except Exception as e:
        logger.error(f"Error querying the index: {str(e)}")
        return "An error occurred while processing your request. Please try again later."


def get_nutrition_info(food_item: str) -> str:
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a food nutrition expert."},
                {"role": "user", "content": f"Provide detailed nutritional information for {food_item}."}
            ]
        )
        nutrition_data = response.choices[0].message.content
        logger.info(f"Nutritional information for {food_item} retrieved successfully.")
        return nutrition_data
    except Exception as e:
        logger.error(f"Error retrieving nutritional information for {food_item}: {str(e)}")
        return None

