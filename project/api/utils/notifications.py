from firebase_admin import messaging

class NotificationSender:
    def send_message(self, device_id, data):
        notification = messaging.Notification(title=data['title'], body=data['body'])
        message = messaging.Message(notification=notification, token=device_id)
        response = messaging.send(message)

        return response