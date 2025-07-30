import asyncio
import json
import logging
import time

import zmq
import zmq.asyncio

from .event import NotificationEvent


class AsyncNotificationHub:
    def __init__(self):
        # Use asyncio-compatible ZeroMQ context
        self.context = zmq.asyncio.Context()

        # Receive events from services (PULL socket for load balancing)
        self.collector = self.context.socket(zmq.PULL)
        self.collector.bind("tcp://*:5555")

        # Publish events to subscribers (PUB socket for fan-out)
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:5556")

        # Track statistics
        self.stats = {"events_received": 0, "events_published": 0, "active_subscribers": 0}

        self.running = False
        self.logger = logging.getLogger("notification-hub")

    async def start(self):
        """Start the notification hub"""
        self.running = True
        self.logger.info("Starting Async Notification Hub...")

        # Start concurrent tasks
        tasks = [
            asyncio.create_task(self.event_collector()),
            asyncio.create_task(self.stats_reporter()),
            asyncio.create_task(self.health_check()),
        ]

        try:
            # Run all tasks concurrently
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            self.logger.info("Shutting down...")
            await self.stop()

    async def event_collector(self):
        """Main event collection loop"""
        while self.running:
            try:
                # Receive event from any service (non-blocking with timeout)
                if await self.collector.poll(timeout=1000):  # 1 second timeout
                    message_bytes = await self.collector.recv()
                    message = json.loads(message_bytes.decode())

                    # Create event object
                    event = NotificationEvent(
                        event_type=message["event_type"],
                        source_service=message["source_service"],
                        data=message["data"],
                        timestamp=message.get("timestamp", time.time()),
                        correlation_id=message.get("correlation_id"),
                    )

                    self.logger.info(f"Received: {event.event_type} from {event.source_service}")
                    self.stats["events_received"] += 1

                    # Publish to subscribers
                    await self.publish_event(event)

                await asyncio.sleep(0.001)  # Small yield to prevent busy waiting

            except Exception as e:
                self.logger.error(f"Error in event collector: {e}")
                await asyncio.sleep(1)

    async def publish_event(self, event: NotificationEvent):
        """Publish event to all subscribers"""
        try:
            message = {
                "event_type": event.event_type,
                "source_service": event.source_service,
                "data": event.data,
                "timestamp": event.timestamp,
                "correlation_id": event.correlation_id,
            }

            # Send as multipart message: [topic, data]
            await self.publisher.send_multipart(
                [
                    event.event_type.encode(),  # Topic for filtering
                    json.dumps(message).encode(),  # Event data
                ]
            )

            self.stats["events_published"] += 1
            self.logger.debug(f"Published: {event.event_type}")

        except Exception as exc:
            self.logger.error(f"Error publishing event: {exc}")

    async def stats_reporter(self):
        """Periodically report statistics"""
        while self.running:
            await asyncio.sleep(30)  # Report every 30 seconds
            self.logger.info(f"Stats: {self.stats}")

    async def health_check(self):
        """Simple health check endpoint simulation"""
        while self.running:
            await asyncio.sleep(10)
            # Could implement actual health checks here
            self.logger.debug("Health check: OK")

    async def stop(self):
        """Graceful shutdown"""
        if self.running:
            self.running = False
            self.collector.close()
            self.publisher.close()
            self.context.term()


# Usage
async def run_hub():
    hub = AsyncNotificationHub()
    await hub.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(run_hub())
