import json
import asyncio
from uuid import UUID
from app.core.redis import redis_client
from app.websocket.connection_manager import manager
from app.constant.user_status import USER_STATUS

async def redis_listener():
    pubsub = redis_client.pubsub()

    pubsub.psubscribe("notification:*")
    pubsub.subscribe("presence")


    print("[Redis Listener] Subscribed to notification channel")

    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            user_id = None

            if message is not None:
                print("\n\n message \n\n", message, "\n\n\n")
                
                channel = message["channel"]

                payload = json.loads(message["data"])


                print('\n\n\n payload \n\n\n', payload, '\n\n\n')
                print('\n\n\n channel \n\n\n', channel, '\n\n\n')

                if channel.startswith("notification"):
                    await manager.send_to_user(message=payload, to_user_id = payload["user_id"])

                elif channel.startswith("presence"):
                    event_type = payload["type"]
                    if event_type in USER_STATUS.values():
                        user_id = payload["data"]["user_id"]

                        await manager.broadcast(message=payload, user_id=UUID(user_id))
                
                print(f"[Redis_event] user={user_id}")


            await asyncio.sleep(0.1)

    except Exception as e:
        print("[Redis Listener] Error:", e)    

    finally:
        pubsub.close()