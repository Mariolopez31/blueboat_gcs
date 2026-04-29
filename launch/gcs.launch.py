#!/usr/bin/env python3

import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory("blueboat_gcs")
    description_pkg = get_package_share_directory("blueboat_cirtesu_description")

    rviz_config = os.path.join(pkg_share, "rviz", "blueboat_gcs.rviz")
    blueboat_xacro = os.path.join(description_pkg, "urdf", "blueboat_enu_real.xacro")

    map_to_cirtesu = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="map_to_cirtesu_base_link",
        arguments=["0", "0", "0", "3.1416", "0", "3.1416", "map", "cirtesu_base_link"],
        output="screen",
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="blueboat_robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": ParameterValue(
                Command([
                    "xacro ",
                    blueboat_xacro,
                    " environment:=sim",
                    " lookup_csv:="
                ]),
                value_type=str
            )
        }],
    )

    cirtesu_mesh = Node(
        package="blueboat_gcs",
        executable="cirtesu_mesh_marker.py",
        name="cirtesu_mesh_marker",
        output="screen",
        parameters=[{"use_sim_time": False}],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
    )

    return LaunchDescription([
        map_to_cirtesu,
        robot_state_publisher,
        cirtesu_mesh,
        rviz,
    ])
