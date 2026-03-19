#!/bin/bash

REALSENSE_CONFIG_PATH="/home/${USERNAME}/.realsense-config.json"

if [[ ! -f "${REALSENSE_CONFIG_PATH}" ]]; then
    cat > "${REALSENSE_CONFIG_PATH}" <<'EOF'
{
  "context": {
    "device-mask": 511,
    "dds": {
      "enabled": true,
      "domain": 0
    }
  }
}
EOF
    chown "${USERNAME}:${USERNAME}" "${REALSENSE_CONFIG_PATH}"
    echo "Created ${REALSENSE_CONFIG_PATH} with DDS-enabled RealSense defaults"
fi
