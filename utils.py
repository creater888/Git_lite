import hashlib
import json


def generate_hash(data):

    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)

    return hashlib.sha256(data.encode()).hexdigest()[:10]