#!/bin/bash

# Change to root directory
cd \


# Installing Dependencies
sudo apt-get update
sudo apt-get install -y isc-dhcp-server
sudo apt-get install -y isc-dhcp-server nmap


# Editing Configurations
# # /etc/dhcp/dhcpd.conf for isc-dhcp-server
sudo cat <<EOT > /etc/dhcp/dhcpd.conf
# Lease
default-lease-time 86400; # 1d
max-lease-time 604800; # 7d

# Main DHCP Server for the network
authoritative;

# Define Range for DHCP
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.150;
    option routers 192.168.1.1;
}
EOT


# Creating bash scripts
# # start_camera_strean.sh
sudo cat <<EOT > /usr/local/bin/start_camera_stream.sh
#!/bin/bash

libcamera-vid -t 0 --width 1332 --height 990 --inline -o udp://239.0.0.1:8000
EOT

# # start_dhcp_server.sh
sudo cat <<EOT > /usr/local/bin/start_dhcp_server.sh
#!/bin/bash

result=$(sudo nmap --script broadcast-dhcp-discover -e eth0)

if echo "$result" | grep -q "IP Offered"; then
    sudo systemctl stop isc-dhcp-server
else
    sudo systemctl start isc-dhcp-server
fi
EOT


# Setting up systemd services
# # start_camera_stream.service
sudo cat <<EOT > /etc/systemd/system/start_camera_stream.service
[Unit]
Description=Start Camera Stream

[Service]
ExecStart=/usr/local/bin/start_camera_stream.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOT

# # start_dhcp_server.service
sudo cat <<EOT > /etc/systemd/system/start_dhcp_server.service
[Unit]
Description=Start DHCP Server

[Service]
ExecStart=/usr/local/bin/start_dhcp_server.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOT


# Setting up autostart
# # start_camera_stream.service
sudo systemctl daemon-reload
sudo systemctl enable start_camera_stream.service
sudo systemctl start start_camera_stream.service

# # start_dhcp_server.service
sudo systemctl daemon-reload
sudo systemctl enable start_dhcp_server.service
sudo systemctl start start_dhcp_server.service
