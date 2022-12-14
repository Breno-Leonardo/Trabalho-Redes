import os
import math
import hashlib


def limit_to_two_decimals(n):
    return math.floor(n * 100) / 100


class File:
    def __init__(self, fullPath, name):
        self.path = fullPath
        self.sizeBytes = os.stat(fullPath).st_size
        self.size = self.convert_bytes()
        self.type = os.path.splitext(fullPath)[1]
        self.name = name
        with open(fullPath, 'rb') as file:
            byte = file.read()
            self.sha256_hash = hashlib.sha256(byte).hexdigest()

    def convert_bytes(self):
        if self.sizeBytes < 1024:
            return "%d Bytes" % self.sizeBytes
        elif self.sizeBytes < (1024 * 1024):
            return "%s KB" % limit_to_two_decimals(self.sizeBytes / 1024)
        elif self.sizeBytes < (1024 * 1024 * 1024):
            return "%s MB" % limit_to_two_decimals(self.sizeBytes / (1024 * 1024))
        else:
            return "%s GB" % limit_to_two_decimals(self.sizeBytes / (1024 * 1024 * 1024))

    def obj(self):
        return {
            "name": self.name,
            "sizeBytes": self.sizeBytes,
            "size": self.size,
            "type": self.type,
            "sha256": self.sha256_hash
        }

    def __str__(self):
        return "File Name: {}, File Size: {}, File Type: {}, sha256:{}".format(self.name, self.size, self.type,
                                                                               self.sha256_hash)
