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

async def affine_ops_async(
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
    js_module = await js_package.js_module
    web_worker = js_resources.web_worker

    kwargs = {}

    outputs = await js_module.affineOps(to_js(input_transform), to_js(operations), webWorker=web_worker, noCopy=True, **kwargs)

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
