"""
Example Event-Driven Agent using Nüm Agents SDK.

This example demonstrates how to use the EventBus and Scheduler
components to create an event-driven agent.
"""

import asyncio
import logging
from datetime import datetime, timedelta

from num_agents.core import Flow, SharedStore
from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus
from num_agents.scheduler.scheduler import Scheduler

from flow import create_flow


async def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    
    # Create EventBus and Scheduler
    event_bus = EventBus()
    scheduler = Scheduler(event_bus=event_bus)
    
    # Create a shared store
    shared = SharedStore()
    
    # Create the agent flow
    flow = create_flow(event_bus, scheduler, shared)
    
    # Subscribe to system events for logging
    event_bus.subscribe(
        EventTypes.FLOW_STARTED,
        lambda e: logger.info(f"Flow started: {e.payload.get('flow_name')}")
    )
    event_bus.subscribe(
        EventTypes.FLOW_COMPLETED,
        lambda e: logger.info(f"Flow completed: {e.payload.get('flow_name')}")
    )
    event_bus.subscribe(
        EventTypes.NODE_STARTED,
        lambda e: logger.debug(f"Node started: {e.payload.get('node_name')}")
    )
    event_bus.subscribe(
        EventTypes.NODE_COMPLETED,
        lambda e: logger.debug(f"Node completed: {e.payload.get('node_name')}")
    )
    
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started")
    
    try:
        # Publish initial system startup event
        event_bus.publish(
            Event(
                event_type=EventTypes.SYSTEM_STARTUP,
                payload={"timestamp": datetime.now().isoformat()},
                source="System"
            )
        )
        
        # Execute the flow
        logger.info("Starting agent flow")
        results = flow.execute()
        logger.info(f"Flow execution completed with results: {results}")
        
        # Keep the application running to allow scheduled tasks to execute
        logger.info("Agent is running. Press Ctrl+C to exit.")
        while True:
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("Shutting down agent")
        
        # Publish system shutdown event
        event_bus.publish(
            Event(
                event_type=EventTypes.SYSTEM_SHUTDOWN,
                payload={"timestamp": datetime.now().isoformat()},
                source="System"
            )
        )
        
        # Stop the scheduler
        scheduler.stop()
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    asyncio.run(main())
