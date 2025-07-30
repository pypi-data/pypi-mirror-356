import os
import hashlib
from datetime import datetime
from devpayr.config.config import Config
from devpayr.exceptions.exceptions import DevPayrException
from devpayr.services.payment_service import PaymentService
from devpayr.support.injectable_handler import InjectableHandler


class RuntimeValidator:
    """
    Validates a license key and handles optional injectable processing.
    """

    def __init__(self, config: Config):
        self.config = config
        self.license = config.get("license")

        if not self.license:
            raise DevPayrException("License key is required for runtime validation.")

        self.cache_key = f"devpayr_{self._hash_license()}"

    def validate(self) -> dict:
        """
        Performs remote validation or uses cache, and optionally processes injectables.
        """
        if not self.config.get("recheck") and self._is_cached():
            return {"cached": True, "message": "License validated from cache"}

        response = PaymentService(self.config).check_with_license_key()

        if not response.get("data", {}).get("has_paid"):
            raise DevPayrException("Project is unpaid or unauthorized.")

        self._cache_success()

        # Set custom processor if available
        processor = self.config.get("injectablesProcessor")
        if processor:
            InjectableHandler.set_processor(processor)

        # Auto-process injectables if enabled
        if (
            self.config.get("injectables") and
            self.config.get("handleInjectables", True) and
            response.get("data", {}).get("injectables")
        ):
            self._handle_injectables(response["data"]["injectables"])

        return response

    def _handle_injectables(self, injectables: list):
        InjectableHandler.process(injectables, {
            "secret": self.config.get("secret"),
            "path": self.config.get("injectablesPath") or self._cache_dir(),
            "verify": self.config.get("injectablesVerify", True)
        })

    def _cache_success(self):
        """
        Cache today's date to avoid revalidation if `recheck` is off.
        """
        path = os.path.join(self._cache_dir(), self.cache_key)
        with open(path, "w", encoding="utf-8") as f:
            f.write(datetime.today().strftime("%Y-%m-%d"))

    def _is_cached(self) -> bool:
        """
        Check if license has already been validated today.
        """
        path = os.path.join(self._cache_dir(), self.cache_key)
        if not os.path.exists(path):
            return False
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip() == datetime.today().strftime("%Y-%m-%d")

    def _cache_dir(self) -> str:
        """
        Resolve the system's temp directory.
        """
        return os.getenv("TMPDIR") or os.getenv("TEMP") or os.getenv("TMP") or "/tmp"

    def _hash_license(self) -> str:
        """
        Generate SHA256 hash of license key.
        """
        return hashlib.sha256(self.license.encode()).hexdigest()