"""
Parallel Flow for the Nüm Agents SDK.

This module provides classes for implementing parallel execution of nodes or sub-flows,
allowing for concurrent processing in agent workflows.
"""

import asyncio
import concurrent.futures
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from num_agents.core import Flow, Node, SharedStore


class ExecutionMode(Enum):
    """Enum for different execution modes of parallel nodes."""
    
    THREAD = "thread"  # Execute nodes in separate threads
    PROCESS = "process"  # Execute nodes in separate processes
    ASYNC = "async"  # Execute nodes asynchronously using asyncio


class ParallelNode(Node):
    """
    A node that can be executed in parallel with other nodes.
    
    This class extends the base Node class to add support for parallel execution,
    allowing the node to be run in a separate thread, process, or asynchronously.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        execution_mode: ExecutionMode = ExecutionMode.THREAD,
        timeout: Optional[float] = None
    ) -> None:
        """
        Initialize a parallel node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            execution_mode: The execution mode for this node
            timeout: Optional timeout in seconds for the node's execution
        """
        super().__init__(name, shared_store)
        self.execution_mode = execution_mode
        self.timeout = timeout
        self._result = None
        self._exception = None
    
    async def process_async(self) -> None:
        """
        Process the node asynchronously.
        
        This method is used when the node is executed in ASYNC mode.
        """
        try:
            self._process()
            self._result = True
        except Exception as e:
            self._exception = e
            self._result = False
    
    def process_with_timeout(self) -> None:
        """
        Process the node with a timeout.
        
        This method is used when the node is executed in THREAD or PROCESS mode.
        """
        try:
            self._process()
            self._result = True
        except Exception as e:
            self._exception = e
            self._result = False
    
    @property
    def result(self) -> Any:
        """Get the result of the node's execution."""
        return self._result
    
    @property
    def exception(self) -> Optional[Exception]:
        """Get any exception that occurred during the node's execution."""
        return self._exception
    
    def was_successful(self) -> bool:
        """Check if the node's execution was successful."""
        return self._result is True and self._exception is None


class ParallelGroup:
    """
    A group of nodes that can be executed in parallel.
    
    This class represents a group of nodes that should be executed in parallel,
    with options for synchronization and error handling.
    """
    
    def __init__(
        self,
        name: str,
        nodes: List[ParallelNode],
        execution_mode: ExecutionMode = ExecutionMode.THREAD,
        timeout: Optional[float] = None,
        max_workers: Optional[int] = None,
        continue_on_error: bool = False
    ) -> None:
        """
        Initialize a parallel group.
        
        Args:
            name: The name of the group
            nodes: The list of nodes in the group
            execution_mode: The execution mode for this group
            timeout: Optional timeout in seconds for the group's execution
            max_workers: Optional maximum number of workers to use
            continue_on_error: Whether to continue executing other nodes if one fails
        """
        self.name = name
        self.nodes = nodes
        self.execution_mode = execution_mode
        self.timeout = timeout
        self.max_workers = max_workers
        self.continue_on_error = continue_on_error
        
        # Set the execution mode for all nodes in the group
        for node in self.nodes:
            node.execution_mode = execution_mode
    
    async def execute_async(self) -> bool:
        """
        Execute the nodes in the group asynchronously.
        
        This method is used when the group is executed in ASYNC mode.
        
        Returns:
            True if all nodes executed successfully, False otherwise
        """
        tasks = []
        for node in self.nodes:
            tasks.append(asyncio.create_task(node.process_async()))
        
        if self.timeout:
            # Execute with timeout
            try:
                await asyncio.wait_for(asyncio.gather(*tasks), timeout=self.timeout)
                return all(node.was_successful() for node in self.nodes)
            except asyncio.TimeoutError:
                # Handle timeout
                for task in tasks:
                    task.cancel()
                return False
            except Exception:
                # Handle other exceptions
                if not self.continue_on_error:
                    for task in tasks:
                        task.cancel()
                return False
        else:
            # Execute without timeout
            try:
                await asyncio.gather(*tasks)
                return all(node.was_successful() for node in self.nodes)
            except Exception:
                # Handle exceptions
                if not self.continue_on_error:
                    for task in tasks:
                        task.cancel()
                return False
    
    def execute_threaded(self) -> bool:
        """
        Execute the nodes in the group using threads.
        
        This method is used when the group is executed in THREAD mode.
        
        Returns:
            True if all nodes executed successfully, False otherwise
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for node in self.nodes:
                futures.append(executor.submit(node.process_with_timeout))
            
            if self.timeout:
                # Execute with timeout
                try:
                    concurrent.futures.wait(futures, timeout=self.timeout)
                    # Check if all futures are done
                    if not all(future.done() for future in futures):
                        # Cancel any futures that are not done
                        for future in futures:
                            if not future.done():
                                future.cancel()
                        return False
                    return all(node.was_successful() for node in self.nodes)
                except Exception:
                    # Handle exceptions
                    if not self.continue_on_error:
                        for future in futures:
                            if not future.done():
                                future.cancel()
                    return False
            else:
                # Execute without timeout
                try:
                    concurrent.futures.wait(futures)
                    return all(node.was_successful() for node in self.nodes)
                except Exception:
                    # Handle exceptions
                    if not self.continue_on_error:
                        for future in futures:
                            if not future.done():
                                future.cancel()
                    return False
    
    def execute_multiprocess(self) -> bool:
        """
        Execute the nodes in the group using processes.
        
        This method is used when the group is executed in PROCESS mode.
        
        Returns:
            True if all nodes executed successfully, False otherwise
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for node in self.nodes:
                futures.append(executor.submit(node.process_with_timeout))
            
            if self.timeout:
                # Execute with timeout
                try:
                    concurrent.futures.wait(futures, timeout=self.timeout)
                    # Check if all futures are done
                    if not all(future.done() for future in futures):
                        # Cancel any futures that are not done
                        for future in futures:
                            if not future.done():
                                future.cancel()
                        return False
                    return all(node.was_successful() for node in self.nodes)
                except Exception:
                    # Handle exceptions
                    if not self.continue_on_error:
                        for future in futures:
                            if not future.done():
                                future.cancel()
                    return False
            else:
                # Execute without timeout
                try:
                    concurrent.futures.wait(futures)
                    return all(node.was_successful() for node in self.nodes)
                except Exception:
                    # Handle exceptions
                    if not self.continue_on_error:
                        for future in futures:
                            if not future.done():
                                future.cancel()
                    return False
    
    def execute(self) -> bool:
        """
        Execute the nodes in the group.
        
        This method executes the nodes in the group using the specified execution mode.
        
        Returns:
            True if all nodes executed successfully, False otherwise
        """
        if self.execution_mode == ExecutionMode.ASYNC:
            # Create an event loop if one doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            return loop.run_until_complete(self.execute_async())
        
        elif self.execution_mode == ExecutionMode.THREAD:
            return self.execute_threaded()
        
        elif self.execution_mode == ExecutionMode.PROCESS:
            return self.execute_multiprocess()
        
        # Default to sequential execution
        for node in self.nodes:
            try:
                node.process()
            except Exception as e:
                node._exception = e
                node._result = False
                if not self.continue_on_error:
                    return False
        
        return all(node.was_successful() for node in self.nodes)


