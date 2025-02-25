from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_px4_estimation',
            executable='uwb_driver',
            parameters=[
                {'topic_name': '/uwb_sensor/Iris'}
            ]
        ),
        Node(
            package='ros2_px4_estimation',
            executable='uwb_positioning',
            namespace='LS_uwb_estimator',
            parameters=[
                {"method": "LS"},
                {"allowed_delay_ns": 1e8},
                {"max_range": 30.0}
            ]
        ),
        Node(
            package = 'ros2_px4_estimation',
            executable='uwb_positioning',
            namespace = 'GN_10iter_uwb_estimator',
            parameters=[
                {"method": "GN"},
                {"iterations": 10},
                {"allowed_delay_ns": 1e8},
                {"max_range": 30.0}
            ]
        ),
        Node(
            package = 'ros2_px4_estimation',
            executable='uwb_positioning',
            namespace = 'GN_1iter_uwb_estimator',
            parameters=[
                {"method": "GN"},
                {"iterations": 1},
                {"allowed_delay_ns": 1e8},
                {"max_range": 30.0}
            ]
        ),
        Node(
            package = 'ros2_px4_estimation',
            executable='ukf_positioning',
            namespace = 'ukf_positioning',
            parameters=[
                {"deltaT": 5e-3},
                {"R_uwb": 1e-3},
                {'Q': 1e-3}
            ]
        )
    ])
