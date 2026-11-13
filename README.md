# NUT 2.8.1 client for Debian 12 (Bookworm)

A Bookworm-compatible build of the NUT client components used by a Proxmox Backup Server (PBS) NUT Secondary.

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

The selected client packages have been successfully built in an isolated Debian 12 LXC build container:

- `nut-client 2.8.1-7~bookworm1`
- `libupsclient6 2.8.1-7~bookworm1`

The generated package contents were inspected. The `nut-monitor.service` unit in `nut-client` references the tmpfiles configuration shipped by that package: `/usr/lib/tmpfiles.d/nut-client.conf`.

Both packages were installed and tested on a Debian 12 PBS host. The existing `/etc/nut/nut.conf` and `/etc/nut/upsmon.conf` configuration was preserved. The `nut-monitor.service` is active, its `ExecStartPre` command succeeds, and `upsc` reports the UPS status as `OL`.

**Reproducibility is not yet established.** A clean build from a fresh repository checkout, with all build dependencies explicitly installed and validated, has not yet been completed. A full NUT FSD and coordinated shutdown test has also not been performed.

## Repository contents

- `BUILD.md` — build environment, source inputs, and build procedure/status.
- `PACKAGING.md` — packaging adaptations and rationale.
- `SECURITY.md` — secrets and deployment safety.
- `LICENSE` — project documentation/license notice.

## Important

Do not install these packages on Debian 13 (Trixie) or other releases without rebuilding and validating dependencies for that target. Do not mix Trixie binaries into Bookworm: their libc and t64 dependencies are incompatible with Debian 12.

Do not commit host-specific NUT configuration, UPS credentials, passwords, private keys, or local `.deb` artifacts.
