import pytest
import inject

from acmev2.services import IDirectoryService
from acmev2.settings import ACMESettings


class TestServicesMixin:

    @pytest.fixture(autouse=True)
    def setup_services(self):
        self.directory_service = inject.instance(IDirectoryService)
        self.settings = inject.instance(ACMESettings)