class ParallelFlow(Flow):
    """
    A flow that can execute groups of nodes in parallel.
    
    This class extends the base Flow class to add support for parallel execution,
    allowing groups of nodes to be run concurrently.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        node_groups: List[Union[Node, ParallelGroup]]
    ) -> None:
        """
        Initialize a parallel flow.
        
        Args:
            name: The name of the flow
            shared_store: The shared store for the agent
            node_groups: A list of nodes or parallel groups to execute
        """
        # Extract all nodes for the parent class
        all_nodes = []
        for group in node_groups:
            if isinstance(group, ParallelGroup):
                all_nodes.extend(group.nodes)
            else:
                all_nodes.append(group)
        
        super().__init__(name, shared_store, all_nodes)
        self.node_groups = node_groups
    
    def run(self) -> None:
        """
        Run the flow with parallel execution.
        
        This method executes the nodes or groups in the flow, with parallel
        groups being executed concurrently.
        """
        for group in self.node_groups:
            if isinstance(group, ParallelGroup):
                # Execute the group in parallel
                group.execute()
            else:
                # Execute the node sequentially
                group.process()


class SubFlow(Flow):
    """
    A flow that can be used as a node in another flow.
    
    This class extends the base Flow class to allow it to be used as a node
    in another flow, enabling hierarchical flow composition.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        nodes: List[Node]
    ) -> None:
        """
        Initialize a sub-flow.
        
        Args:
            name: The name of the flow
            shared_store: The shared store for the agent
            nodes: The list of nodes in the flow
        """
        super().__init__(name, shared_store, nodes)
    
    def process(self) -> None:
        """
        Process the sub-flow as a node.
        
        This method allows the sub-flow to be used as a node in another flow.
        """
        self.run()


class ParallelSubFlow(SubFlow, ParallelNode):
    """
    A sub-flow that can be executed in parallel with other nodes.
    
    This class combines the SubFlow and ParallelNode classes to create a sub-flow
    that can be executed in parallel with other nodes.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        nodes: List[Node],
        execution_mode: ExecutionMode = ExecutionMode.THREAD,
        timeout: Optional[float] = None
    ) -> None:
        """
        Initialize a parallel sub-flow.
        
        Args:
            name: The name of the flow
            shared_store: The shared store for the agent
            nodes: The list of nodes in the flow
            execution_mode: The execution mode for this flow
            timeout: Optional timeout in seconds for the flow's execution
        """
        SubFlow.__init__(self, name, shared_store, nodes)
        ParallelNode.__init__(self, name, shared_store, execution_mode, timeout)
    
    def _process(self) -> None:
        """
        Process the sub-flow.
        
        This method is called by the ParallelNode's process method.
        """
        self.run()
