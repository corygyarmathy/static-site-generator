# shell.nix
let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  name = "impureVenv";
  venvDir = "./.venv";
  buildInputs = with pkgs; [
    python3
    (pkgs.python3.withPackages (
      python-pkgs: with python-pkgs; [
        # select Python packages here
        venvShellHook
        debugpy
      ]
    ))
  ];
  postVenvCreation = ''
    pip install -r ${./requirements.txt}
  '';
  shellHook = ''
    venvShellHook
  '';
}
