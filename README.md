## Overview

The `wagoalex/wled-controller` Docker image provides an efficient way to manage and control your WLED devices through simple and configurable Python scripts. This container allows users to set LED colors and effects on their devices using environment variables.

## Usage

To use this Docker image, you'll need to define your Docker Compose configuration and specify the required environment variables. Below is an example of a Docker Compose file to help you get started:

```yaml
version: '3.8'  # Specifies the version of Docker Compose file format
services:
  wled-controller:
    image: wagoalex/wled-controller:latest  # Specifies the Docker image to use for this service
    # container_name: wled-controller  # Optionally, you can uncomment this line to set a custom container name
    environment:
      - WLED_IP=192.168.2.82               # The IP address of the WLED device to be controlled
      - COLOR_TO_SET="[200, 110, 0]"       # The color to set on the WLED device in RGB format [GREEN, RED, BLUE]
                                           # 200, 110, 0 corresponds to WAGO Green
      - SEG_START=0                        # Start position for the LED segment
      - SEG_STOP=108                       # Stop position for the LED segment
      - SEG_FX=3                           # Effect ID for the LED segment, 3 is the default(="transfering animation data)
    command: ["python", "script.py"]       # The command to run the Python script within the container

## Environment Variables

The following environment variables can be set to configure the behavior of the container:

- `WLED_IP`: The IP address of the WLED device to be controlled (default: `192.168.3.242`)
- `COLOR_TO_SET`: The color to set on the WLED device in RGB format (e.g., `"[200, 110, 0]"` for WAGO Green)
- `SEG_START`: Start position for the LED segment (default: `0`)
- `SEG_STOP`: Stop position for the LED segment (default: `20`)
- `SEG_FX`: Effect ID for the LED segment (default: `3`)


## Building and Running the Image

The Dockerfile uses a multi-stage build to ensure the final image is as small as possible. It starts with a base Python image, installs any dependencies, and then copies everything to a minimal runtime image.

To build and run the image:

1. **Build the Docker Image**:
    ```bash
    docker build -t wagoalex/wled-controller .
    ```

2. **Run the Docker Container**:
    ```bash
    docker run --env WLED_IP=192.168.2.82 --env COLOR_TO_SET="[200, 110, 0]" wagoalex/wled-controller
    ```
