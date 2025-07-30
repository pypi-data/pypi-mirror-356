"""
Main PubSub client for managing subscriptions and message processing
"""

import asyncio
import inspect
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from .acknowledgement import Acknowledgement
from .registry import get_registry
from .resources import ResourceManager
from ..utils.serialization import deserialize_event

logger = logging.getLogger(__name__)


class PubSubClient:
    """
    Class to manage Pub/Sub client operations with message handling and subscription listening.

    The PubSubClient class is designed to interact with Google Cloud Pub/Sub. It provides functionality
    to listen to subscriptions, process incoming messages with specific handlers, and manage the lifecycle
    of the Pub/Sub client. It supports a multithreaded approach to process messages concurrently and includes
    flow control mechanisms to regulate message processing. This class can be used for implementing event-driven
    message processing systems where different types of events are handled by specific handlers. The class also
    supports stopping message listening gracefully.

    Attributes:
        project_id (str): The Google Cloud Project ID.
        subscriber (SubscriberClient): A Pub/Sub SubscriberClient instance used for subscription operations.
        executor (ThreadPoolExecutor): A thread pool executor for managing threaded tasks.
        max_messages (int): The maximum number of messages to be pulled concurrently.
        running (bool): Determines whether the client is actively listening to subscriptions.
        streaming_futures (list): List of Pub/Sub streaming pull futures to manage active subscriptions.

    Methods:
        start_listening(timeout: Optional[float]): Begins listening to all registered subscriptions.
        stop_listening(): Stops the active subscription listener and cleans up resources.
        _process_message(message, handlers): Handles incoming messages using registered handlers.
    """

    def __init__(
        self,
        project_id: str,
        max_workers: int = 10,
        max_messages: int = 100,
        auto_create_resources: bool = True,
        resource_config: Optional[Dict[str, Any]] = None,
    ):
        self.project_id = project_id
        self.subscriber = pubsub_v1.SubscriberClient()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.max_messages = max_messages
        self.running = False
        self.streaming_futures = []
        self._start_lock = threading.Lock()

        # Resource management
        self.auto_create_resources = auto_create_resources
        self.resource_config = resource_config or {}
        self.resource_manager = ResourceManager(project_id, auto_create_resources)

    def start_listening(self, timeout: Optional[float] = None, stop_callback=None):
        """
        Starts listening to Pub/Sub subscriptions and processes incoming messages.

        This method sets up the Pub/Sub client to listen to all subscriptions registered in the system,
        and processes incoming messages using the corresponding message handlers. It supports configuring
        a timeout for waiting on incoming messages and ensures that multiple subscriptions can be handled
        concurrently using futures. The method keeps the main execution thread running and relies on
        exceptions or a manual stop signal to terminate the listening process.

        Parameters:
            timeout (Optional[float]): Maximum time in seconds to wait for messages. If not provided, the
            listener will run indefinitely until manually stopped or interrupted.
            stop_callback (Optional[callable]): A callback function that returns True when listening should stop.

        Raises:
            TimeoutError: If processing of messages exceeds the specified timeout duration.
            KeyboardInterrupt: If the listener is manually interrupted via keyboard signal.
        """
        with self._start_lock:
            if self.running:
                logger.warning("Client is already listening")
                return

            self.running = True
        registry = get_registry()

        # Check if there are any subscriptions to listen to
        subscriptions = registry.get_all_subscriptions()
        if not subscriptions:
            logger.warning("No subscriptions registered, nothing to listen to")
            return

        # Ensure all resources exist before starting to listen
        try:
            if self.auto_create_resources:
                logger.info("Ensuring topics and subscriptions exist...")
                subscription_paths = self.resource_manager.ensure_resources_for_subscriptions(
                    subscriptions
                )
                logger.info(f"Successfully verified {len(subscription_paths)} subscription(s)")
            else:
                logger.info("Verifying topics and subscriptions exist (auto-creation disabled)...")
                # When auto-creation is disabled, we still need to verify resources exist
                for subscription_name in subscriptions.keys():
                    subscription_path = self.subscriber.subscription_path(
                        self.project_id, subscription_name
                    )
                    if not self.resource_manager._subscription_exists(subscription_path):
                        raise ValueError(
                            f"Subscription '{subscription_name}' does not exist and auto_create_resources is disabled"
                        )
                logger.info(f"Successfully verified {len(subscriptions)} subscription(s) exist")
        except Exception as e:
            logger.error(f"Failed to verify resources: {e}")
            self.running = False
            raise

        for subscription_name, handlers in subscriptions.items():
            subscription_path = self.subscriber.subscription_path(
                self.project_id, subscription_name
            )

            logger.info(f"Starting to listen on subscription: {subscription_path}")

            def callback(message, handlers=handlers):
                self._process_message(message, handlers)

            # Configure flow control settings
            flow_control = pubsub_v1.types.FlowControl(max_messages=self.max_messages)

            streaming_pull_future = self.subscriber.subscribe(
                subscription_path, callback=callback, flow_control=flow_control
            )
            self.streaming_futures.append(streaming_pull_future)
            logger.info(f"Listening for messages on {subscription_path}")

        # Keep the main thread running
        try:
            logger.info("PubSub listener started. Press Ctrl+C to stop.")

            if timeout:
                # Run with timeout
                import time

                start_time = time.time()
                while self.running and (time.time() - start_time) < timeout:
                    if stop_callback and stop_callback():
                        logger.info("Stop callback triggered, stopping listener")
                        break
                    time.sleep(0.1)
                if self.running and (time.time() - start_time) >= timeout:
                    logger.info("Timeout reached, stopping listener")
            else:
                # Run indefinitely until stopped
                while self.running:
                    try:
                        if stop_callback and stop_callback():
                            logger.info("Stop callback triggered, stopping listener")
                            break
                        time.sleep(1.0)
                    except KeyboardInterrupt:
                        logger.info("Received interrupt signal")
                        break

        except KeyboardInterrupt:
            logger.info("Shutting down PubSub listener...")
        finally:
            # Always stop listening when exiting, whether due to timeout or interruption
            if self.running:
                self.stop_listening()

    def stop_listening(self, timeout: float = 30.0):
        """
        Stops the active PubSub listener and halts all ongoing streaming operations.

        This method ensures that all active streaming pull futures are cancelled
        and their resources are cleaned up. It also shuts down the executor service
        responsible for handling asynchronous tasks, thereby completely halting
        the PubSub listener process.

        Args:
            timeout: Maximum time to wait for graceful shutdown (default: 30 seconds)

        Raises:
            Any exceptions encountered during the cancellation of streaming pull futures.
        """
        if not self.running:
            logger.warning("PubSub listener is not running")
            return

        logger.info("Stopping PubSub listener...")
        self.running = False

        # Give a moment for any in-flight messages to complete
        import time

        time.sleep(0.5)

        # Cancel all streaming pull futures
        logger.debug(f"Cancelling {len(self.streaming_futures)} streaming futures...")
        for future in self.streaming_futures:
            future.cancel()
            try:
                future.result(timeout=5.0)  # Wait for cancellation to complete
            except Exception as e:
                logger.debug(f"Error during future cancellation: {e}")

        self.streaming_futures.clear()

        # Shutdown executor
        logger.debug("Shutting down executor...")
        self.executor.shutdown(wait=True)

        logger.info("PubSub listener stopped successfully")

    @staticmethod
    def _process_message(message, handlers):
        """
        Processes a received message by delegating it to the appropriate handler based
        on the provided handlers configuration. It ensures that the message is deserialized,
        processed by handlers, and, if successful, acknowledges the message. If an error
        occurs during processing, the system logs the error and ensures the appropriate
        action (acknowledge or not acknowledge) is taken.

        Arguments:
            message (Message): The incoming message to be processed. Must contain
                the raw message data.
            handlers (list): A list of dictionaries, each containing:
                - 'handler' (Callable): The handler function or coroutine to process the event.
                - 'event_type' (Optional[Type]): The expected type for the deserialized event.
                    If not specified, the raw data will be passed to the handler.

        Raises:
            Exception: If an unforeseen error occurs while processing the message or invoking
                one of the handlers.
        """
        try:
            # Parse message data
            data = json.loads(message.data.decode("utf-8"))
            acknowledgement = Acknowledgement(message)

            for handler_info in handlers:
                handler = handler_info["handler"]
                event_type = handler_info.get("event_type")

                try:
                    # Prepare arguments for the handler
                    if event_type:
                        # Deserialize to event type
                        event = deserialize_event(data, event_type)
                    else:
                        # Pass raw data
                        event = data

                    # Check if handler is async
                    if inspect.iscoroutinefunction(handler):
                        asyncio.run(handler(event, acknowledgement))
                    else:
                        handler(event, acknowledgement)

                    # If we get here without exception, handler succeeded
                    if not acknowledgement.acknowledged:
                        acknowledgement.ack()
                    break

                except Exception as e:
                    logger.error(f"Error in handler {handler.__name__}: {e}", exc_info=True)
                    if not acknowledgement.acknowledged:
                        acknowledgement.nack()
                    break

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            # Don't call nack() here since individual handlers handle their own acknowledgments


def create_pubsub_app(
    project_id: str,
    max_workers: int = 10,
    max_messages: int = 100,
    auto_create_resources: bool = True,
    resource_config: Optional[Dict[str, Any]] = None,
) -> PubSubClient:
    """
    Creates and configures a Pub/Sub client application. The function initializes a Pub/Sub client
    with the provided project identifier and optional parameters for configuring
    worker thread pool size, maximum messages to process, and resource creation behavior.

    Args:
        project_id (str): The Google Cloud project identifier for which the Pub/Sub client will be created.
        max_workers (int, optional): The maximum number of worker threads the client can use.
            Default is 10.
        max_messages (int, optional): The maximum number of messages the client can handle simultaneously.
            Default is 100.
        auto_create_resources (bool, optional): Whether to automatically create missing topics and subscriptions.
            Default is True.
        resource_config (dict, optional): Configuration for resource creation (topics, subscriptions).
            Default is None.

    Returns:
        PubSubClient: A configured Pub/Sub client instance.
    """
    return PubSubClient(
        project_id, max_workers, max_messages, auto_create_resources, resource_config
    )
