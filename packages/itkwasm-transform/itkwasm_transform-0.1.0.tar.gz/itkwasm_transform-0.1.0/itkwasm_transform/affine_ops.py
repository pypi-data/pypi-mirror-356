# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
    TransformList,
)

def affine_ops(
    input_transform: TransformList,
    operations: Any,
) -> TransformList:
    """Apply operations to an affine transform

    :param input_transform: The input affine transform
    :type  input_transform: TransformList

    :param operations: JSON array of operations to apply
    :type  operations: Any

    :return: The output affine transform
    :rtype:  TransformList
    """
    func = environment_dispatch("itkwasm_transform", "affine_ops")
    output = func(input_transform, operations)
    return output
