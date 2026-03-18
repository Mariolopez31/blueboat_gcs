# blueboat_gcs

ROS 2 package for the BlueBoat Ground Control Station (GCS) at CIRTESU.

It is intended to run on the operator PC and provides:

- RViz startup with a predefined configuration
- publication of a reference `.pcd` map
- publication of the CIRTESU mesh as a marker

## Repository layout

```text
blueboat_gcs/
├── launch/
│   └── gcs.launch.py
├── maps/
│   └── cirtesu_map.pcd
├── meshes/
│   └── cirtesu.dae
├── rviz/
│   └── blueboat_gcs.rviz
├── scripts/
│   └── cirtesu_mesh_marker.py
├── package.xml
├── CMakeLists.txt
└── README.md
````

## Requirements

* Ubuntu 22.04
* ROS 2 Humble
* `pcl_ros`
* `rviz2`

Install dependencies:

```bash
sudo apt update
sudo apt install ros-humble-pcl-ros ros-humble-rviz2 ros-humble-tf2-ros
```

## Submodule workflow

`blueboat_gcs` is intended to be used as a submodule inside the main `blueboat_cirtesu` repository.

If cloning the parent repository:

```bash
git clone --recurse-submodules https://github.com/Mariolopez31/blueboat_cirtesu.git
```

If already cloned:

```bash
git submodule update --init --recursive
```

When modifying this package:

1. Commit and push changes inside `blueboat_gcs`
2. Go back to the parent repository
3. Commit the updated submodule reference there

Example:

```bash
cd src/blueboat_gcs
git add .
git commit -m "Update GCS package"
git push
```

Then in the parent repo:

```bash
git add src/blueboat_gcs
git commit -m "Update blueboat_gcs submodule"
git push
```

## Build

From the workspace root:

```bash
cd ~/cirtesu_ws
colcon build --packages-select blueboat_gcs
source install/setup.bash
```

## Run

```bash
ros2 launch blueboat_gcs gcs.launch.py
```

This launches:

* a static transform from `map` to `cirtesu_base_link`
* the `.pcd` map publisher
* the CIRTESU mesh marker publisher
* RViz

## Frames

Current environment setup:

```text
map
└── cirtesu_base_link
```

The mesh is published in `cirtesu_base_link`.

The point cloud map is currently also published in `map`.

