"""
LLM Node for the Event-Driven Agent example.

This node handles interactions with a language model and demonstrates
how to integrate LLM capabilities into an event-driven agent.
"""

from typing import Any, Dict

from num_agents.core import Node, SharedStore


class LLMNode(Node):
    """
    Node for interacting with a language model.
    
    This node simulates interactions with an LLM and demonstrates
    how to process inputs and outputs in an event-driven context.
    """
    
    def __init__(self, name: str = None) -> None:
        """
        Initialize an LLM node.
        
        Args:
            name: Optional name for the node
        """
        super().__init__(name or "LLMNode")
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node simulates generating a response from an LLM based on
        the user input and any processed data.
        
        Args:
            shared: The shared store for accessing and storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Get the user input from the shared store
        user_input = shared.get("user_input", "")
        
        # Get any processed data if available
        processed_data = shared.get("processed_data", None)
        
        # Generate a response using the LLM
        response = self._generate_response(user_input, processed_data)
        
        # Store the response in the shared store
        shared.set("llm_response", response)
        
        # Print the response
        print(f"\n[ASSISTANT] {response}\n")
        
        return {
            "llm_response": response
        }
    
    def _generate_response(self, user_input: str, processed_data: Any) -> str:
        """
        Generate a response using the LLM.
        
        In a real application, this would call an actual LLM API.
        
        Args:
            user_input: The user's input string
            processed_data: Any processed data to include in the response
            
        Returns:
            The generated response
        """
        # In a real application, this would use an LLM API like OpenAI
        # to generate a response
        
        # Simulate an LLM response based on the input and processed data
        if processed_data:
            if isinstance(processed_data, dict) and "processed_data" in processed_data:
                processed_text = processed_data["processed_data"]
                word_count = processed_data.get("word_count", 0)
                return (
                    f"I've processed your input: '{user_input}'\n"
                    f"The processed result is: '{processed_text}'\n"
                    f"Word count: {word_count}"
                )
            else:
                return f"I've processed your input: '{user_input}'\nThe result is: {processed_data}"
        else:
            # Generate a response based on keywords in the user input
            if "help" in user_input.lower():
                return (
                    "I can help you with the following:\n"
                    "- Process data (try 'process this text')\n"
                    "- Send notifications (try 'remind me to check emails')\n"
                    "- Answer questions about the Nüm Agents SDK"
                )
            elif any(word in user_input.lower() for word in ["hello", "hi", "hey"]):
                return "Hello! I'm an event-driven agent built with the Nüm Agents SDK. How can I assist you today?"
            else:
                return f"I received your input: '{user_input}'. What would you like me to do with this information?"
