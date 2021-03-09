from typing import Type, Callable


class BaseType:
    pass


class VarType(BaseType):
    pass


class Device(BaseType):
    def __init__(self, device: str=None, name: str=None, property_access = None):
        self.device = device

        if name:
            for char in [' ', ';', ':']:
                if char in name:
                    raise Exception(f'Invalid character "{char}" in device name "{name}"')

        self.name = name
        self.property_access = property_access if property_access else []

    @classmethod
    def access_prop(cls, device, property_access):
        lst = device.property_access.copy()
        lst.append(property_access)
        return cls(device.device,
                   name=device.name,
                   property_access=lst)


class Variable:
    def __init__(self, var: str, var_type: Type[BaseType]):
        self.var = var
        self.var_type: Type[BaseType] = var_type


class Function:
    def __init__(self, var: Callable, var_type: Type[BaseType]):
        self.var = var
        self.var_type: Type[BaseType] = var_type


class FunctionBuiltIn:
    def __init__(self, inst: str, no_args: int, returns: bool=True):
        self.inst = inst
        self.no_args = no_args
        self.returns = returns

