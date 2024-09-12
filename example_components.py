from components import KFPythonFuncComponent
from example_code import add, multiply_with_five, save_arguments_with_yaml

save_arguments_component: KFPythonFuncComponent = KFPythonFuncComponent(save_arguments_with_yaml)
save_arguments_component.set_attr_for_user(base_image="python:3.9-slim")
save_arguments_comp = save_arguments_component.component

example_component_1: KFPythonFuncComponent = KFPythonFuncComponent(add)
example_component_1.set_attr_for_user(packages_to_install=["torch"])
comp1 = example_component_1.component

example_component_2: KFPythonFuncComponent = KFPythonFuncComponent(multiply_with_five)
example_component_2.set_attr_for_user(packages_to_install=["numpy"])
comp2 = example_component_2.component
