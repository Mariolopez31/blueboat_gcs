#!/usr/bin/env python3

import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory("blueboat_gcs")
    description_pkg = get_package_share_directory("blueboat_cirtesu_description")

    rviz_config = os.path.join(pkg_share, "rviz", "blueboat_gcs.rviz")
    diagnostics_aggregator_config = os.path.join(
        pkg_share, "config", "diagnostic_aggregator.yaml"
    )
    enable_livox_viz = LaunchConfiguration("enable_livox_viz")
    enable_fake_cirtesu_mesh = LaunchConfiguration("enable_fake_cirtesu_mesh")
    enable_diagnostics_aggregator = LaunchConfiguration("enable_diagnostics_aggregator")

    map_to_cirtesu = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="map_to_cirtesu_base_link",
        arguments=[
            "0", "0", "0",
            "3.1416", "0", "3.1416",
            "map", "cirtesu_base_link"
        ],
        output="screen",
        condition=IfCondition(enable_fake_cirtesu_mesh),
    )

    # robot_state_publisher = Node(
    #     package="robot_state_publisher",
    #     executable="robot_state_publisher",
    #     name="blueboat_robot_state_publisher",
    #     output="screen",
    #     parameters=[{
    #         "robot_description": ParameterValue(
    #             Command([
    #                 "xacro ",
    #                 blueboat_xacro,
    #                 " environment:=real",
    #                 " lookup_csv:="
    #             ]),
    #             value_type=str
    #         )
    #     }],
    # )

    cirtesu_mesh = Node(
        package="blueboat_gcs",
        executable="cirtesu_mesh_marker.py",
        name="cirtesu_mesh_marker",
        output="screen",
        parameters=[{"use_sim_time": False}],
        condition=IfCondition(enable_fake_cirtesu_mesh),
    )

    diagnostics_aggregator = Node(
        package="diagnostic_aggregator",
        executable="aggregator_node",
        name="analyzers",
        output="screen",
        parameters=[diagnostics_aggregator_config],
        condition=IfCondition(enable_diagnostics_aggregator),
    )


    # livox2_to_pc2 = Node(
    #     package="livox2_to_pc2",
    #     executable="livox2_to_pc2",
    #     name="livox2_to_pc2",
    #     output="screen",
    #     parameters=[{
    #         "in_topic": "/livox/lidar",
    #         "out_topic": "/blueboat/livox/points_viz",

    #         "sub_reliability": "reliable",
    #         "pub_reliability": "reliable",

    #         "frame_id": "livox_frame",
    #         "include_ring": False,

    #         # Modo conservador para RViz
    #         "publish_rate_hz": 2.0,
    #         "point_stride": 5,
    #         "max_points": 30000,
    #     }],
    #     condition=IfCondition(enable_livox_viz),
    # )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "enable_livox_viz",
            default_value="true",
            description="Launch lightweight Livox CustomMsg to PointCloud2 bridge for RViz",
        ),

        DeclareLaunchArgument(
            "enable_fake_cirtesu_mesh",
            default_value="false",
            description="Launch fake static mesh at map origin. Disable for real FAST-LIO/GPS TF.",
        ),
        DeclareLaunchArgument(
            "enable_diagnostics_aggregator",
            default_value="true",
            description="Launch diagnostic aggregator for Robot Monitor and /diagnostics_agg.",
        ),

        map_to_cirtesu,
        # robot_state_publisher,
        cirtesu_mesh,
        diagnostics_aggregator,
        # livox2_to_pc2,
        rviz,
    ])
