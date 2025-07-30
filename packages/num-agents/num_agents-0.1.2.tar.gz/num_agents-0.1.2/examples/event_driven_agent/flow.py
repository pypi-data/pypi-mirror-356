"""
Flow definition for the Event-Driven Agent example.

This module defines the flow structure for the agent, including
the nodes and their connections.
"""

from num_agents.core import Flow, Node, SharedStore
from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus
from num_agents.eventbus.event_bus_node import EventEmitterNode, EventListenerNode, EventDrivenBranchNode
from num_agents.scheduler.scheduler import Scheduler
from num_agents.scheduler.scheduler_node import ScheduleTaskNode, WaitForTaskNode

from nodes.user_input_node import UserInputNode
from nodes.data_processor_node import DataProcessorNode
from nodes.notification_node import NotificationNode
from nodes.llm_node import LLMNode


def create_flow(event_bus: EventBus, scheduler: Scheduler, shared: SharedStore = None) -> Flow:
    """
    Create the agent flow with EventBus and Scheduler integration.
    
    Args:
        event_bus: The EventBus instance for event-driven communication
        scheduler: The Scheduler instance for task scheduling
        shared: Optional SharedStore instance to use (creates a new one if None)
        
    Returns:
        The configured Flow instance
    """
    # Create nodes
    user_input_node = UserInputNode(name="UserInputNode")
    
    # Event emitter for user input
    user_input_event_node = EventEmitterNode(
        event_bus=event_bus,
        event_type=EventTypes.USER_INPUT,
        payload_key="user_input",
        name="UserInputEventNode"
    )
    
    # Data processor with scheduled processing
    data_processor_node = DataProcessorNode(name="DataProcessorNode")
    
    # Schedule the data processing task
    schedule_processing_node = ScheduleTaskNode(
        scheduler=scheduler,
        task_name="DataProcessing",
        callback=lambda data: {"processed": data.upper() if isinstance(data, str) else data},
        args_key="user_input",
        task_id_output_key="processing_task_id",
        name="ScheduleProcessingNode"
    )
    
    # Wait for the processing task to complete
    wait_for_processing_node = WaitForTaskNode(
        scheduler=scheduler,
        task_id_key="processing_task_id",
        result_key="processed_data",
        name="WaitForProcessingNode"
    )
    
    # Event emitter for processed data
    data_processed_event_node = EventEmitterNode(
        event_bus=event_bus,
        event_type=EventTypes.custom("data.processed"),
        payload_key="processed_data",
        name="DataProcessedEventNode"
    )
    
    # LLM node for generating responses
    llm_node = LLMNode(name="LLMNode")
    
    # Event listener for system notifications
    notification_listener_node = EventListenerNode(
        event_bus=event_bus,
        event_type=EventTypes.custom("system.notification"),
        output_key="notification",
        timeout=1.0,  # Short timeout since we don't want to block the flow
        name="NotificationListenerNode"
    )
    
    # Notification node
    notification_node = NotificationNode(name="NotificationNode")
    
    # Event-driven branch for different types of user requests
    branch_node = EventDrivenBranchNode(
        event_bus=event_bus,
        event_branches={
            EventTypes.custom("request.process"): data_processor_node,
            EventTypes.custom("request.notify"): notification_node
        },
        default_branch=llm_node,  # Default to LLM if no specific event
        timeout=2.0,
        name="BranchNode"
    )
    
    # Create the flow
    flow = Flow()
    
    # Use the provided shared store if available
    if shared:
        flow.shared = shared
    
    # Add nodes to the flow
    flow.add_node(user_input_node)
    flow.add_node(user_input_event_node)
    flow.add_node(branch_node)
    flow.add_node(data_processor_node)
    flow.add_node(schedule_processing_node)
    flow.add_node(wait_for_processing_node)
    flow.add_node(data_processed_event_node)
    flow.add_node(llm_node)
    flow.add_node(notification_listener_node)
    flow.add_node(notification_node)
    
    # Define the flow structure
    flow.add_transition(user_input_node, user_input_event_node)
    flow.add_transition(user_input_event_node, branch_node)
    
    # Data processing path
    flow.add_transition(data_processor_node, schedule_processing_node)
    flow.add_transition(schedule_processing_node, wait_for_processing_node)
    flow.add_transition(wait_for_processing_node, data_processed_event_node)
    flow.add_transition(data_processed_event_node, llm_node)
    
    # All paths eventually lead to the LLM node
    flow.add_transition(notification_node, llm_node)
    
    # After LLM, check for notifications
    flow.add_transition(llm_node, notification_listener_node)
    
    # Loop back to user input
    flow.add_transition(notification_listener_node, user_input_node)
    
    # Set the start node
    flow.set_start(user_input_node)
    
    return flow
