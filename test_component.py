from unittest import TestCase
from kfp.components import PythonComponent
from pyfunc_component import KFPythonFuncComponent
from example_code import add
from log_config import level

import logging, os

logging.basicConfig(level=level)


class TestKFPythonFuncComponent(TestCase):
    def setUp(self) -> None:
        self.component = KFPythonFuncComponent(add)
        self.component_path = f"{os.getcwd()}/example_components.py"
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    # def test_make_kf_component(self):
    #     kf_component = self.component.component
    #     self.assertIsInstance(kf_component, PythonComponent)

    # def test_run_target_func(self):
    #     result = self.component.run_target_func(1, 2)
    #     self.assertEqual(result, 3)

    # def test_build_image(self):
    #     self.component.build_image(target_component_path=self.component_path)

    def test_push_image(self):
        self.component.push_image(target_component_path=self.component_path)
