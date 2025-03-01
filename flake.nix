{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = {self, nixpkgs, ...}:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      django-smoketest = pkgs.python312Packages.buildPythonPackage {
        pname = "django-smoketest";
        version = "1.2.1";
        format = "pyproject";
        src = pkgs.fetchPypi {
          pname = "django-smoketest";
          version = "1.2.1";
          sha256 = "sha256-cI91yYVa9zez/lQDy4MQfPPQ01Ebt/gWy4dTzmPwqHs=";
        };
        doCheck = false;
        propagatedBuildInputs = [ pkgs.python312Packages.hatchling pkgs.python312Packages.hatch-vcs pkgs.python312Packages.django ];
      };
      django-waffle = pkgs.python312Packages.buildPythonPackage {
        pname = "django-waffle";
        version = "3.4";
        format = "pyproject";
        src = pkgs.fetchPypi {
          pname = "django-waffle";
          version = "4.1.0";
          sha256 = "sha256-5J19Rh2J872OU/IO/jkxCsyo8nXJiISV5o4ZU0W/GLE=";
        };
        doCheck = false;
        propagatedBuildInputs = [ pkgs.python312Packages.hatchling pkgs.python312Packages.hatch-vcs pkgs.python312Packages.django ];
      };
      sentry-sdk = pkgs.python312Packages.buildPythonPackage {
        pname = "sentry-sdk";
        version = "2.8.0";
        format = "pyproject";
        src = pkgs.fetchPypi {
          pname = "sentry_sdk";
          version = "2.8.0";
          sha256 = "sha256-qkMU+HfZzZrdWgyboY4/J/mffeg1zja9FQ5IpBx8ZG8=";
        };
        doCheck = false;
        propagatedBuildInputs = [ pkgs.python312Packages.hatchling pkgs.python312Packages.hatch-vcs pkgs.python312Packages.urllib3 pkgs.python312Packages.certifi ];
      };
      whitenoise = pkgs.python312Packages.buildPythonPackage {
        pname = "whitenoise";
        version = "6.6.0";
        format = "pyproject";
        src = pkgs.fetchPypi {
          pname = "whitenoise";
          version = "6.6.0";
          sha256 = "sha256-iZj3NwlzRH+sHo726N7SxSCaex9nwQEoZtvNCWgcMlE=";
        };
        doCheck = false;
        propagatedBuildInputs = [ pkgs.python312Packages.hatchling pkgs.python312Packages.hatch-vcs pkgs.python312Packages.django ];
      };
      tox-uv = pkgs.python312Packages.buildPythonPackage {
        pname = "tox-uv";
        version = "1.25.0";
        format = "pyproject";
        src = pkgs.fetchPypi {
          pname = "tox_uv";
          version = "1.11.0";
          sha256 = "05824mc7fqls7in2dq02k5qaiqbk0rabg3m945x5dbmlyqx1kih0";
        };
        doCheck = false;
        propagatedBuildInputs = [ pkgs.python312Packages.hatchling pkgs.python312Packages.hatch-vcs pkgs.python312Packages.uv pkgs.python312Packages.tox ];
      };
    in
    {
      devShells.x86_64-linux.default =
        pkgs.mkShell
          {
            buildInputs = [
              pkgs.flyctl
              pkgs.ruff
              pkgs.uv
              (pkgs.python312.withPackages (p: [
                p.django
                p.django-debug-toolbar
                django-smoketest
                p.django-stubs
                django-waffle
                p.factory-boy
                p.gunicorn
                p.mypy
                p.mypy-extensions
                p.pip-tools
                p.psycopg2
                sentry-sdk
                p.tomli
                p.tox
                tox-uv
                p.types-requests
                whitenoise
              ]))
            ];
          };
    };
}
