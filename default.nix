with import <nixpkgs> {};
let
    name = "Flask-env";
    pythonEnv = python38.withPackages (ps: [
        # ps.numpy
        # ps.toolz
        ps.pytest_6
        ps.unittest2
        ps.autopep8
        ps.flake8
        ps.django
        ps.psycopg2
        ps.faker
        ps.bpython
  ]);
in mkShell {
    buildInputs = [
        pythonEnv

        black
        mypy

        # libffi
        # openssl
  ];
}