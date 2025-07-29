#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""Visualization helpers."""

import pinocchio as pin
from pinocchio import visualize


def start_meshcat_visualizer(
    robot: pin.RobotWrapper,
) -> visualize.MeshcatVisualizer:
    """Open a MeshCat visualizer in a Web browser.

    Args:
        robot: Pinocchio robot wrapper with its model and data.

    Returns:
        MeshCat visualizer.
    """
    visualizer = visualize.MeshcatVisualizer(
        robot.model, robot.collision_model, robot.visual_model
    )
    robot.setVisualizer(visualizer, init=False)
    visualizer.initViewer(open=True)
    visualizer.loadViewerModel()
    return visualizer
