# Generated file. To retain edits, remove this comment.

from pathlib import Path, PurePosixPath
import os
from typing import Dict, Tuple, Optional, List, Any

from importlib_resources import files as file_resources

_pipeline = None

from itkwasm import (
    InterfaceTypes,
    PipelineOutput,
    PipelineInput,
    Pipeline,
    TransformList,
)

def create_rigid3d_perspective_transform(
    dimension: int = 3,
    parameters_type: str = "float32",
) -> TransformList:
    """Create a rigid3d-perspective spatial transformation.

    :param dimension: Dimension of the transform (2, 3, or 4)
    :type  dimension: int

    :param parameters_type: Type of the transform parameters (float32 or float64)
    :type  parameters_type: str

    :return: Output transform
    :rtype:  TransformList
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline(file_resources('itkwasm_transform_wasi').joinpath(Path('wasm_modules') / Path('create-rigid3d-perspective-transform.wasi.wasm')))

    pipeline_outputs: List[PipelineOutput] = [
        PipelineOutput(InterfaceTypes.TransformList),
    ]

    pipeline_inputs: List[PipelineInput] = [
    ]

    args: List[str] = ['--memory-io',]
    # Inputs
    # Outputs
    transform_name = '0'
    args.append(transform_name)

    # Options
    input_count = len(pipeline_inputs)
    if dimension:
        args.append('--dimension')
        args.append(str(dimension))

    if parameters_type:
        args.append('--parameters-type')
        args.append(str(parameters_type))


    outputs = _pipeline.run(args, pipeline_outputs, pipeline_inputs)

    result = outputs[0].data
    return result

