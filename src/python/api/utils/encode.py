import hashlib
import string
import random


class HashCodeGenerator:
    def __init__(self, mongo_client, code_length=8):
        self.characters = string.ascii_letters
        self.code_length = code_length
        self.mongo_client = mongo_client

    def generate_code(self, url):
        hash_digest = hashlib.sha256(url.encode()).hexdigest()
        shortened_hash = self.base62_encode(hash_digest)[: self.code_length]
        code = "".join(random.choice(self.characters) for _ in range(self.code_length))
        for i in range(self.code_length):
            code = code[:i] + shortened_hash[i] + code[i + 1 :]
        if self.code_exists(code):  # Generate a new code if exists to avoid collision
            code = self.generate_code(url)
        return code

    def base62_encode(self, hex_value):
        base62_characters = string.ascii_letters + string.digits
        value = int(hex_value, 16)
        base62 = ""
        while value > 0:
            value, index = divmod(value, 62)
            base62 = base62_characters[index] + base62
        return base62

    def code_exists(self, code):
        existing = self.mongo_client.url_shortener.mappings.find_one(
            {"shortened": code}
        )
        return existing is not None
