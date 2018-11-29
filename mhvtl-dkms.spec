URL: http://sites.google.com/site/linuxvtl2/
License: GPLv2
Group: Applications/Archiving
Name: mhvtl-dkms
Version: %{version}
Release: %{release}
Summary: Virtual Tape Library Module
BuildArch: noarch
Source: %{version}-%{release}_release.tar.gz
Requires: dkms kernel-devel make gcc mt-st zlib-devel lzo-devel

%description
A Virtual tape library and tape drives:

Used to emulate hardware robot & tape drives:

VTL consists of a pseudo HBA kernel driver and user-space daemons which
function as the SCSI target.

Communication between the kernel module and the daemons is achieved
via /dev/mhvtl? device nodes.

The kernel module is based on the scsi_debug driver.
The SSC/SMC target daemons have been written from scratch.

%prep
rm -rf %{buildroot}

%build
mkdir -p %{buildroot}/usr/src/mhvtl-%{version}.%{release}
cd %{buildroot}/usr/src/
tar xf %{SOURCE0} mhvtl-%{version}-%{release}_release/kernel
mv mhvtl-%{version}-%{release}_release/kernel/* %{buildroot}/usr/src/mhvtl-%{version}.%{release}/
rm -rf %{buildroot}/*.tar.gz mhvtl-%{version}-%{release}_release
cat > %{buildroot}/usr/src/mhvtl-%{version}.%{release}/dkms.conf <<EOF
PACKAGE_NAME="mhvtl"
PACKAGE_VERSION="%{version}.%{release}"
BUILT_MODULE_NAME[0]="mhvtl"
DEST_MODULE_LOCATION[0]="/kernel/drivers/scsi/"
AUTOINSTALL="yes"
EOF

%clean
rm -rf %{buildroot}

%files
/usr/src/mhvtl-%{version}.%{release}

%post
cd /usr/src/mhvtl-%{version}.%{release}
dkms add     -m mhvtl -v %{version}.%{release}
dkms build   -m mhvtl -v %{version}.%{release}
dkms install -m mhvtl -v %{version}.%{release}

%preun
dkms remove -m mhvtl -v %{version}.%{release} --all

