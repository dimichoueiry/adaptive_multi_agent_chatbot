import asyncio
from demo.src.agents.concordia_cs_agent import ConcordiaCSAgent
from demo.src.knowledge.vector_store import VectorStore

async def test_agent():
    # Initialize the vector store
    vector_store = VectorStore(collection_name="concordia_cs")
    
    # Initialize the agent
    agent = ConcordiaCSAgent(
        name="Concordia CS Advisor",
        description="I am a specialized assistant for Concordia University's Computer Science program admissions.",
        model="llama3.2"
    )
    agent.knowledge_enhancer.vector_store = vector_store
    
    # Test queries
    test_queries = [
        "What are the admission requirements for international students?",
        "What is the minimum GPA required for the Computer Science program?",
        "When is the application deadline for Fall 2024?",
        "Do I need to submit English language test scores?"
    ]
    
    print("Testing ConcordiaCSAgent with enhanced knowledge retrieval...")
    print("-" * 80)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        response = await agent.process_query(query)
        print(f"Response: {response}")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(test_agent()) 