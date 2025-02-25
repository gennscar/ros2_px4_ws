from launch import LaunchDescription
from launch_ros.actions import Node


yaw_topic_name = "/yaw_sensor/estimated_yaw"
drone_name = "/drone"

kf_params_pos = [

    [{'deltaT': 1e-1}, {'R_uwb': 1e-2}, {'R_px4': 5e-1}, {'R_range_sensor': 1e-2},
    {'R_compass': 1e0}, {'Q_drone': 5e-3}, {'Q_rover': 1e-3}, 
    {'Q_compass': 2e3}, {'Q_rover_z': 1e-8}, {'Q_drone_z': 1e-1}, 
    {'rng_sensor_fuse_radius': 0.40}, {'vehicle_namespace': drone_name}, {'uwb_estimator': "/LS_uwb_estimator/norot_pos"},
    {"yaw_subscriber_topic": yaw_topic_name}, {"enable_watchdog": True}],
]



def generate_launch_description():
    ld = LaunchDescription()

    
    ld.add_entity(Node(
        package = "ros2_px4_estimation",
        executable = "gazebo_yaw_estimator",
        name = "gazebo_yaw_estimator",
        parameters = [
            {"yaw_publisher_topic": yaw_topic_name},
            {"yaw_offset": 25.0},
            {"yaw_std_dev": 0.75}
        ]
    ))

    ld.add_entity(Node(
        package='ros2_px4_estimation',
        executable='drone_rover_uwb_positioning',
        namespace='LS_uwb_estimator',
        parameters=[
            {"sensor_id": "tag_0"},
            {"allowed_delay_ns": 1e8},
            {"max_range": 15.0},
            {"yaw_subscriber_topic": yaw_topic_name},
            {"method": "LS"}
        ]
    ))

    ld.add_entity(Node(
        package='ros2_px4_estimation',
        executable='apriltag_yaw_estimator',
        namespace='apriltag_yaw_estimator',
    ))

    for i, param in enumerate(kf_params_pos):
        ld.add_entity(Node(
            package='ros2_px4_estimation',
            executable='drone_rover_kf_pos_theta_sim',
            namespace='KF_pos_estimator_' + str(i),
            parameters=param
        ))

    return ld
