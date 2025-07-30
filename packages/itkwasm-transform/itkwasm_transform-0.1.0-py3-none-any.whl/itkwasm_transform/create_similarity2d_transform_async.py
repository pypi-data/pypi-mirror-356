# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
    TransformList,
)

async def create_similarity2d_transform_async(
    parameters_type: str = "float32",
) -> TransformList:
    """Create a similarity2d spatial transformation.

    :param parameters_type: Type of the transform parameters (float32 or float64)
    :type  parameters_type: str

    :return: Output transform
    :rtype:  TransformList
    """
    func = environment_dispatch("itkwasm_transform", "create_similarity2d_transform_async")
    output = await func(parameters_type=parameters_type)
    return output
