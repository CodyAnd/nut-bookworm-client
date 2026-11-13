# Build

## Target

- OS: Debian GNU/Linux 12 (Bookworm)
- Architecture: amd64
- Upstream: Network UPS Tools 2.8.1
- Debian packaging baseline: Bookworm `nut 2.8.0-7`
- Binary packages selected: `nut-client`, `libupsclient6`
- Local package version: `2.8.1-7~bookworm1`

## Build environment used for the initial build

The initial successful build was performed in an isolated, unprivileged Debian 12 LXC container (CT 125), with 2 vCPU, 2 GiB RAM and 8 GiB root filesystem. It was not built on the PBS or Proxmox VE hosts.

The working source tree was:

```text
/usr/src/nut-packaging/nut-2.8.1-bookworm
```

The tree combined upstream NUT 2.8.1 with Debian Bookworm packaging copied from the Bookworm 2.8.0-7 source package.

## Important build settings

The build used the Bookworm host multiarch tuple and selected only the two client packages:

```sh
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
cd /usr/src/nut-packaging/nut-2.8.1-bookworm
export DEB_HOST_MULTIARCH="$(dpkg-architecture -qDEB_HOST_MULTIARCH)"
export DH_OPTIONS="-pnut-client -plibupsclient6"
dpkg-buildpackage -b -uc -us -d
```

The locale exports are a requirement of the CT 125 build environment; they are not required on the PVE or PBS hosts.

The `-d` option bypassed the full source package's generic Build-Depends check because the Debian source package declares dependencies for server drivers, CGI, and documentation outputs not selected for this client-only build. It must not be interpreted as proof that arbitrary build environments have all required dependencies. A clean build procedure must explicitly install and validate the actual required toolchain and libraries.

## Configure options

The Debian rules were adapted to disable unneeded components, including CGI, USB, SNMP, Avahi, IPMI, FreeIPMI, Powerman, and Modbus. Documentation was limited to man pages. The resulting configure run confirmed `--with-doc=man` and the correct multiarch library path.

## Build outputs

The initial build produced:

- `nut-client_2.8.1-7~bookworm1_amd64.deb`
- `libupsclient6_2.8.1-7~bookworm1_amd64.deb`

Debug-symbol packages were also produced by the build system.

## Reproducibility status

The initial build succeeded, but this repository does not yet contain the complete packaging tree, dependency manifest, or an automated clean-checkout build script. Until those are committed and a clean rebuild is verified, the build should be treated as **successfully built once, not yet proven reproducible**.
