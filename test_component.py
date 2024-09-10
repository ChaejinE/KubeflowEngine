from unittest import TestCase
from component import KFComponent
from kfp.components import PythonComponent
from example import add
from log import logger


class TestComponent(TestCase):
    def setUp(self) -> None:
        self.component = KFComponent(add)
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_make_kf_component(self):
        component = self.component.component
        self.assertIsInstance(component, PythonComponent)

    def test_run_func(self):
        result = self.component.run_func(1, 2)
        logger.info("Result : ", result)
