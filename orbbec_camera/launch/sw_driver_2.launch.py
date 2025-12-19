from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import PushRosNamespace
from launch.actions import GroupAction
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import Node
import os


def generate_launch_description():
    # ============================================================================
    # Launch control parameters
    # ============================================================================
    # These control which pieces are launched (enable/disable whole groups)
    control_args = [
        DeclareLaunchArgument("launch_world_to_strawberry_tf", default_value="true"),
        DeclareLaunchArgument("frame_prefix", default_value="strawberry"),
        DeclareLaunchArgument("launch_frame_prefix_to_camera", default_value="true"),
        DeclareLaunchArgument("namespace_prefix", default_value=""),
    ]

    # ============================================================================
    # Static TF (world -> strawberry) parameters
    # ============================================================================
    tf_world_args = [
        DeclareLaunchArgument("world_frame", default_value="world"),
        DeclareLaunchArgument("strawberry_root", default_value="strawberry"),
        DeclareLaunchArgument("world_to_strawberry_x", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_y", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_z", default_value="1.0"),
        DeclareLaunchArgument("world_to_strawberry_roll", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_pitch", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_yaw", default_value="0.0"),
    ]

    # ============================================================================
    # Static TF (strawberry -> strawberry/orbbec_femto_bolt_link) parameters
    # ============================================================================
    tf_camera_args = [
        DeclareLaunchArgument("namespace", default_value=LaunchConfiguration("frame_prefix")),
        DeclareLaunchArgument("camera_initial_tf", default_value="strawberry/orbbec_femto_bolt_link"),
        DeclareLaunchArgument("world_to_strawberry_x", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_y", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_z", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_roll", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_pitch", default_value="0.0"),
        DeclareLaunchArgument("world_to_strawberry_yaw", default_value="0.0"),
    ]

    # ============================================================================
    # Orbbec camera parameters
    # ============================================================================
    args = [
        DeclareLaunchArgument("camera_name", default_value="orbbec_femto_bolt"),
        DeclareLaunchArgument("depth_registration", default_value="true"),
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
        DeclareLaunchArgument('enable_noise_removal_filter', default_value='false'),
        DeclareLaunchArgument('enable_decimation_filter', default_value='false'),
        DeclareLaunchArgument('enable_spatial_filter', default_value='false'),
        DeclareLaunchArgument('enable_temporal_filter', default_value='false'),
        DeclareLaunchArgument('enable_hole_filling_filter', default_value='false'),
        DeclareLaunchArgument("enable_threshold_filter", default_value="false"),
        DeclareLaunchArgument('noise_removal_filter_min_diff', default_value='10'),
        DeclareLaunchArgument('noise_removal_filter_max_size', default_value='50'),
        DeclareLaunchArgument('decimation_filter_scale', default_value='-1'),
        DeclareLaunchArgument('spatial_filter_alpha', default_value='-1.0'),
        DeclareLaunchArgument('spatial_filter_diff_threshold', default_value='-1'),
        DeclareLaunchArgument('spatial_filter_magnitude', default_value='-1'),
        DeclareLaunchArgument('spatial_filter_radius', default_value='-1'),
        DeclareLaunchArgument('temporal_filter_diff_threshold', default_value='-1.0'),
        DeclareLaunchArgument('temporal_filter_weight', default_value='-1.0'),
        DeclareLaunchArgument('hole_filling_filter_mode', default_value=''),
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
        DeclareLaunchArgument('align_target_stream', default_value='COLOR'),# COLOR or DEPTH
        DeclareLaunchArgument("laser_energy_level", default_value="-1"),
        DeclareLaunchArgument("enable_heartbeat", default_value="false"),
        DeclareLaunchArgument("time_domain", default_value="global"),
        DeclareLaunchArgument('device_preset', default_value='Custom'),
    ]

    # combine all declared args for the LaunchDescription
    args = control_args + tf_world_args + tf_camera_args + args

    # Node configuration
    parameters = [{arg.name: LaunchConfiguration(arg.name)} for arg in args]
    # get  ROS_DISTRO
    ros_distro = os.environ["ROS_DISTRO"]

    # static tf node (world -> strawberry)
    tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="tf_world_to_strawberry",
        condition=IfCondition(LaunchConfiguration("launch_world_to_strawberry_tf")),
        arguments=[
            LaunchConfiguration("world_to_strawberry_x"),
            LaunchConfiguration("world_to_strawberry_y"),
            LaunchConfiguration("world_to_strawberry_z"),
            LaunchConfiguration("world_to_strawberry_roll"),
            LaunchConfiguration("world_to_strawberry_pitch"),
            LaunchConfiguration("world_to_strawberry_yaw"),
            LaunchConfiguration("world_frame"),
            LaunchConfiguration("strawberry_root"),
        ],
    )

    # static tf node (strawberry -> strawberry/orbbec_femto_bolt_link)
    tf_camera_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="tf_strawberry_to_camera",
        condition=IfCondition(LaunchConfiguration("launch_frame_prefix_to_camera")),
        arguments=[
            LaunchConfiguration("world_to_strawberry_x"),
            LaunchConfiguration("world_to_strawberry_y"),
            LaunchConfiguration("world_to_strawberry_z"),
            LaunchConfiguration("world_to_strawberry_roll"),
            LaunchConfiguration("world_to_strawberry_pitch"),
            LaunchConfiguration("world_to_strawberry_yaw"),
            LaunchConfiguration("strawberry_root"),
            LaunchConfiguration("camera_initial_tf"),
        ],
    )

    if ros_distro == "foxy":
        return LaunchDescription(
            args
            + [
                GroupAction(
                    [
                        PushRosNamespace(LaunchConfiguration("namespace_prefix")),
                        PushRosNamespace(LaunchConfiguration("camera_name")),
                        Node(
                            package="orbbec_camera",
                            executable="orbbec_camera_node",
                            name="ob_camera_node",
                            namespace="",
                            parameters=parameters,
                            output="screen",
                        ),
                    ]
                )
            ]
            + [tf_node, tf_camera_node]
        )
    else:
        compose_node = ComposableNode(
            package="orbbec_camera",
            plugin="orbbec_camera::OBCameraNodeDriver",
            name="ob_camera_node",
            namespace="",
            parameters=parameters,
        )
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
        ld = LaunchDescription(
            args
            + [
                GroupAction(
                    [
                        PushRosNamespace(LaunchConfiguration("namespace_prefix")),
                        PushRosNamespace(LaunchConfiguration("camera_name")),
                        container,
                    ]
                )
            ]
            + [tf_node, tf_camera_node]
        )
        return ld
