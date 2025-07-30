# jyablonski Common Modules
![Tests](https://github.com/jyablonski/jyablonski_common_modules/actions/workflows/ci_cd.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/jyablonski/jyablonski_common_modules/badge.svg?branch=master)](https://coveralls.io/github/jyablonski/jyablonski_common_modules?branch=master) ![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

Version: 0.0.10

Utility Repo w/ functions and tools for data engineering, cloud infrastructure, and development workflows. Includes helpers for:

- PostgreSQL Connections + Upsert Functions
- General Python Functions
- Standard Logging & optional Opensearch Logging Functions
- AWS Helper Functions

## Testing
To run tests, run `make test`

## Install

- `poetry add jyablonski_common_modules`
- `poetry add jyablonski_common_modules --extras es-logging`
- `poetry add jyablonski_common_modules --extras all`
