import os
from typing import List, Dict, Optional, Type
from devpayr.crypto.crypto_helper import CryptoHelper
from devpayr.crypto.hash_helper import HashHelper
from devpayr.exceptions.exceptions import DevPayrException, InjectableVerificationException


class InjectableHandler:
    """
    Handles decrypting, verifying, and writing injectables to disk.
    Allows overriding with a custom injectable processor.
    """

    _custom_processor: Optional[Type] = None

    @classmethod
    def set_processor(cls, processor_class: Type) -> None:
        """
        Set a custom injectable processor class.
        """
        if not hasattr(processor_class, "handle") or not callable(getattr(processor_class, "handle")):
            raise DevPayrException("Custom processor must implement a static `handle()` method.")
        cls._custom_processor = processor_class

    @classmethod
    def process(cls, injectables: List[Dict], options: Dict) -> None:
        """
        Process a batch of injectables using the default or custom processor.

        Options:
            - secret (required)
            - path (optional) – base directory to apply injectables to
            - verify (bool, optional) – whether to verify signatures
        """
        secret = options.get("secret")
        base_path = options.get("path") or os.path.abspath(os.path.expanduser("~"))
        verify = options.get("verify", True)

        if not secret:
            raise DevPayrException("Injectable handler requires a secret key.")

        for injectable in injectables:
            slug = injectable.get("slug")
            encrypted = injectable.get("encrypted_content") or injectable.get("content")
            target_path = injectable.get("target_path")
            signature = injectable.get("signature")

            if not slug or not encrypted or not target_path:
                raise DevPayrException("Injectable must include slug, content, and target_path.")

            if verify and signature and not HashHelper.verify_signature(encrypted, secret, signature):
                raise InjectableVerificationException(f"Signature verification failed for injectable: {slug}")

            processor = cls._custom_processor or cls
            processor.handle(injectable, secret, base_path, verify)

    @staticmethod
    def handle(injectable: Dict, secret: str, base_path: str, verify_signature: bool = True) -> str:
        """
        Default injectable handler (append, prepend, replace).
        """
        slug = injectable.get("slug")
        target_path = injectable.get("target_path")
        encrypted = injectable.get("encrypted_content") or injectable.get("content")
        mode = injectable.get("mode", "replace")

        if not target_path:
            raise DevPayrException(f"No target path specified for injectable: {slug}")

        decrypted = CryptoHelper.decrypt(encrypted, secret)

        full_path = os.path.abspath(os.path.join(base_path, target_path.strip("/\\")))

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(decrypted)
            return full_path

        # File exists, read existing content
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                existing = f.read()
        except Exception as e:
            raise DevPayrException(f"Failed to read {full_path}: {str(e)}")

        content = (
            existing + decrypted if mode == "append"
            else decrypted + existing if mode == "prepend"
            else decrypted
        )

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise DevPayrException(f"Failed to write to {full_path}: {str(e)}")

        return full_path