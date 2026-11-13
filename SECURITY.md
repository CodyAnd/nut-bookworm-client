# Security and deployment notes

- Never commit UPS credentials, passwords, private keys, or host-specific `/etc/nut` configuration.
- Do not use production PBS/PVE configuration files as build inputs.
- Build packages in an isolated Debian 12 environment, not on the PBS or PVE host.
- The packages are intended only for Debian 12 Bookworm amd64 unless separately rebuilt and validated.
- Do not install Debian 13/Trixie NUT binaries on Bookworm. Their libc and t64 dependency requirements are not compatible with the Debian 12 base system.
- During package installation on a live PBS host, inspect maintainer scripts and control service activation deliberately. The package post-install script can request a restart of `nut-monitor.service` and `nut.target`.
- Keep the PBS NUT monitor inactive until its final configuration and shutdown coordination have been reviewed.
- Keep NUT powerdown/killpower behavior disabled where the deployment requires UPS output sockets to remain energized after host shutdown. Validate the exact host configuration before enabling monitoring.
