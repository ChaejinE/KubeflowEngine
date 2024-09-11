from pyfunc_component import KFPythonFuncComponent
from example_code import add

example_component: KFPythonFuncComponent = KFPythonFuncComponent(add)
example_component.set_attr_for_user(packages_to_install=["torch"])
example_component = example_component.component
