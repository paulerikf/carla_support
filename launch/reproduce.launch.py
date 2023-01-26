import os
import sys

import launch
import launch_ros.actions
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def local_config_file(name):
    return os.path.join(get_package_share_directory('carla_support'), 'config/carla_sensors', name)


arguments = [
    DeclareLaunchArgument(name='town', default_value='Town04'),
    DeclareLaunchArgument(name='drone_config', default_value=local_config_file('drone_front_rgb.json')),
    DeclareLaunchArgument(name='car_config', default_value=local_config_file('car_rgb.json')),
]


spawn_car = launch.actions.IncludeLaunchDescription(
    launch.launch_description_sources.PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory(
            'carla_spawn_objects'), 'carla_example_ego_vehicle.launch.py')
    ),
    launch_arguments={
        'objects_definition_file': LaunchConfiguration('car_config')
        #spawn_point_param_name: launch.substitutions.LaunchConfiguration('spawn_point'),
    }.items()
)


def spawn_objects(objects_definition_file):
    carla_spawn_objects_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory(
                'carla_spawn_objects'), 'carla_spawn_objects.launch.py')
        ),
        launch_arguments={
            'objects_definition_file': objects_definition_file
            # spawn_point_param_name: LaunchConfiguration('spawn_point'),
        }.items()
    )
    return carla_spawn_objects_launch


spawn_drone = spawn_objects(LaunchConfiguration('drone_config'))


bridge = launch.actions.IncludeLaunchDescription(
    launch.launch_description_sources.PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory(
            'carla_ros_bridge'), 'carla_ros_bridge.launch.py')
    ),
    launch_arguments={
        'town': LaunchConfiguration('town'),
        'timeout': '30.0',
        'fixed_delta_seconds': '0.06',
    }.items()
)

def generate_launch_description():
    return launch.LaunchDescription([
        *arguments,
        bridge,
        spawn_car,
        spawn_drone
    ])
