Name:		pytorch
Summary:	PyTorch
Version:	1.3.1
Release:	0
License:	BSD-3-Clause and Apache-2.0
Provides:	caffe2 = %{version}-%{release}

Source0:	%{name}-%{version}.tar.gz
Source1001:	pytorch.manifest

Source10001:	pybind11.tar.gz
Source10002:	cub.tar.gz
Source10003:	eigen.tar.gz
Source10004:	googletest.tar.gz
Source10005:	benchmark.tar.gz
Source10006:	protobuf.tar.gz
Source10007:	ios-cmake.tar.gz
Source10008:	NNPACK.tar.gz
Source10009:	gloo.tar.gz
Source10010:	pthreadpool.tar.gz
Source10011:	FXdiv.tar.gz
Source10012:	FP16.tar.gz
Source10013:	psimd.tar.gz
Source10014:	zstd.tar.gz
Source10015:	cpuinfo.tar.gz
Source10016:	python-enum.tar.gz
Source10017:	python-peachpy.tar.gz
Source10018:	python-six.tar.gz
Source10019:	onnx.tar.gz
Source10020:	onnx-tensorrt.tar.gz
Source10021:	sleef.tar.gz
Source10022:	ideep.tar.gz
Source10023:	nccl.tar.gz
Source10024:	gemmlowp.tar.gz
Source10025:	QNNPACK.tar.gz
Source10026:	neon2sse.tar.gz
Source10027:	fbgemm.tar.gz
Source10028:	foxi.tar.gz


BuildRequires:	cmake
BuildRequires:	openblas-devel
BuildRequires:	python3
BuildRequires:	python3-PyYAML
BuildRequires:	protobuf-devel
BuildRequires:	python-PyYAML
BuildRequires:	libyaml-devel

%description
Testing

%prep
%setup -q
cp %{SOURCE1001} .

mkdir -p third_party
tar -xf %SOURCE10001 -C third_party/
tar -xf %SOURCE10002 -C third_party/
tar -xf %SOURCE10003 -C third_party/
tar -xf %SOURCE10004 -C third_party/
tar -xf %SOURCE10005 -C third_party/
tar -xf %SOURCE10006 -C third_party/
tar -xf %SOURCE10007 -C third_party/
tar -xf %SOURCE10008 -C third_party/
tar -xf %SOURCE10009 -C third_party/
tar -xf %SOURCE10010 -C third_party/
tar -xf %SOURCE10011 -C third_party/
tar -xf %SOURCE10012 -C third_party/
tar -xf %SOURCE10013 -C third_party/
tar -xf %SOURCE10014 -C third_party/
tar -xf %SOURCE10015 -C third_party/
tar -xf %SOURCE10016 -C third_party/
tar -xf %SOURCE10017 -C third_party/
tar -xf %SOURCE10018 -C third_party/
tar -xf %SOURCE10019 -C third_party/
tar -xf %SOURCE10020 -C third_party/
tar -xf %SOURCE10021 -C third_party/
tar -xf %SOURCE10022 -C third_party/
tar -xf %SOURCE10023 -C third_party/
tar -xf %SOURCE10024 -C third_party/
tar -xf %SOURCE10025 -C third_party/
tar -xf %SOURCE10026 -C third_party/
tar -xf %SOURCE10027 -C third_party/
tar -xf %SOURCE10028 -C third_party/


%build

export USE_CUDA=0
export NO_CUDA=1
export USE_FBGEMM=0
export PYTHON_EXECUTABLE=/usr/bin/python3

mkdir -p build
pushd build
alias python=python3
%cmake .. -DATEN_NO_TEST=ON -DBUILD_BINARY=ON -DBUILD_CUSTOM_PROTOBUF=OFF -DBUILD_PYTHON=OFF -DUSE_CUDA=OFF -DUSE_MPI=OFF -DUSE_NCCL=OFF -DUSE_METAL=OFF -DUSE_NUMA=OFF -DPYTHON_EXECUTABLE=/usr/bin/python3
make -j4
popd

%install
pushd build
%make_install
popd

## CMAKE script of caffe2 does not use the standard path prefixes
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}/usr/lib/*.so %{buildroot}%{_libdir}

## .pc files needs some updates
sed -i 's|^libdir=.*/lib$|libdir=%{_libdir}|' caffe2.pc
sed -i 's|^libdir=.*/lib$|libdir=%{_libdir}|' pytorch.pc

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m0644 -p caffe2.pc %{buildroot}%{_libdir}/pkgconfig/
install -m0644 -p pytorch.pc %{buildroot}%{_libdir}/pkgconfig/

## CMAKE script of pytorch installs headers incorrectly
pushd %{buildroot}
mv torch %{buildroot}%{_includedir}
popd

%post -p %{_sbindir}/ldconfig
%postun -p %{_sbindir}/ldconfig

%files
%license LICENSE
%manifest pytorch.manifest
%{_libdir}/*.so
%{_prefix}/share/ATen/Declarations.yaml

%package tools
Summary:	Caffe2/PyTorch Tools
Provides:	caffe2-tools  = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description tools
Caffe2/PyTorch tools

%files tools
%license LICENSE
%manifest pytorch.manifest
%{_bindir}/*

%package devel
Summary:	Caffe2/PyTorch Development Package
Requires:	%{name} = %{version}-%{release}
Provides:	caffe2-devel = %{version}-%{release}

%description devel
Caffe2/PyTorch development files

%files devel
%{_includedir}/*
%{_prefix}/share/cmake/*
%{_libdir}/pkgconfig/*.pc
