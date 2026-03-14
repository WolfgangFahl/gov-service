# gov-service
| | |
| :--- | :--- |
| **PyPi** | [![PyPI Status](https://img.shields.io/pypi/v/gov-service.svg)](https://pypi.python.org/pypi/gov-service/) [![License](https://img.shields.io/github/license/WolfgangFahl/gov-service.svg)](https://www.apache.org/licenses/LICENSE-2.0) [![pypi](https://img.shields.io/pypi/pyversions/gov-service)](https://pypi.org/project/gov-service/) [![format](https://img.shields.io/pypi/format/gov-service)](https://pypi.org/project/gov-service/) [![downloads](https://img.shields.io/pypi/dd/gov-service)](https://pypi.org/project/gov-service/) |
| **GitHub** | [![Github Actions Build](https://github.com/WolfgangFahl/gov-service/actions/workflows/build.yml/badge.svg)](https://github.com/WolfgangFahl/gov-service/actions/workflows/build.yml) [![Release](https://img.shields.io/github/v/release/WolfgangFahl/gov-service)](https://github.com/WolfgangFahl/gov-service/releases) [![Contributors](https://img.shields.io/github/contributors/WolfgangFahl/gov-service)](https://github.com/WolfgangFahl/gov-service/graphs/contributors) [![Last Commit](https://img.shields.io/github/last-commit/WolfgangFahl/gov-service)](https://github.com/WolfgangFahl/gov-service/commits/) [![GitHub issues](https://img.shields.io/github/issues/WolfgangFahl/gov-service.svg)](https://github.com/WolfgangFahl/gov-service/issues) [![GitHub closed issues](https://img.shields.io/github/issues-closed/WolfgangFahl/gov-service.svg)](https://github.com/WolfgangFahl/gov-service/issues/?q=is%3Aissue+is%3Aclosed) |
| **Code** | [![style-black](https://img.shields.io/badge/%20style-black-000000.svg)](https://github.com/psf/black) [![imports-isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/) |
| **Docs** | [![API Docs](https://img.shields.io/badge/API-Documentation-blue)](https://WolfgangFahl.github.io/gov-service/) [![formatter-docformatter](https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg)](https://github.com/PyCQA/docformatter) [![style-google](https://img.shields.io/badge/%20style-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings) |

A local GOV (Geschichtliches Ortsverzeichnis) server service, usable as an alternative GOV server via the GOV-Tag `base_url` option.

## Command Line Testing

You can test queries directly from the command line using the `scripts/gov_query` tool:

```bash
# List available queries
scripts/gov_query -li

# Test the NameByGovId query with Schönberg's GOV-Kennung
scripts/gov_query -qn NameByGovId --params gov_id=SCHERGJO54EJ -f json
```

## API Testing

When the service is running (e.g. via `scripts/startup --gov`), you can test the REST API endpoint directly using curl:

```bash
# HTML (default)
curl -s http://localhost:8000/item/wikihtml/SCHERGJO54EJ

# JSON via Accept header
curl -s -H "Accept: application/json" http://localhost:8000/item/show/SCHERGJO54EJ

# YAML via Accept header
curl -s -H "Accept: application/x-yaml" http://localhost:8000/item/show/SCHERGJO54EJ

# JSON via format query parameter (overrides Accept header)
curl -s "http://localhost:8000/item/show/SCHERGJO54EJ?format=json"
```

## API Documentation

The service is built with [FastAPI](https://fastapi.tiangolo.com/), which automatically provides interactive API documentation when the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Docs
[GOV-Service on GOV-Wiki](https://gov-wiki.genealogy.net/index.php/GOV-Service)
