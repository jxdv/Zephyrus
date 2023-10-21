import hashlib


class Target:
    def __init__(self, target_path, hash_alg):
        self.target_path = target_path
        self.hash_alg = hash_alg

    def checksum(self, buff_size=128*1024):
        h = hashlib.new(self.hash_alg)
        buffer = bytearray(buff_size)
        buffer_view = memoryview(buffer)

        with open(self.target_path, "rb", buffering=0) as f:
            while True:
                chunk = f.readinto(buffer_view)
                if not chunk:
                    break
                h.update(buffer_view[:chunk])
        return h.hexdigest()

    def __str__(self):
        return f"{self.target_path}"

    def __repr__(self):
        return f"Target(\'{self.target_path}\')"
