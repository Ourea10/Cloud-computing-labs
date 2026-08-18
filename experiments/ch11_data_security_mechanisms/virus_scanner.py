import hashlib

from experiments.ch11_data_security_mechanisms.models import (
    FileObject,
    ScanReport,
    ScanResult,
)

from cryptography.fernet import Fernet


class DecryptionService:

    def __init__(self):

        self.key = Fernet.generate_key()

        self.cipher = Fernet(self.key)

    def encrypt(
        self,
        content: bytes,
    ) -> bytes:

        return self.cipher.encrypt(
            content
        )

    def decrypt(
        self,
        content: bytes,
    ) -> bytes:

        return self.cipher.decrypt(
            content
        )
        
class DigitalVirusScanner:

    KNOWN_SIGNATURES = {
        hashlib.sha256(
            b"EICAR_TEST_SIGNATURE"
        ).hexdigest()
    }

    def scan(
        self,
        file: FileObject,
    ) -> ScanReport:

        digest = hashlib.sha256(
            file.content
        ).hexdigest()

        if digest in self.KNOWN_SIGNATURES:

            return ScanReport(
                file_id=file.file_id,
                result=ScanResult.MALICIOUS,
                findings=[
                    "Known malware signature detected"
                ],
            )

        return ScanReport(
            file_id=file.file_id,
            result=ScanResult.CLEAN,
        )