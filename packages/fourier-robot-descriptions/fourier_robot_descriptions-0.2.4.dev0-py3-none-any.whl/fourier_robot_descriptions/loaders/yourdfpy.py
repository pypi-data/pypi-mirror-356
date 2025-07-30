#!/usr/bin/env python3
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023 Inria

"""Load a robot description in yourdfpy."""

from typing import Optional

from fourier_robot_descriptions.fourier import PACKAGE_PATH, REPOSITORY_PATH

try:
    import yourdfpy
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "This feature requires 'yourdfpy', which can be installed by `pip install yourdfpy`"
    ) from e


def load_robot_description(
    description_name: str,
    commit: str | None = None,
) -> yourdfpy.URDF:
    """Load a robot description in yourdfpy.

    Args:
        description_name: Name of the robot description.
        commit: If specified, check out that commit from the cloned robot
            description repository.

    Returns:
        Robot model for yourdfpy.
    """
    URDF_PATH = str(PACKAGE_PATH / f"{description_name}.urdf")
    return yourdfpy.URDF.load(URDF_PATH, mesh_dir=PACKAGE_PATH)
