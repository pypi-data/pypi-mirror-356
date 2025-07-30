import json
from typing import List, Dict, Any, Optional
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import botocore
import boto3
from botocore.exceptions import ClientError

try:
    from . import log
except ImportError:
    import log


class SQSHandler:
    def __init__(self, queue_url: str, region_name: str = 'us-east-2', user_profile: str = None):
        """
        Initialize the SQSHandler.

        Args:
            queue_url (str): The URL of the SQS queue.
            region_name (str, optional): The AWS region name. Defaults to 'us-east-1'.
        """
        self.queue_url = queue_url
        if user_profile:
            boto3.setup_default_session(profile_name=user_profile,
                                        region_name=region_name)
        self.client_config = botocore.config.Config(
            max_pool_connections=50)
        self.sqs = boto3.client('sqs', region_name=region_name, config=self.client_config)
        self.logger = log.setup_logger(__name__, log_to_console=True)

    def send_message(self, message_body: str or dict, message_attributes: Optional[Dict[str, Dict[str, str]]] = None) -> \
            Dict[
                str, Any]:
        """
        Send a message to the SQS queue.

        Args:
            message_body (str or dict): The body of the message to send.
            message_attributes (Dict[str, Dict[str, str]], optional): Message attributes.

        Returns:
            Dict[str, Any]: The response from SQS.

        Example:
            handler = SQSHandler('https://sqs.us-east-1.amazonaws.com/123456789012/my-queue')
            response = handler.send_message('Hello, SQS!', {'Attribute': {'StringValue': 'Value', 'DataType': 'String'}})
        """
        if isinstance(message_body, dict):
            message_body = json.dumps(message_body)

        try:
            params = {
                'QueueUrl': self.queue_url,
                'MessageBody': message_body
            }
            if message_attributes:
                params['MessageAttributes'] = message_attributes

            response = self.sqs.send_message(**params)
            return response
        except ClientError as e:
            self.logger.error(f"Failed to send message: {e}")
            raise

    def receive_messages(self, max_number: int = 10, wait_time: int = 20) -> List[Dict[str, Any]]:
        """
        Receive messages from the SQS queue.

        Args:
            max_number (int, optional): Maximum number of messages to receive. Defaults to 10.
            wait_time (int, optional): Long polling wait time in seconds. Defaults to 20.

        Returns:
            List[Dict[str, Any]]: List of received messages.

        Example:
            handler = SQSHandler('https://sqs.us-east-1.amazonaws.com/123456789012/my-queue')
            messages = handler.receive_messages(max_number=5, wait_time=10)
        """
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time,
                AttributeNames=['All'],
                MessageAttributeNames=['All']
            )
            messages = response.get('Messages', [])
            self.logger.info(f"Received {len(messages)} messages")
            return messages
        except ClientError as e:
            self.logger.error(f"Failed to receive messages: {e}")
            raise

    def delete_message(self, receipt_handle: str) -> Dict[str, Any]:
        """
        Delete a message from the SQS queue.

        Args:
            receipt_handle (str): The receipt handle of the message to delete.

        Returns:
            Dict[str, Any]: The response from SQS.

        Example:
            handler = SQSHandler('https://sqs.us-east-1.amazonaws.com/123456789012/my-queue')
            response = handler.delete_message('AQEBRXTo.../')
        """
        try:
            response = self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            self.logger.info(f"Message deleted. ReceiptHandle: {receipt_handle}")
            return response
        except ClientError as e:
            self.logger.error(f"Failed to delete message: {e}")
            raise

    def purge_queue(self) -> Dict[str, Any]:
        """
        Purge all messages from the SQS queue.

        Returns:
            Dict[str, Any]: The response from SQS.

        Example:
            handler = SQSHandler('https://sqs.us-east-1.amazonaws.com/123456789012/my-queue')
            response = handler.purge_queue()
        """
        try:
            response = self.sqs.purge_queue(QueueUrl=self.queue_url)
            self.logger.info("Queue purged successfully")
            return response
        except ClientError as e:
            self.logger.error(f"Failed to purge queue: {e}")
            raise

    def get_queue_attributes(self, attribute_names: List[str] = ['All']) -> Dict[str, Any]:
        """
        Get attributes of the SQS queue.

        Args:
            attribute_names (List[str], optional): List of attribute names to retrieve. Defaults to ['All'].

        Returns:
            Dict[str, Any]: The queue attributes.

        Example:
            handler = SQSHandler('https://sqs.us-east-1.amazonaws.com/123456789012/my-queue')
            attributes = handler.get_queue_attributes(['QueueArn', 'ApproximateNumberOfMessages'])
        """
        try:
            response = self.sqs.get_queue_attributes(
                QueueUrl=self.queue_url,
                AttributeNames=attribute_names
            )
            self.logger.info(f"Retrieved queue attributes: {response['Attributes']}")
            return response['Attributes']
        except ClientError as e:
            self.logger.error(f"Failed to get queue attributes: {e}")
            raise

    def count_messages(self) -> Dict[str, int]:
        """
        Get the approximate count of messages in the SQS queue.

        Returns:
            Dict[str, int]: A dictionary containing counts for different message states.
                - 'total': Total number of messages (visible + not visible + in flight)
                - 'visible': Number of messages available for retrieval
                - 'not_visible': Number of messages that are in flight or delayed
                - 'in_flight': Number of messages that have been retrieved but not deleted

        Example:
            handler = SQSHandler('https://sqs.us-east-1.amazonaws.com/123456789012/my-queue')
            message_counts = handler.count_messages()
            print(f"Total messages: {message_counts['total']}")
        """
        try:
            attributes = self.get_queue_attributes([
                'ApproximateNumberOfMessages',
                'ApproximateNumberOfMessagesNotVisible',
                'ApproximateNumberOfMessagesDelayed'
            ])

            visible = int(attributes.get('ApproximateNumberOfMessages', 0))
            not_visible = int(attributes.get('ApproximateNumberOfMessagesNotVisible', 0))
            delayed = int(attributes.get('ApproximateNumberOfMessagesDelayed', 0))

            total = visible + not_visible + delayed

            counts = {
                'total': total,
                'visible': visible,
                'not_visible': not_visible + delayed,
                'in_flight': not_visible
            }

            self.logger.info(f"Message counts: {counts}")
            return counts
        except ClientError as e:
            self.logger.error(f"Failed to count messages: {e}")
            raise

    def delete_all_messages(self, num_threads=10):
        """
        Deletes all messages from the SQS queue with a progress indicator and parallel processing.

        Args:
            num_threads (int): Number of threads to use for parallel processing. Defaults to 10.

        Example:
            handler = SQSHandler('https://sqs.us-east-1.amazonaws.com/123456789012/my-queue')
            handler.delete_all_messages()
        """
        try:
            total_deleted = 0
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                while True:
                    messages = self.sqs.receive_message(
                        QueueUrl=self.queue_url,
                        MaxNumberOfMessages=10,
                        WaitTimeSeconds=1
                    ).get('Messages', [])

                    if not messages:
                        break

                    futures.append(executor.submit(self._delete_messages_batch, messages))

                for future in as_completed(futures):
                    result = future.result()
                    total_deleted += result
                    self._print_progress(total_deleted)

            self.logger.info(f"Successfully deleted {total_deleted} messages from the queue.")

        except ClientError as e:
            self.logger.error(f"Failed to delete messages: {e}")
            raise

    def _delete_messages_batch(self, messages):
        """
        Deletes a batch of messages from the SQS queue.

        Args:
            messages (list): List of messages to delete.

        Returns:
            int: Number of messages deleted.
        """
        entries = [{'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']} for msg in messages]
        response = self.sqs.delete_message_batch(
            QueueUrl=self.queue_url,
            Entries=entries
        )

        if 'Failed' in response:
            self.logger.error(f"Failed to delete some messages: {response['Failed']}")
            raise Exception(f"Failed to delete some messages: {response['Failed']}")

        return len(entries)

    def _print_progress(self, total_deleted):
        """
        Prints a progress indicator for the number of deleted messages.

        Args:
            total_deleted (int): The total number of messages deleted so far.
        """
        sys.stdout.write(f"\rTotal messages deleted: {total_deleted}")
        sys.stdout.flush()
        time.sleep(0.1)
