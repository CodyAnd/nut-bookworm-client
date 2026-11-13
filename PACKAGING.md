# Debian packaging adaptations

The initial package set was built from upstream NUT 2.8.1 using Debian Bookworm packaging from `nut 2.8.0-7`.

## Version

`2.8.1-7~bookworm1`, distribution `bookworm`.

## Patch series

The Bookworm packaging patch series was reviewed against upstream 2.8.1.

- `0001-reproductible-build.patch`, `0003-install-dev-files-in-usr.patch`, and `0008-drop-w3c-icons.patch` were already represented in upstream 2.8.1 and were not reapplied.
- `appdata-launchable.patch` was not applicable because the upstream AppStream metadata already contained the desktop launchable entry.

The working `debian/patches/series` therefore contained explanatory comments rather than applying those patches.

## Rules changes

The working `debian/rules` differed from the original Bookworm rules in these ways:

1. Disabled unneeded server-side and hardware integrations for this client-only package build: CGI, USB, SNMP, Avahi, IPMI, FreeIPMI, Powerman, and Modbus.
2. Added creation of placeholder `NEWS` and `README` files before `dh_autoreconf`, because the upstream 2.8.1 source tree uses `NEWS.adoc` and `README.adoc` and the autoreconf step expects the legacy filenames.
3. Changed the documentation input from the absent `TODO` to the upstream `TODO.adoc`.
4. Corrected the `nut-monitor.service` tmpfiles configuration path during Debian package installation. The upstream service template refers to `/usr/lib/tmpfiles.d/nut-common-tmpfiles.conf`, but the selected `nut-client` package ships `/usr/lib/tmpfiles.d/nut-client.conf`. The Debian rules now check for the expected original path and replace it with the path provided by `nut-client`.

The configure run selected man-page documentation only because the selected binary package set did not include `nut-doc`.

## Runtime dependency relationship

The built `upsmon` dynamically links to `libupsclient.so.6`. The PBS client installation therefore requires both `nut-client` and `libupsclient6`.

The PBS package set does not include NUT server or hardware driver packages.

## Validation performed

- Package metadata and dependencies were inspected.
- The `upsmon` binary was checked for the `SHUTDOWNEXIT` parser strings in the build container.
- The generated `upsmon.conf(5)` man page documents `SHUTDOWNEXIT boolean|number`.
- On the Debian 12 PBS host, `upsmon -V` reported NUT 2.8.1 and `ldd` resolved `libupsclient.so.6`.
- An APT simulation showed exactly two upgrades and no package additions or removals.
- The generated `nut-client` package was checked to contain `/usr/lib/tmpfiles.d/nut-client.conf` and to reference that path in `nut-monitor.service`.
- The package checksums were verified after transfer to the Debian 12 PBS test host.
- Both packages were installed on PBS, preserving the existing `/etc/nut/nut.conf` and `/etc/nut/upsmon.conf`.
- After installation, `nut-monitor.service` was active and its `ExecStartPre` command completed successfully.
- `upsc` successfully queried the Primary and returned `ups.status: OL`.

A full NUT FSD test and coordinated Primary/Secondary shutdown test have not been performed. A clean build from a fresh repository checkout with an explicitly validated dependency set is also still outstanding.
