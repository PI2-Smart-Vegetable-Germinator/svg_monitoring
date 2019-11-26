from project.api.utils.notifications import NotificationSender

def filter_device_ids(users, close_to_harvest_plantings):
    device_ids = []

    for user in users:
        for planting in close_to_harvest_plantings:
            if user['machineId'] == planting[0].machine_id:
                device_ids.append((user['deviceId'], planting[1]))

    return device_ids

def notify_close_harvest(sender, device_ids):
    for device_id in device_ids:
        notification_body = 'Faltam %s dias para retirar as mudas de sua SVG!' % str(device_id[1])
        if device_id[1] <= 0:
            notification_body = 'Você já pode retirar as mudas de sua SVG!'
        notification = {
            'title': 'Colheita próxima!',
            'body': notification_body,
            'dataContent': {
                'code': 'SVG_CLOSE_HARVEST'
            }
        }
        sender.send_message(device_id[0], notification)
