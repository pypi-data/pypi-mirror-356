class Node:
    """Base class for all reasoning nodes."""
    def __init__(self, name: str):
        self.name = name
    
    def _run(self, shared_store: 'SharedStore') -> 'SharedStore':
        raise NotImplementedError("Subclasses must implement this method")
