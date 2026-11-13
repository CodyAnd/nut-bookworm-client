# NUT 2.8.1 client for Debian 12 (Bookworm)

A reproducible, Bookworm-compatible build of the NUT client components used by a Proxmox Backup Server (PBS) NUT Secondary.

## Scope

This project builds only:

- `nut-client`
- `libupsclient6`

The package set is intended for Debian 12 (Bookworm), amd64. It is based on upstream Network UPS Tools (NUT) 2.8.1 with Debian packaging adapted from Bookworm's `nut 2.8.0-7` source package.

This is a local compatibility build, **not an official Debian package** and not a general-purpose replacement for Debian's NUT packages.

## Why 2.8.1?

The PBS shutdown design uses the NUT 2.8.1 `SHUTDOWNEXIT` directive. With `SHUTDOWNEXIT no`, a Secondary `upsmon` can remain connected to the Primary while PBS proceeds through its shutdown sequence. The Primary can then use `HOSTSYNC` to wait for the Secondary to disconnect before shutting down.

The built `upsmon` binary and generated `upsmon.conf(5)` manual were checked for `SHUTDOWNEXIT`.

## Build status

The initial package build has succeeded in an isolated Debian 12 LXC build container. The resulting packages were installed on a Debian 12 PBS test host:

- `nut-client 2.8.1-7~bookworm1`
- `libupsclient6 2.8.1-7~bookworm1`

The package upgrade preserved the existing `/etc/nut/nut.conf` and `/etc/nut/upsmon.conf` files. Service start/restart actions were blocked during that installation; the PBS NUT monitor was left inactive.

**Reproducibility work is still in progress.** The exact build scripts and complete packaging inputs must be committed and tested from a clean checkout before this repository can claim a fully reproducible build.

## Repository contents

- `BUILD.md` — build environment, source inputs, and build procedure/status.
- `PACKAGING.md` — packaging adaptations and rationale.
- `SECURITY.md` — secrets and deployment safety.
- `LICENSE` — project documentation/license notice.

## Important

Do not install these packages on Debian 13 (Trixie) or other releases without rebuilding and validating dependencies for that target. Do not mix Trixie binaries into Bookworm: their libc and t64 dependencies are incompatible with Debian 12.

Do not commit host-specific NUT configuration, UPS credentials, passwords, private keys, or local `.deb` artifacts.
