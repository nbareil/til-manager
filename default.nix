# nixos-unstable on 2022-12-16 - https://status.nixos.org/
with (import (fetchTarball https://github.com/nixos/nixpkgs/archive/0f5996b524c91677891a432cc99c7567c7c402b1.tar.gz) {});


let
  customPython = pkgs.python3.buildEnv.override {
    extraLibs = with pkgs.python3Packages; [
      awesome-slugify
      jinja2
      click
      colorama
      humanize
      build
    ];
  };
in
pkgs.mkShell {
  buildInputs = [
       customPython
        pkgs.black
        pkgs.python3Packages.isort
        pkgs.pre-commit
  ];
}
