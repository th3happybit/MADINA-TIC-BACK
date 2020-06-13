from django.conf import settings
from pusher_push_notifications import PushNotifications
import pusher 


"""
Notification push with pusher Beams
"""
def push_notify(citoyen_id, maire_id, title, body):

    push_client = PushNotifications(
            instance_id='65b0754a-0713-4b71-bc41-4d2abae63fc6',
            secret_key='E1067A08CDB1C1F6DD92AF5CAFF4CA9C8F5B50740B6865B3CFACFC282A202A10',
            )
    response = push_client.publish_to_users(
            user_ids = [str(citoyen_id), str(maire_id)],
            publish_body={
                        'apns': {
                            'aps': {
                             'alert': title,
                                   },
                                },
                        'fcm': {
                         'notification': {
                             'title': title,
                             'body': body,
                                         },
                                },
                        },
            )
    print(response['publishId'])

"""
Notification push with pusher channels
"""
def channels_notify(channel, event, data):
    pusher_client = pusher.Pusher(
            app_id= settings.PUSHER_APP_ID,
            key= settings.PUSHER_KEY,
            secret= settings.PUSHER_SECRET,
            cluster= settings.PUSHER_CLUSTER
                )
    
    return pusher_client.trigger(channel, event, {u'message': data})