cmake_minimum_required(VERSION 3.8)
project(blueboat_gcs)

find_package(ament_cmake REQUIRED)

install(
  PROGRAMS
    scripts/cirtesu_mesh_marker.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY
    launch
    rviz
    maps
    meshes
    resource
  DESTINATION share/${PROJECT_NAME}
)

ament_package()