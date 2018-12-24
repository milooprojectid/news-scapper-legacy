# import pusher, os

# def publish(channel, event, data):
#   pusher_client = pusher.Pusher(
#     app_id=os.getenv('PUSHER_APP_ID'),
#     key=os.getenv('PUSHER_APP_KEY'),
#     secret=os.getenv('PUSHER_APP_SECRET'),
#     cluster=os.getenv('PUSHER_APP_CLUSTER'),
#     ssl=True
#   )
#   pusher_client.trigger(channel, event, data)
