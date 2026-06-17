Name:           fastflowlm
Version:        %{flm_version}
Release:        1%{?dist}
Summary:        NPU-accelerated LLM runtime for AMD Ryzen AI

License:        MIT
URL:            https://github.com/FastFlowLM/FastFlowLM
Source0:        %{name}-%{version}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  cargo
BuildRequires:  cmake >= 3.22
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libavcodec-free-devel
BuildRequires:  libavformat-free-devel
BuildRequires:  libavutil-free-devel
BuildRequires:  libcurl-devel
BuildRequires:  libdrm-devel
BuildRequires:  libswresample-free-devel
BuildRequires:  libswscale-free-devel
BuildRequires:  boost-devel
BuildRequires:  fftw-devel
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  readline-devel
BuildRequires:  rust
BuildRequires:  libuuid-devel
# XRT development headers — install from the AMD/Lemonade repository
BuildRequires:  xrt-devel

Requires:       boost-program-options
Requires:       fftw
Requires:       libavcodec-free
Requires:       libavformat-free
Requires:       libcurl
Requires:       libswresample-free
Requires:       libswscale-free
Requires:       readline
# XRT NPU runtime — install from the AMD/Lemonade repository
Requires:       xrt-npu

%description
FastFlowLM (FLM) runs large language models on AMD Ryzen AI NPUs
(XDNA2 family: Strix, Strix Halo, Kraken, Gorgon Point) without a
GPU. It provides a CLI and an OpenAI-compatible REST server, and
supports LLMs, VLMs, audio and embedding models.

%prep
%autosetup -n %{name}-%{version}
git submodule update --init --recursive

%build
cd src
cmake --preset linux-default \
    -DCMAKE_INSTALL_PREFIX=/opt/fastflowlm \
    -DFLM_VERSION=%{version} \
    -DNPU_VERSION=32.0.203.304
cmake --build build -j%{_smp_build_ncpus}

%install
cd src
DESTDIR=%{buildroot} cmake --install build --prefix=/opt/fastflowlm

# Remove headers (not needed in the binary package)
rm -rf %{buildroot}/opt/fastflowlm/include

# Symlink into PATH
install -d %{buildroot}%{_bindir}
ln -sf /opt/fastflowlm/bin/flm %{buildroot}%{_bindir}/flm

%files
%license LICENSE_RUNTIME.txt
/opt/fastflowlm/
%{_bindir}/flm

%changelog
* Tue Jun 17 2026 FastFlowLM Team <noreply@fastflowlm.com> - 0.9.43-1
- Initial RPM packaging
