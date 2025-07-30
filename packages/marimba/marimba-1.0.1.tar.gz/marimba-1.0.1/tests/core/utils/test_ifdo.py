import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

from ifdo import iFDO
from ifdo.models import ImageSetHeader

from marimba.core.utils.ifdo import load_ifdo, save_ifdo


class TestIfdo(TestCase):
    """
    Class to test the functionality of the iFDO class.

    Methods:
    - setUp(): Sets up the initial state before each test case.
    - tearDown(): Cleans up the state after each test case.
    - test_load_ifdo(): Tests the load_ifdo() function.
    - test_save_ifdo(): Tests the save_ifdo() function.
    """

    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        self.ifdo_path = Path(self.test_dir.name) / "test_ifdo.yaml"
        self.uuid = str(uuid4())
        self.ifdo = iFDO(
            image_set_header=ImageSetHeader(
                image_set_name="test_image_set_name",
                image_set_uuid=self.uuid,
                image_set_handle="test_image_set_handle",
            ),
            image_set_items={},
        )

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    @patch("uuid.uuid4", return_value=UUID("12345678123456781234567812345678"))
    def test_load_ifdo(self, mock_uuid: MagicMock) -> None:
        self.ifdo.save(self.ifdo_path)
        loaded_ifdo = load_ifdo(self.ifdo_path)
        self.assertEqual(self.ifdo, loaded_ifdo)

    def test_save_ifdo(self) -> None:
        save_ifdo(self.ifdo, self.ifdo_path)
        self.assertTrue(self.ifdo_path.exists())
        loaded_ifdo = load_ifdo(self.ifdo_path)
        self.assertEqual(self.ifdo, loaded_ifdo)
