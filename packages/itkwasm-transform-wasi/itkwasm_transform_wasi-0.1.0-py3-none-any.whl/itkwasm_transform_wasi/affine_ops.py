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
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline(file_resources('itkwasm_transform_wasi').joinpath(Path('wasm_modules') / Path('affine-ops.wasi.wasm')))

    pipeline_outputs: List[PipelineOutput] = [
        PipelineOutput(InterfaceTypes.TransformList),
    ]

    pipeline_inputs: List[PipelineInput] = [
        PipelineInput(InterfaceTypes.TransformList, input_transform),
        PipelineInput(InterfaceTypes.JsonCompatible, operations),
    ]

    args: List[str] = ['--memory-io',]
    # Inputs
    args.append('0')
    args.append('1')
    # Outputs
    output_transform_name = '0'
    args.append(output_transform_name)

    # Options
    input_count = len(pipeline_inputs)

    outputs = _pipeline.run(args, pipeline_outputs, pipeline_inputs)

    result = outputs[0].data
    return result

