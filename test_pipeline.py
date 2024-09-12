from unittest import TestCase
from pipelines import KFPipeline
from example_components import example_component_1, example_component_2, save_arguments_component


class TestPipelines(TestCase):
    def setUp(self) -> None:
        self.pipeline_input_params: dict = {
            example_component_1.component_name: {
                "a": {"type": int, "usage": "input", "dsec": "Input number param 1", "value": 0},
                "b": {"type": int, "usage": "input", "desc": "Input number param 2", "value": 0},
            },
            example_component_2.component_name: {
                "operation_type": {"type": str, "usage": "condition", "desc": "Select operation", "value": None},
            },
        }

        example_component_1.after(save_arguments_component)

        example_component_2.condition = "operation_type == 'multiply'"
        example_component_2.after(example_component_1)

        self.pipeline = KFPipeline(components=[example_component_1, example_component_2], **self.pipeline_input_params)
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    # def test_parse_params_for_pipeline(self):
    #     parsed_params = self.pipeline.parse_params_for_pipeline(self.pipeline_input_params)
    #     self.assertDictEqual(
    #         parsed_params,
    #         {
    #             example_component_1.component_name: {
    #                 key: value["value"]
    #                 for key, value in self.pipeline_input_params[example_component_1.component_name].items()
    #             },
    #             example_component_2.component_name: {
    #                 key: value["value"]
    #                 for key, value in self.pipeline_input_params[example_component_2.component_name].items()
    #             },
    #         },
    #     )

    def test_compile(self):
        func = self.pipeline.make()
        print(func)
