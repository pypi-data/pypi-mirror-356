# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
    TransformList,
)

async def create_gaussian_smoothing_on_update_displacement_field_transform_async(
    dimension: int = 3,
    parameters_type: str = "float32",
) -> TransformList:
    """Create a gaussian-smoothing-on-update-displacement-field spatial transformation.

    :param dimension: Dimension of the transform (2, 3, or 4)
    :type  dimension: int

    :param parameters_type: Type of the transform parameters (float32 or float64)
    :type  parameters_type: str

    :return: Output transform
    :rtype:  TransformList
    """
    func = environment_dispatch("itkwasm_transform", "create_gaussian_smoothing_on_update_displacement_field_transform_async")
    output = await func(dimension=dimension, parameters_type=parameters_type)
    return output
