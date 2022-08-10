def bmp180_temperature(topic, payload):
    import json
    json_tree = json.loads(payload)
    temperature = json_tree["StatusSNS"]["BMP180"]["Temperature"]
    return temperature


def direct(topic, payload):
    return payload
