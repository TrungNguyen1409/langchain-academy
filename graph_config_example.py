"""
Example of extended LangGraph configuration with graph database integration
"""

import os
from typing import Dict, Any, Optional
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.graph import CompiledGraph

class GraphConfigBuilder:
    """Builder class for creating comprehensive LangGraph configurations"""
    
    def __init__(self):
        self.config = {"configurable": {}}
    
    def add_thread_id(self, thread_id: str) -> 'GraphConfigBuilder':
        """Add thread ID for conversation tracking"""
        self.config["configurable"]["thread_id"] = thread_id
        return self
    
    def add_user_context(self, user_id: str, session_id: str) -> 'GraphConfigBuilder':
        """Add user and session context"""
        self.config["configurable"]["user_id"] = user_id
        self.config["configurable"]["session_id"] = session_id
        return self
    
    def add_neo4j_graph(self, uri: str, user: str, password: str, database: str = "neo4j") -> 'GraphConfigBuilder':
        """Add Neo4j graph database configuration"""
        self.config["configurable"]["graph_db"] = {
            "type": "neo4j",
            "uri": uri,
            "user": user,
            "password": password,
            "database": database
        }
        return self
    
    def add_sqlite_graph(self, db_path: str) -> 'GraphConfigBuilder':
        """Add SQLite graph database configuration"""
        self.config["configurable"]["graph_db"] = {
            "type": "sqlite",
            "path": db_path
        }
        return self
    
    def add_memory_config(self, memory_type: str, **kwargs) -> 'GraphConfigBuilder':
        """Add memory configuration"""
        self.config["configurable"]["memory"] = {
            "type": memory_type,
            **kwargs
        }
        return self
    
    def add_checkpointing(self, checkpoint_path: str) -> 'GraphConfigBuilder':
        """Add checkpointing configuration"""
        self.config["configurable"]["checkpoint_store"] = SqliteSaver.from_conn_string(checkpoint_path)
        return self
    
    def add_custom_metadata(self, **metadata) -> 'GraphConfigBuilder':
        """Add custom metadata to configuration"""
        self.config["configurable"]["metadata"] = metadata
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build and return the final configuration"""
        return self.config

# Example usage
def create_advanced_config():
    """Create an advanced configuration with graph database"""
    
    # Basic configuration
    config = (GraphConfigBuilder()
              .add_thread_id("conversation_1")
              .add_user_context("user123", "session456")
              .add_neo4j_graph(
                  uri="bolt://localhost:7687",
                  user="neo4j",
                  password=os.getenv("NEO4J_PASSWORD", "password"),
                  database="langgraph"
              )
              .add_memory_config(
                  memory_type="neo4j",
                  collection="conversations",
                  max_tokens=4000
              )
              .add_checkpointing("sqlite:///checkpoints.db")
              .add_custom_metadata(
                  environment="production",
                  version="1.0.0",
                  features=["graph_db", "memory", "checkpointing"]
              )
              .build())
    
    return config

# Example with SQLite graph database
def create_sqlite_config():
    """Create configuration with SQLite graph database"""
    
    config = (GraphConfigBuilder()
              .add_thread_id("thread_2")
              .add_sqlite_graph("./knowledge_graph.db")
              .add_memory_config(
                  memory_type="sqlite",
                  table="conversation_memory"
              )
              .add_custom_metadata(
                  graph_schema={
                      "nodes": ["concepts", "entities", "relationships"],
                      "edges": ["relates_to", "part_of", "similar_to"]
                  }
              )
              .build())
    
    return config

# Example usage in your agent
if __name__ == "__main__":
    # Create advanced config
    advanced_config = create_advanced_config()
    print("Advanced Config:")
    print(advanced_config)
    
    print("\n" + "="*50 + "\n")
    
    # Create SQLite config
    sqlite_config = create_sqlite_config()
    print("SQLite Config:")
    print(sqlite_config)
    
    # Example of using the config with your agent
    # messages = [HumanMessage(content="Add 3 and 4.")]
    # result = react_graph_memory.invoke({"messages": messages}, advanced_config)
