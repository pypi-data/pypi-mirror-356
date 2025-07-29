import os
import sys
from devpayr.devpayr import DevPayr
from devpayr.config.config import Config
from devpayr.services.project_service import ProjectService
from devpayr.services.license_service import LicenseService
from devpayr.services.domain_service import DomainService
from devpayr.services.injectable_service import InjectableService
from devpayr.services.payment_service import PaymentService


def test_devpayr_bootstrap_and_services():
    print("\n🧪 Running DevPayr.bootstrap() and core service accessors...")

    triggered = {"called": False, "data": None}

    def on_ready_callback(data):
        triggered["called"] = True
        triggered["data"] = data

    config_dict = {
        "base_url": "http://127.0.0.1:8000/api/v1",
        "injectables": False,
        "onReady": on_ready_callback,
        "debug": True,
        "secret":"123456789",
        "license":"01975a4e-bc1c-72fc-a1b5-b509d8f07c75",
        "timeout":5000,
        "invalidBehavior":"log",
        "customInvalidMessage": "This copy is not licensed for production uses.",
    }

    DevPayr.bootstrap(config_dict)

    # Check if config is stored
    assert isinstance(DevPayr.config(), Config)

    # Check if callback was triggered
    assert triggered["called"] is True
    assert isinstance(triggered["data"], dict)

    # Check service accessors
    assert isinstance(DevPayr.projects(), ProjectService)
    assert isinstance(DevPayr.licenses(), LicenseService)
    assert isinstance(DevPayr.domains(), DomainService)
    assert isinstance(DevPayr.injectables(), InjectableService)
    assert isinstance(DevPayr.payments(), PaymentService)

    print("✅ DevPayr bootstrap and service accessors working.")


if __name__ == "__main__":
    test_devpayr_bootstrap_and_services()