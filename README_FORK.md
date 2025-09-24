# Fork Notes

This fork customises the Orbbec SDK ROS 2 workspace to match our deployment
requirements. Below is a quick summary of the main differences from upstream
`v2-main`.

## Docker workflow

- `docker/orbbecsdk_ros2.Dockerfile` no longer pulls down Azure Kinect packages.
  It installs the ROS image transport stack, diagnostics interfaces, `libgflags`
  and `nlohmann-json`, and reloads udev rules after package installation.
- `docker/entrypoint.sh` now sources `/opt/ros/${ROS_DISTRO}` and an optional
  `${HOME}/orbbec_ws` overlay before executing the container command.
- When the container starts, the entrypoint reloads udev rules if `/run/udev`
  is available, so host-mounted rules take effect.
- `docker/docker-compose.yaml` defines the `orbbecsdk_ros2_jazzy` service that
  builds from the new Dockerfile and launches `orbbec_camera femto_bolt.launch.py`.
- A blank `docker/.env` file is provided for local overrides; both it and
  `docker/.secrets` are ignored by git.

## CI workflows

- `.github/workflows/main.yml` retains the upstream package build with the
  version bump step under review for future cleanup.
- `.github/workflows/upload_to_ghcr.yml` now runs only after the main workflow
  completes successfully (via `workflow_run`), and it builds/pushes the
  `docker/orbbecsdk_ros2.Dockerfile` image as `ghcr.io/haru-project/orbbecsdk_ros2:latest`.

## Udev helper script

- The original `orbbec_camera/scripts/install_udev_rules.sh` has moved to
  `scripts/download_resources.sh`. The script installs the
  `orbbec_camera/scripts/99-obsensor-libusb.rules` file and refreshes udev.
- Documentation in `README.MD` and `README_CN.MD` points to the new script.

Keep this document up to date as new fork-specific behaviour is introduced, so
contributors have a single reference for the deviations from upstream.
