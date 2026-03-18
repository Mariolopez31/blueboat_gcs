#!/usr/bin/env python3

import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory("blueboat_gcs")

    rviz_config = os.path.join(pkg_share, "rviz", "blueboat_gcs.rviz")
    pcd_file = os.path.join(pkg_share, "maps", "map1_centered.pcd")

    map_to_cirtesu = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="map_to_cirtesu_base_link",
        arguments=["0", "0", "0", "3.1416", "0", "3.1416", "map", "cirtesu_base_link"],
        output="screen",
    )

    cirtesu_pcd = Node(
        package="pcl_ros",
        executable="pcd_to_pointcloud",
        name="cirtesu_pcd_publisher",
        output="screen",
        parameters=[{
            "file_name": pcd_file,
            "tf_frame": "map",
            "interval": 1.0,
        }],
        remappings=[
            ("cloud_pcd", "/map_pointcloud")
        ]
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
        cirtesu_pcd,
        cirtesu_mesh,
        rviz,
    ])