from example_components import example_component_1, example_component_2
from pipelines import KFPipeline

pipeline_input_params: dict = {
    example_component_1.component_name: {
        {"x": {"type": int, "usage": "input", "dsec": "Input number param 1", "value": 0, "arg_name": "a"}},
        {"y": {"type": int, "usage": "input", "desc": "Input number param 2", "value": 0, "arg_name": "b"}},
    },
    example_component_2.component_name: {
        {"operation_type": {"type": str, "usage": "condition", "desc": "Select operation", "value": None}},
    },
}

# Setting component 1
# Setting component 2
example_component_2.condition = "operation_type == 'multiply'"
example_component_2.after(example_component_1)

pipeline = KFPipeline(components=[example_component_1, example_component_2], **pipeline_input_params)
