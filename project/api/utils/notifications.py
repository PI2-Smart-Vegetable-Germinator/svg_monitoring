from firebase_admin import messaging

class NotificationSender:
    def send_message(self, device_id, data):
        notification = messaging.Notification(title=data['title'], body=data['body'])
        message = messaging.Message(notification=notification, token=device_id, data=data.get('dataContent'))
        response = messaging.send(message)

        return response

    def send_data_message(self, device_id, data):
        message = messaging.Message(token=device_id, data=data)
        response = messaging.send(message)

        return response