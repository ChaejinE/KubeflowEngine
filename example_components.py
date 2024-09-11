from components import KFPythonFuncComponent
from example_code import add, multiply_with_five

example_component_1: KFPythonFuncComponent = KFPythonFuncComponent(add)
example_component_1.set_attr_for_user(packages_to_install=["torch"])
comp1 = example_component_1.component

example_component_2: KFPythonFuncComponent = KFPythonFuncComponent(multiply_with_five)
example_component_2.set_attr_for_user(packages_to_install=["numpy"])
comp2 = example_component_2.component
