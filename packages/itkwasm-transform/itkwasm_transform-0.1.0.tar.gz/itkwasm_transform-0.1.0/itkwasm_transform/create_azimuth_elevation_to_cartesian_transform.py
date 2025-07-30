# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
    TransformList,
)

def create_azimuth_elevation_to_cartesian_transform(
    parameters_type: str = "float32",
) -> TransformList:
    """Create a azimuth-elevation-to-cartesian spatial transformation.

    :param parameters_type: Type of the transform parameters (float32 or float64)
    :type  parameters_type: str

    :return: Output transform
    :rtype:  TransformList
    """
    func = environment_dispatch("itkwasm_transform", "create_azimuth_elevation_to_cartesian_transform")
    output = func(parameters_type=parameters_type)
    return output
