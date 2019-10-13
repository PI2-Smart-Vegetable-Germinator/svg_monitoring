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
        notification = {
            'title': 'Colheita próxima!',
            'body': 'Faltam %s dias para retirar as mudas de sua SVG!' % str(device_id[1])
        }
        sender.send_message(device_id[0], notification)
