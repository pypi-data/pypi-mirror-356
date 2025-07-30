# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
    TransformList,
)

def create_versor_transform(
    parameters_type: str = "float32",
) -> TransformList:
    """Create a versor spatial transformation.

    :param parameters_type: Type of the transform parameters (float32 or float64)
    :type  parameters_type: str

    :return: Output transform
    :rtype:  TransformList
    """
    func = environment_dispatch("itkwasm_transform", "create_versor_transform")
    output = func(parameters_type=parameters_type)
    return output
