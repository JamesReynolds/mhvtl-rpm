URL: http://sites.google.com/site/linuxvtl2/
License: GPLv2
Group: Applications/Archiving
Name: mhvtl
Version: %{version}
Release: %{release}
Summary: Virtual Tape Library Userspace Daemons
Source: %{version}-%{release}_release.tar.gz
Requires: kernel-devel make gcc mt-st zlib-devel lzo-devel
BuildRequires: lzo-devel zlib-devel
Requires(pre): shadow-utils

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
%setup -n mhvtl-%{version}-%{release}_release

%build
%{__make} VERSION="%{version}.%{release}" %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}
sed -i 's/-g bin/-g $(GROUP)/g' usr/Makefile
%{__make} install USR=`id -nu` SUSER=`id -nu` GROUP=`id -ng` DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,vtl,vtl,755)
%attr(0755, root, root) /etc/init.d/mhvtl
%attr(4755, root, -)    %{_bindir}/vtllibrary
%attr(4755, root, -)    %{_bindir}/vtltape
%attr(0600, root, root) %{_bindir}/update_device.conf
%attr(0755, -, -)       %{_bindir}/make_vtl_media
%attr(0755, -, -)       %{_bindir}/mktape
%attr(0755, -, -)       %{_bindir}/edit_tape
%attr(0755, -, -)       %{_bindir}/vtlcmd
%attr(0755, -, -)       %{_bindir}/dump_tape
%attr(0755, -, -)       %{_bindir}/tapeexerciser
%attr(0755, -, -)       %{_bindir}/build_library_config
/opt/mhvtl
%doc %{_mandir}/man5/device.conf.5.gz
%doc %{_mandir}/man5/mhvtl.conf.5.gz
%doc %{_mandir}/man5/library_contents.5.gz
%doc %{_mandir}/man1/mktape.1.gz
%doc %{_mandir}/man1/vtlcmd.1.gz
%doc %{_mandir}/man1/mhvtl.1.gz
%doc %{_mandir}/man1/edit_tape.1.gz
%doc %{_mandir}/man1/make_vtl_media.1.gz
%doc %{_mandir}/man1/vtllibrary.1.gz
%doc %{_mandir}/man1/build_library_config.1.gz
%doc %{_mandir}/man1/vtltape.1.gz
%attr(755, root, bin) %{_libdir}/libvtlcart.so
%attr(755, root, bin) %{_libdir}/libvtlscsi.so

%pre
getent group vtl >/dev/null || groupadd -r --system vtl
getent passwd vtl >/dev/null || \
    useradd --system -r -g vtl -d /opt/mhvtl -s /bin/sh \
    -c "Virtual Tape Library User" vtl
exit 0

%postun -p /sbin/ldconfig

%post
/sbin/ldconfig
/etc/init.d/mhvtl stop
/sbin/chkconfig --add mhvtl &>/dev/null || :
/bin/systemctl daemon-reload &>/dev/null || :

%preun
if (( $1 == 0 )); then
    /sbin/service mhvtl shutdown &>/dev/null || :
    /bin/systemctl stop mhvtl &>/dev/null || :
    /sbin/chkconfig --del mhvtl &>/dev/null || :
fi
