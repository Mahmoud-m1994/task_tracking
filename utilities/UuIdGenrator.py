import uuid


def generate_text_uuid(text):
    unique_id = str(uuid.uuid4())
    text_uuid = text + "_" + unique_id
    return text_uuid
