def normalize(data):
    normalized = {}
    for k, v in data.items():
        if isinstance(v, str):
            normalized[k] = v.strip().lower()
        else:
            normalized[k] = v
    return normalized