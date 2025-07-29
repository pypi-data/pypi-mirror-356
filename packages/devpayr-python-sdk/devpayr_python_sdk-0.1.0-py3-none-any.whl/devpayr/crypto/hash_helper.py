import hashlib
import hmac


class HashHelper:
    """
    Utility class to generate and verify SHA-256 hashes and HMAC-SHA256 signatures.
    """

    @staticmethod
    def hash(content: str) -> str:
        """
        Generate a SHA-256 hash of a string.
        """
        return hashlib.sha256(content.encode()).hexdigest()

    @staticmethod
    def signature(content: str, secret: str) -> str:
        """
        Generate an HMAC-SHA256 signature.
        """
        return hmac.new(secret.encode(), content.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def verify_hash(content: str, expected_hash: str) -> bool:
        """
        Check if the SHA-256 hash of the content matches the expected hash.
        """
        return hmac.compare_digest(HashHelper.hash(content), expected_hash)

    @staticmethod
    def verify_signature(content: str, secret: str, expected_signature: str) -> bool:
        """
        Check if the HMAC-SHA256 signature of the content matches the expected signature.
        """
        return hmac.compare_digest(HashHelper.signature(content, secret), expected_signature)