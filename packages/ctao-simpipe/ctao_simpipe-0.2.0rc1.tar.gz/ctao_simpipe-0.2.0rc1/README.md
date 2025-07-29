# DPPS SimPipe: Integration and Release

The **CTAO DPPS Simulation Production Pipeline (SimPipe)** provides the software, workflows, and data models for generating accurate Monte Carlo simulations of the CTAO observatory.

This packages defines the central `ctao-simpipe` packages, integrating the following components:

- [simtools](https://github.com/gammasim/simtools) - toolkit for model parameter management, production configuration, setting, validation workflows
- [CORSIKA](https://www.iap.kit.edu/corsika/) air shower simulations
- [sim_telarray](https://gitlab.cta-observatory.org/Konrad.Bernloehr/sim_telarray) telescope simulations
- simulation model database - mongoDB database for simulation model parameters and production model definitions

## Deployment

simtools, CORSIKA, and sim_telarray are planned to be deployed on the WMS nodes (CVMFS) for simulation productions using docker images:

- one image per simtools/CORSIKA/sim_telarray version (plus build option variations including CPU vector optimization)
  - example for a [docker file](https://github.com/gammasim/simtools/blob/main/docker/Dockerfile-prod-opt) and [building workflow](https://github.com/gammasim/simtools/blob/main/.github/workflows/build-docker-corsika-simtelarray-image.yml) (using GitHub actions at this point)
- simulation model database is versioned (due to ongoing structure changing) and should be configured accordingly

## Software Installation

- simtools is installed using pip / conda
- CORSIKA is installed using a tar-file (currently downloaded from a cloud storage)
- sim_telarray is installed using a tar-file (currently downloaded from a cloud storage); planned to be installed from gitlab
- simulation model databases - no installed required; configuration of secrets for access

Download of corsika / sim_telarray is facilitated by a private upload to the DESY Sync&Share.
Ask the maintainers to provide the token to you and define it in a `.env` file in this repository:

```console
SOFTWARE_DOWNLOAD_SECRET=<the token received from the maintainers>
```

Then run `make build-dev-docker` to build the simpipe container locally.

## SimPipe Maintainer Documentation

The following section is preliminary and the setup is still in development (especially a simplification of the updating process).

### Updating submodules `dpps-aiv-toolkit` and `simtools`

The `dpps-aiv-toolkit` and `simtools` are submodules of the `dpps-simpipe` repository. To update them, follow these steps (identical for both):

```bash
cd dpps-aiv-toolkit
git checkout <branch-or-commit>
cd ..
git add dpps-aiv-toolkit
git commit -m "Update dpps-aiv-toolkit submodule to latest version"
git push
```

### Updating SimPipe components

1. `simtools`:
   - update the submodule in `simtools` to the latest version (see above)
   - update gammasimtools version in `pyproject.toml`
   - update gammasimtools version in `chart/templates/bootstrapSimulationModel.yaml`
   - update gammasimtools version in `Dockerfile`
2. Production and model parameters (SimulationModels):
   - update `SimulationModels` version in `./chart/values.yaml`
3. `CORSIKA` and `sim_telarray`:
   - update versions in `.gitlab-ci.yml` (this is propagated into the docker file)
4. For a new DPPS release:
   - update DPPS release version in aiv-config.yml
