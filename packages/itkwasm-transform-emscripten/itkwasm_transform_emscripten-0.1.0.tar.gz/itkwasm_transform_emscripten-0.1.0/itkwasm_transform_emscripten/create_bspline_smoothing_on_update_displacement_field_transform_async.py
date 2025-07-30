# Generated file. To retain edits, remove this comment.

from pathlib import Path
import os
from typing import Dict, Tuple, Optional, List, Any

from .js_package import js_package

from itkwasm.pyodide import (
    to_js,
    to_py,
    js_resources
)
from itkwasm import (
    InterfaceTypes,
    TransformList,
)

async def create_bspline_smoothing_on_update_displacement_field_transform_async(
    dimension: int = 3,
    parameters_type: str = "float32",
) -> TransformList:
    """Create a bspline-smoothing-on-update-displacement-field spatial transformation.

    :param dimension: Dimension of the transform (2, 3, or 4)
    :type  dimension: int

    :param parameters_type: Type of the transform parameters (float32 or float64)
    :type  parameters_type: str

    :return: Output transform
    :rtype:  TransformList
    """
    js_module = await js_package.js_module
    web_worker = js_resources.web_worker

    kwargs = {}
    if dimension:
        kwargs["dimension"] = to_js(dimension)
    if parameters_type:
        kwargs["parametersType"] = to_js(parameters_type)

    outputs = await js_module.createBsplineSmoothingOnUpdateDisplacementFieldTransform(webWorker=web_worker, noCopy=True, **kwargs)

    output_web_worker = None
    output_list = []
    outputs_object_map = outputs.as_object_map()
    for output_name in outputs.object_keys():
        if output_name == 'webWorker':
            output_web_worker = outputs_object_map[output_name]
        else:
            output_list.append(to_py(outputs_object_map[output_name]))

    js_resources.web_worker = output_web_worker

    if len(output_list) == 1:
        return output_list[0]
    return tuple(output_list)
