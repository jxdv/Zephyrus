import unittest
import os

from core.target import Target


class TestChecksum(unittest.TestCase):
    def __init__(self, method_name="runTest"):
        super().__init__(method_name)
        current_dir = os.path.dirname(__file__)
        data_path = os.path.join(current_dir, "data")
        self.test_files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

    def test_md5(self):
        expected_md5 = {
            "file1.txt": "b37ab71452f6ada34d54db68c8f96222",
            "file2.txt": "c158b09cce4e14d0224cbff268da2515",
            "file3.txt": "3ae9feaa1f2d6da5be697a900e680022",
            "file4.txt": "9961eb6ba547c14d0c267eb35855886e",
            "file5.txt": "f3257074b85d823f2e84d94be86582f5"
        }

        for file_name in self.test_files:
            md5 = expected_md5.get(file_name)
            file_path = os.path.abspath(os.path.join("tests/data", file_name))
            target = Target(file_path)
            self.assertEqual(target.checksum(hash_alg="md5"), md5)

    def test_sha256(self):
        expected_sha256 = {
            "file1.txt": "e927d973ee89fb4bc0fb7f94307a8cf66823827df33e824ecc64aa721dc7ab33",
            "file2.txt": "99923cafa82971a8ab7c1f810ba7a7208bb63506d88a75b65492582b1a84d46e",
            "file3.txt": "3fd2140217ee59594c50e020b74ab70dfcbd34aa03c8a2aea8708e3eda5ac9b7",
            "file4.txt": "75d116f4850911746fa00d5321aed724fb65c55338c25217f1dc82e1b6c93294",
            "file5.txt": "f6e70463d81bb1f0b82184df9169819d0c822b8210ac623d5bd1925a7bbc07d7"
        }

        for file_name in self.test_files:
            sha256 = expected_sha256.get(file_name)
            file_path = os.path.abspath(os.path.join("tests/data", file_name))
            target = Target(file_path)
            self.assertEqual(target.checksum(hash_alg="sha256"), sha256)


if __name__ == "__main__":
    unittest.main()
