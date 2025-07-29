import pulsar
import json
from nimbit.mesh.message import Message
from nimbit.mesh.pulsar_client import PulsarClient

async def default_agent_runtime(message_handler):
    consumer = PulsarClient.client.subscribe('nim-in', subscription_name='nim-in', consumer_type=pulsar.ConsumerType.Shared)

    producers = {}

    while True:
        try:
            msg = consumer.receive()

            props = msg.properties()
            metadata = json.loads(props.get("metadata", "{}"))
            message = Message(
                requestId=props.get("requestId"),
                source=props.get("source"),
                destination=props.get("destination", None),
                metadata=metadata,
                content=msg.data().decode("utf-8"),
            )

            response: Message = await message_handler(message)


            consumer.acknowledge(msg)
        except Exception as e:
            print("ERROR", e)
            consumer.negative_acknowledge(msg)

