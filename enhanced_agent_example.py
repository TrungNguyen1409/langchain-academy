"""
Enhanced agent example with graph database integration
"""

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import os

# Example tools
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@tool
def get_weather(city: str) -> str:
    """Get the current weather in a city."""
    return f"The weather in {city} is sunny and 72°F"

# Create the agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [add_numbers, get_weather]
agent = create_react_agent(llm, tools)

# Enhanced configuration with graph database
def create_enhanced_config(thread_id: str = "1"):
    """Create an enhanced configuration with graph database support"""
    
    return {
        "configurable": {
            "thread_id": thread_id,
            "user_id": "user123",
            "session_id": "session456",
            
            # Graph database configuration
            "graph_db": {
                "type": "sqlite",
                "path": "./knowledge_graph.db",
                "schema": {
                    "nodes": ["concepts", "entities", "relationships"],
                    "edges": ["relates_to", "part_of", "similar_to"]
                }
            },
            
            # Memory configuration
            "memory": {
                "type": "sqlite",
                "table": "conversation_memory",
                "max_tokens": 4000,
                "retention_days": 30
            },
            
            # Checkpointing
            "checkpoint_store": SqliteSaver.from_conn_string("sqlite:///checkpoints.db"),
            
            # Custom metadata
            "metadata": {
                "environment": "development",
                "version": "1.0.0",
                "features": ["graph_db", "memory", "checkpointing"],
                "graph_queries": {
                    "find_related": "MATCH (n)-[r]->(m) WHERE n.id = $node_id RETURN m, r",
                    "get_entities": "MATCH (n:entity) RETURN n LIMIT 10"
                }
            }
        }
    }

# Example usage
def run_enhanced_agent():
    """Run the agent with enhanced configuration"""
    
    # Create enhanced config
    config = create_enhanced_config("conversation_1")
    
    # Specify input
    messages = [HumanMessage(content="Add 3 and 4, then tell me about the weather in Paris.")]
    
    # Run with enhanced config
    result = agent.invoke({"messages": messages}, config)
    
    # Print results
    print("Enhanced Agent Result:")
    for message in result['messages']:
        message.pretty_print()
    
    return result

# Graph database integration example
def integrate_with_graph_db():
    """Example of how to integrate with a graph database"""
    
    config = create_enhanced_config("graph_conversation")
    
    # Add graph database operations to your agent
    graph_operations = {
        "store_entity": lambda entity: f"Stored entity: {entity}",
        "find_relationships": lambda entity: f"Found relationships for: {entity}",
        "query_graph": lambda query: f"Executed query: {query}"
    }
    
    # Enhanced config with graph operations
    config["configurable"]["graph_operations"] = graph_operations
    
    return config

if __name__ == "__main__":
    # Example 1: Basic enhanced config
    print("=== Enhanced Configuration Example ===")
    config = create_enhanced_config()
    print("Config structure:")
    for key, value in config["configurable"].items():
        print(f"  {key}: {type(value).__name__}")
    
    print("\n=== Graph Database Integration ===")
    graph_config = integrate_with_graph_db()
    print("Graph operations available:")
    for op_name in graph_config["configurable"]["graph_operations"].keys():
        print(f"  - {op_name}")
    
    # Uncomment to run the actual agent
    # result = run_enhanced_agent()
