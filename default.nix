with import <nixpkgs> {};
let
  my-python-packages = python-packages: [
    python-packages.pip
    python-packages.setuptools
  ];
  my-python = python37.withPackages my-python-packages;
in
  pkgs.mkShell {
    buildInputs = [
      bashInteractive
      my-python
      libffi
      openssl
      libxml2
      postgresql
      libxslt
      sass
      nodejs
    ];
    shellHook = ''
      export PATH=$PATH:"$(pwd)/.build/pip_packages/bin"
      export PIP_PREFIX="$(pwd)/.build/pip_packages"
      export PYTHONPATH="$(pwd)/.build/pip_packages/bin:$PYTHONPATH"
      export PYTHONPATH="$(pwd)/.build/pip_packages/lib/python3.7/site-packages:$PYTHONPATH"
      unset SOURCE_DATE_EPOCH
    '';
  }
