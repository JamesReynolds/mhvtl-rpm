# mhvtl-rpm

The [MHVTL](https://sites.google.com/site/linuxvtl2/) project by Mark Harvey is a GPLv2 project to provide a virtual tape interface.

This project provides .spec files and a build to produce a kernel-module DKMS rpm and a userspace rpm targeting CentOS 7.

## Build

```
make
```

optionally:

```
make VERSION=1.5 RELEASE=3
```

## Test

```
vagrant up
```

### Notes:

* This has only been tested with CentOS 7 and MHVTL 1.5-3. Other combinations may not work.
