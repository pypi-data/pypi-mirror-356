from numeta.syntax.statements.various import PointerAssignment
from numeta.builder_helper import BuilderHelper


def get_view(variable, shape):
    if not isinstance(shape, (tuple, list)):
        shape = (shape,)

    builder = BuilderHelper.get_current_builder()
    pointer = builder.generate_local_variables(
        "fc_v", ftype=variable.ftype, dimension=tuple([None for _ in shape]), pointer=True
    )

    PointerAssignment(pointer, shape, variable)

    return pointer
