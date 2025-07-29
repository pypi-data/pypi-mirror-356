import sys
import webbrowser
from devpayr.config.config import Config
from devpayr.exceptions.exceptions import DevPayrException
from devpayr.runtime.validator import RuntimeValidator
from devpayr.services.project_service import ProjectService
from devpayr.services.license_service import LicenseService
from devpayr.services.domain_service import DomainService
from devpayr.services.injectable_service import InjectableService
from devpayr.services.payment_service import PaymentService
import os

class DevPayr:
    """
    🔹 Primary SDK entrypoint. Handles runtime validation, injectables,
    and access to DevPayr service APIs.
    """
    _config: Config = None

    @staticmethod
    def bootstrap(config_dict: dict) -> None:
        """
        Bootstraps the SDK with runtime validation and optional callback.
        """
        DevPayr._config = Config(config_dict)

        try:
            data = {}
            if DevPayr._config.is_license_mode():
                validator = RuntimeValidator(DevPayr._config)
                data = validator.validate()

            callback = DevPayr._config.get("onReady")
            if callable(callback):
                callback(data)

        except DevPayrException as e:
            DevPayr._handle_failure(str(e), config_dict)
        except Exception as e:
            DevPayr._handle_failure(f"Unexpected error: {str(e)}", config_dict)

    @staticmethod
    def _handle_failure(message: str, config: dict) -> None:
        """
        Handles SDK failure behavior: modal, redirect, log, or silent.
        """
        mode = config.get("invalidBehavior", "modal")
        final_message = config.get("customInvalidMessage", message)

        if mode == "redirect":
            target = config.get("redirectUrl", "https://devpayr.com/upgrade")
            webbrowser.open(target)
            sys.exit()

        elif mode == "log":
            print(f"[DevPayr] Invalid license: {final_message}", file=sys.stderr)

        elif mode == "silent":
            pass  # Do nothing

        elif mode == "modal":
            html_path = config.get("customInvalidView") or os.path.join(os.path.dirname(__file__), "resources/unlicensed.html")
            try:
                with open(html_path, "r", encoding="utf-8") as f:
                    html = f.read()
                    html = html.replace("{{message}}", final_message)
                    print(html)
            except Exception:
                print(f"<h1>⚠️ Unlicensed Software</h1><p>{final_message}</p>")
            sys.exit()

    @staticmethod
    def config() -> Config:
        return DevPayr._config

    # 🔹 Core Services

    @staticmethod
    def projects() -> ProjectService:
        return ProjectService(DevPayr._config)

    @staticmethod
    def licenses() -> LicenseService:
        return LicenseService(DevPayr._config)

    @staticmethod
    def domains() -> DomainService:
        return DomainService(DevPayr._config)

    @staticmethod
    def injectables() -> InjectableService:
        return InjectableService(DevPayr._config)

    @staticmethod
    def payments() -> PaymentService:
        return PaymentService(DevPayr._config)