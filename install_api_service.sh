#!/bin/bash
SCRIPT_PATH="/internship/api_service.py"

PYTHON_PATH="/internship/internship/bin/python"

SERVICE_NAME="apache_api_service"

SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "[Unit]
Description=Api Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=$(dirname ${SCRIPT_PATH})
ExecStart=${PYTHON_PATH} ${SCRIPT_PATH}
Restart=always

[Install]
WantedBy=multi-user.target
" | sudo tee ${SERVICE_FILE}

sudo systemctl daemon-reload

sudo systemctl start ${SERVICE_NAME}

sudo systemctl enable ${SERVICE_NAME}

sudo systemctl status ${SERVICE_NAME}