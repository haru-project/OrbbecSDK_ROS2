from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import PushRosNamespace
from launch.actions import GroupAction
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import Node
import os


def generate_launch_description():
    def prefixed_frame_expr(suffix: str):
        return PythonExpression(
            [
                "'",
                LaunchConfiguration("tf_prefix"),
                "/",
                LaunchConfiguration("camera_name"),
                suffix,
                "'",
            ]
        )

    # Camera configuration parameters
    camera_args = [
        DeclareLaunchArgument("camera_name", default_value="camera"),
        DeclareLaunchArgument("depth_registration", default_value="false"),
        DeclareLaunchArgument("serial_number", default_value=""),
        DeclareLaunchArgument("usb_port", default_value=""),
        DeclareLaunchArgument("device_num", default_value="1"),
        DeclareLaunchArgument("uvc_backend", default_value="libuvc"),  # libuvc or v4l2
        DeclareLaunchArgument("product_id", default_value=""),
        DeclareLaunchArgument("enable_point_cloud", default_value="true"),
        DeclareLaunchArgument("cloud_frame_id", default_value=""),
        DeclareLaunchArgument("enable_colored_point_cloud", default_value="true"),
        DeclareLaunchArgument("point_cloud_qos", default_value="default"),
        DeclareLaunchArgument("connection_delay", default_value="100"),
        DeclareLaunchArgument("color_width", default_value="1280"),
        DeclareLaunchArgument("color_height", default_value="720"),
        DeclareLaunchArgument("color_fps", default_value="30"),
        DeclareLaunchArgument("color_format", default_value="MJPG"),
        DeclareLaunchArgument("enable_color", default_value="true"),
        DeclareLaunchArgument("color_flip", default_value="false"),
        DeclareLaunchArgument("color_qos", default_value="default"),
        DeclareLaunchArgument("color_camera_info_qos", default_value="default"),
        DeclareLaunchArgument("enable_color_auto_exposure", default_value="true"),
        DeclareLaunchArgument("color_ae_max_exposure", default_value="-1"),
        DeclareLaunchArgument("color_exposure", default_value="-1"),
        DeclareLaunchArgument("color_gain", default_value="-1"),
        DeclareLaunchArgument("color_brightness", default_value="-1"),
        DeclareLaunchArgument("enable_color_auto_white_balance", default_value="true"),
        DeclareLaunchArgument("color_white_balance", default_value="-1"),
        DeclareLaunchArgument("depth_width", default_value="640"),
        DeclareLaunchArgument("depth_height", default_value="576"),
        DeclareLaunchArgument("depth_fps", default_value="30"),
        DeclareLaunchArgument("depth_format", default_value="Y16"),
        DeclareLaunchArgument("enable_depth", default_value="true"),
        DeclareLaunchArgument("depth_flip", default_value="false"),
        DeclareLaunchArgument("depth_qos", default_value="default"),
        DeclareLaunchArgument("depth_camera_info_qos", default_value="default"),
        DeclareLaunchArgument("ir_width", default_value="640"),
        DeclareLaunchArgument("ir_height", default_value="576"),
        DeclareLaunchArgument("ir_fps", default_value="30"),
        DeclareLaunchArgument("ir_format", default_value="Y16"),
        DeclareLaunchArgument("enable_ir", default_value="true"),
        DeclareLaunchArgument("ir_flip", default_value="false"),
        DeclareLaunchArgument("ir_qos", default_value="default"),
        DeclareLaunchArgument("ir_camera_info_qos", default_value="default"),
        DeclareLaunchArgument("enable_ir_auto_exposure", default_value="true"),
        DeclareLaunchArgument("ir_ae_max_exposure", default_value="-1"),
        DeclareLaunchArgument("ir_exposure", default_value="-1"),
        DeclareLaunchArgument("ir_gain", default_value="-1"),
        DeclareLaunchArgument("ir_brightness", default_value="-1"),
        DeclareLaunchArgument("enable_sync_output_accel_gyro", default_value="true"),
        DeclareLaunchArgument("enable_accel", default_value="false"),
        DeclareLaunchArgument("accel_rate", default_value="200hz"),
        DeclareLaunchArgument("accel_range", default_value="4g"),
        DeclareLaunchArgument("enable_gyro", default_value="false"),
        DeclareLaunchArgument("gyro_rate", default_value="200hz"),
        DeclareLaunchArgument("gyro_range", default_value="1000dps"),
        DeclareLaunchArgument("linear_accel_cov", default_value="0.01"),
        DeclareLaunchArgument("angular_vel_cov", default_value="0.01"),
        DeclareLaunchArgument("publish_tf", default_value="true"),
        DeclareLaunchArgument("tf_publish_rate", default_value="0.0"),
        DeclareLaunchArgument("ir_info_url", default_value=""),
        DeclareLaunchArgument("color_info_url", default_value=""),
        DeclareLaunchArgument("log_level", default_value="none"),
        DeclareLaunchArgument("enable_publish_extrinsic", default_value="false"),
        DeclareLaunchArgument("enable_d2c_viewer", default_value="false"),
        DeclareLaunchArgument("enable_ldp", default_value="true"),
        DeclareLaunchArgument("enable_noise_removal_filter", default_value="false"),
        DeclareLaunchArgument("enable_decimation_filter", default_value="false"),
        DeclareLaunchArgument("enable_spatial_filter", default_value="false"),
        DeclareLaunchArgument("enable_temporal_filter", default_value="false"),
        DeclareLaunchArgument("enable_hole_filling_filter", default_value="false"),
        DeclareLaunchArgument("enable_threshold_filter", default_value="false"),
        DeclareLaunchArgument("noise_removal_filter_min_diff", default_value="10"),
        DeclareLaunchArgument("noise_removal_filter_max_size", default_value="50"),
        DeclareLaunchArgument("decimation_filter_scale", default_value="-1"),
        DeclareLaunchArgument("spatial_filter_alpha", default_value="-1.0"),
        DeclareLaunchArgument("spatial_filter_diff_threshold", default_value="-1"),
        DeclareLaunchArgument("spatial_filter_magnitude", default_value="-1"),
        DeclareLaunchArgument("spatial_filter_radius", default_value="-1"),
        DeclareLaunchArgument("temporal_filter_diff_threshold", default_value="-1.0"),
        DeclareLaunchArgument("temporal_filter_weight", default_value="-1.0"),
        DeclareLaunchArgument("hole_filling_filter_mode", default_value=""),
        DeclareLaunchArgument("threshold_filter_max", default_value="-1"),
        DeclareLaunchArgument("threshold_filter_min", default_value="-1"),
        DeclareLaunchArgument("sync_mode", default_value="standalone"),
        DeclareLaunchArgument("enable_frame_sync", default_value="true"),
        DeclareLaunchArgument("depth_delay_us", default_value="0"),
        DeclareLaunchArgument("color_delay_us", default_value="0"),
        DeclareLaunchArgument("trigger2image_delay_us", default_value="0"),
        DeclareLaunchArgument("trigger_out_delay_us", default_value="0"),
        DeclareLaunchArgument("trigger_out_enabled", default_value="false"),
        DeclareLaunchArgument("ordered_pc", default_value="false"),
        DeclareLaunchArgument("enable_depth_scale", default_value="true"),
        DeclareLaunchArgument("align_mode", default_value="SW"),
        DeclareLaunchArgument("align_target_stream", default_value="COLOR"),  # COLOR or DEPTH
        DeclareLaunchArgument("laser_energy_level", default_value="-1"),
        DeclareLaunchArgument("enable_heartbeat", default_value="false"),
        DeclareLaunchArgument("time_domain", default_value="global"),
        DeclareLaunchArgument("device_preset", default_value="Custom"),
    ]

    # TF configuration parameters (kept separate for clarity)
    tf_args = [
        DeclareLaunchArgument(
            "tf_prefix",
            default_value=PythonExpression(
                [
                    "'strawberry/camera' if int(",
                    LaunchConfiguration("device_num"),
                    ") <= 1 else 'strawberry/camera_' + str(",
                    LaunchConfiguration("device_num"),
                    ")",
                ]
            ),
        ),
        DeclareLaunchArgument("world_frame", default_value="world"),
        DeclareLaunchArgument("pos_x", default_value="0.0"),
        DeclareLaunchArgument("pos_y", default_value="0.0"),
        DeclareLaunchArgument("pos_z", default_value="1.0"),
        DeclareLaunchArgument("att_roll", default_value="0.0"),
        DeclareLaunchArgument("att_pitch", default_value="0.0"),
        DeclareLaunchArgument("att_yaw", default_value="0.0"),
        DeclareLaunchArgument("camera_offset_x", default_value="0.0"),
        DeclareLaunchArgument("camera_offset_y", default_value="0.0"),
        DeclareLaunchArgument("camera_offset_z", default_value="0.0"),
        DeclareLaunchArgument("camera_roll", default_value="0.0"),
        DeclareLaunchArgument("camera_pitch", default_value="0.0"),
        DeclareLaunchArgument("camera_yaw", default_value="0.0"),
    ]

    frame_args = [
        DeclareLaunchArgument(
            "camera_link_frame_id",
            default_value=PythonExpression(
                ["'", LaunchConfiguration("tf_prefix"), "/camera_link'"]
            ),
        ),
        DeclareLaunchArgument(
            "accel_gyro_optical_frame_id",
            default_value=prefixed_frame_expr("_accel_gyro_optical_frame"),
        ),
    ]
    camera_frame_suffixes = [
        ("camera_color_frame_id", "_color_frame"),
        ("camera_depth_frame_id", "_depth_frame"),
        ("camera_ir_frame_id", "_ir_frame"),
        ("camera_left_ir_frame_id", "_left_ir_frame"),
        ("camera_right_ir_frame_id", "_right_ir_frame"),
        ("camera_accel_frame_id", "_accel_frame"),
        ("camera_gyro_frame_id", "_gyro_frame"),
    ]
    optical_frame_suffixes = [
        ("color_optical_frame_id", "_color_optical_frame"),
        ("depth_optical_frame_id", "_depth_optical_frame"),
        ("ir_optical_frame_id", "_ir_optical_frame"),
        ("left_ir_optical_frame_id", "_left_ir_optical_frame"),
        ("right_ir_optical_frame_id", "_right_ir_optical_frame"),
        ("accel_optical_frame_id", "_accel_optical_frame"),
        ("gyro_optical_frame_id", "_gyro_optical_frame"),
    ]
    for arg_name, suffix in camera_frame_suffixes + optical_frame_suffixes:
        frame_args.append(
            DeclareLaunchArgument(arg_name, default_value=prefixed_frame_expr(suffix))
        )

    args = camera_args + tf_args + frame_args

    # Node configuration
    parameter_args = camera_args + frame_args
    camera_parameters = [{arg.name: LaunchConfiguration(arg.name)} for arg in parameter_args]

    tf_nodes = [
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="tf_world_to_strawberry_camera",
            arguments=[
                LaunchConfiguration("pos_x"),
                LaunchConfiguration("pos_y"),
                LaunchConfiguration("pos_z"),
                LaunchConfiguration("att_roll"),
                LaunchConfiguration("att_pitch"),
                LaunchConfiguration("att_yaw"),
                LaunchConfiguration("world_frame"),
                LaunchConfiguration("tf_prefix"),
            ],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="tf_strawberry_camera_to_camera_link",
            arguments=[
                LaunchConfiguration("camera_offset_x"),
                LaunchConfiguration("camera_offset_y"),
                LaunchConfiguration("camera_offset_z"),
                LaunchConfiguration("camera_roll"),
                LaunchConfiguration("camera_pitch"),
                LaunchConfiguration("camera_yaw"),
                LaunchConfiguration("tf_prefix"),
                LaunchConfiguration("camera_link_frame_id"),
            ],
        ),
    ]
    # get  ROS_DISTRO
    ros_distro = os.environ["ROS_DISTRO"]
    if ros_distro == "foxy":
        return LaunchDescription(
            args
            + [
                Node(
                    package="orbbec_camera",
                    executable="orbbec_camera_node",
                    name="ob_camera_node",
                    namespace=LaunchConfiguration("camera_name"),
                    parameters=camera_parameters,
                    output="screen",
                )
            ]
            + tf_nodes
        )
    # Define the ComposableNode
    else:
        # Define the ComposableNode
        compose_node = ComposableNode(
            package="orbbec_camera",
            plugin="orbbec_camera::OBCameraNodeDriver",
            name=LaunchConfiguration("camera_name"),
            namespace="",
            parameters=camera_parameters,
        )
        # Define the ComposableNodeContainer
        container = ComposableNodeContainer(
            name="camera_container",
            namespace="",
            package="rclcpp_components",
            executable="component_container",
            composable_node_descriptions=[
                compose_node,
            ],
            output="screen",
        )
        # Launch description
        ld = LaunchDescription(
            args
            + [
                GroupAction(
                    [PushRosNamespace(LaunchConfiguration("camera_name")), container]
                )
            ]
            + tf_nodes
        )
        return ld
