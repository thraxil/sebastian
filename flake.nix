{
  description = "Sebastian SRS app";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python312;

      pythonWithOverrides = python.override {
        packageOverrides = self: super: {
          asgiref = super.asgiref.overridePythonAttrs (old: rec {
            version = "3.11.0";
            src = pkgs.fetchurl {
              url = "https://files.pythonhosted.org/packages/76/b9/4db2509eabd14b4a8c71d1b24c8d5734c52b8560a7b1e1a8b56c8d25568b/asgiref-3.11.0.tar.gz";
              sha256 = "13acff32519542a1736223fb79a715acdebe24286d98e8b164a73085f40da2c4";
            };
            doCheck = false;
          });
          sqlparse = super.sqlparse.overridePythonAttrs (old: rec {
            version = "0.5.4";
            src = pkgs.fetchurl {
              url = "https://files.pythonhosted.org/packages/18/67/701f86b28d63b2086de47c942eccf8ca2208b3be69715a1119a4e384415a/sqlparse-0.5.4.tar.gz";
              sha256 = "4396a7d3cf1cd679c1be976cf3dc6e0a51d0111e87787e7a8d780e7d5a998f9e";
            };
            doCheck = false;
          });
          django = super.django.overridePythonAttrs (old: rec {
            pname = "Django";
            version = "6.0.3";
            src = pkgs.fetchurl {
              url = "https://files.pythonhosted.org/packages/80/e1/894115c6bd70e2c8b66b0c40a3c367d83a5a48c034a4d904d31b62f7c53a/django-6.0.3.tar.gz";
              sha256 = "90be765ee756af8a6cbd6693e56452404b5ad15294f4d5e40c0a55a0f4870fe1";
            };
            patches = [ ];
            doCheck = false;
          });
          gunicorn = super.gunicorn.overridePythonAttrs (old: rec {
            version = "25.3.0";
            src = pkgs.fetchurl {
              url = "https://files.pythonhosted.org/packages/c4/f4/e78fa054248fab913e2eab0332c6c2cb07421fca1ce56d8fe43b6aef57a4/gunicorn-25.3.0.tar.gz";
              sha256 = "f74e1b2f9f76f6cd1ca01198968bd2dd65830edc24b6e8e4d78de8320e2fe889";
            };
            doCheck = false;
          });
          django-debug-toolbar = self.buildPythonPackage rec {
            pname = "django-debug-toolbar";
            version = "6.3.0";
            format = "pyproject";
            src = pkgs.fetchurl {
              url = "https://files.pythonhosted.org/packages/d8/ea/b62673424dd72d2dbf5adf4145281a421d5792f47380d9bc8e3b11e1a769/django_debug_toolbar-6.3.0.tar.gz";
              sha256 = "f830a86fe02e17f625a22cfbed24a5bd1500762e201ec959c50efb0f9327282b";
            };
            postPatch = ''
              sed -i "/Framework :: Django :: 6.0/d" pyproject.toml
            '';
            nativeBuildInputs = [ self.hatchling self.setuptools self.wheel ];
            propagatedBuildInputs = [ self.django self.sqlparse ];
            doCheck = false;
          };
          django-smoketest = self.buildPythonPackage rec {
            pname = "django-smoketest";
            version = "1.2.1";
            format = "setuptools";
            src = pkgs.fetchurl {
              url = "https://files.pythonhosted.org/packages/28/44/bc26e5932b1de0f2563495e3e8a31da4a5485780bd8db005b7936fbbe854/django-smoketest-1.2.1.tar.gz";
              sha256 = "708f75c9855af737b3fe5403cb83107cf3d0d3511bb7f816cb8753ce63f0a87b";
            };
            propagatedBuildInputs = [ self.django ];
            doCheck = false;
          };
          psycopg = super.psycopg.overridePythonAttrs (old: {
            doCheck = false;
            pythonImportsCheck = [ "psycopg" "psycopg_c" ];
          });
          psycopg-pool = super.psycopg-pool.overridePythonAttrs (old: {
            pythonImportsCheck = [ ];
          });
        };
      };

      pythonEnv = pythonWithOverrides.withPackages (ps: [
        ps.django
        ps.django-smoketest
        ps.django-debug-toolbar
        ps.psycopg
        ps.psycopg-pool
        ps.gunicorn
        ps.sentry-sdk
        ps.whitenoise
        ps.factory-boy
      ]);

      devPythonEnv = pythonWithOverrides.withPackages (ps: [
        ps.django
        ps.django-smoketest
        ps.django-debug-toolbar
        ps.psycopg
        ps.psycopg-pool
        ps.gunicorn
        ps.sentry-sdk
        ps.whitenoise
        ps.factory-boy
        # Dev dependencies
        ps.mypy
        ps.ruff
        ps.hypothesis
        ps.django-stubs
        ps.typing-extensions
      ]);

      # Static files derivation
      staticfiles = pkgs.stdenv.mkDerivation {
        name = "sebastian-staticfiles";
        src = pkgs.lib.cleanSource ./.;
        buildInputs = [ pythonEnv ];
        buildPhase = ''
          export SECRET_KEY=dummy
          export DJANGO_SETTINGS_MODULE=sebastian.settings_docker
          python manage.py collectstatic --noinput
        '';
        installPhase = ''
          mkdir -p $out
          cp -r staticfiles/* $out/
        '';
      };

      # App directory with source and static files
      appDir = pkgs.runCommand "sebastian-app" {} ''
        mkdir -p $out/app
        cp -r ${pkgs.lib.cleanSource ./.}/* $out/app/
        chmod -R +w $out/app
        rm -rf $out/app/staticfiles
        cp -r ${staticfiles} $out/app/staticfiles
      '';

      container = pkgs.dockerTools.buildLayeredImage {
        name = "sebastian";
        tag = "latest";
        contents = [
          pythonEnv
          pkgs.bash
          pkgs.postgresql
          pkgs.coreutils
          appDir
        ];
        config = {
          Cmd = [ "/app/entry-point.sh" "run" ];
          WorkingDir = "/app";
          ExposedPorts = {
            "8000/tcp" = {};
          };
          Env = [
            "PYTHONUNBUFFERED=1"
            "DJANGO_SETTINGS_MODULE=sebastian.settings_docker"
            "APP=sebastian"
            "PATH=${pythonEnv}/bin:${pkgs.bash}/bin:${pkgs.postgresql}/bin:${pkgs.coreutils}/bin"
          ];
        };
      };
    in
    {
      packages.${system} = {
        default = container;
        container = container;
      };

      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pkgs.flyctl
          pkgs.nodejs
          pkgs.postgresql
          pkgs.uv
          devPythonEnv
        ];
      };
    };
}
