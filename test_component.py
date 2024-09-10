from unittest import TestCase
from pythonfunc_component import KFPythonFuncComponent
from kfp.components import PythonComponent
from example import add
from log_config import level

import logging, os

logging.basicConfig(level=level)


class TestKFPythonFuncComponent(TestCase):
    def setUp(self) -> None:
        self.component = KFPythonFuncComponent(add)
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_make_kf_component(self):
        kf_component = self.component.component
        self.assertIsInstance(kf_component, PythonComponent)

    def test_run_target_func(self):
        result = self.component.run_target_func(1, 2)
        self.assertEqual(result, 3)

    def test_build(self):
        self.component.build()
