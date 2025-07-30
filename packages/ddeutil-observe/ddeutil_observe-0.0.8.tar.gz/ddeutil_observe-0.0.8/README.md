# Observe Application

[![test](https://github.com/ddeutils/ddeutil-observe/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/ddeutils/ddeutil-observe/actions/workflows/tests.yml)
[![pypi version](https://img.shields.io/pypi/v/ddeutil-observe)](https://pypi.org/project/ddeutil-observe/)
[![python support version](https://img.shields.io/pypi/pyversions/ddeutil-observe)](https://pypi.org/project/ddeutil-observe/)
[![size](https://img.shields.io/github/languages/code-size/ddeutils/ddeutil-observe)](https://github.com/ddeutils/ddeutil-observe)
[![gh license](https://img.shields.io/github/license/ddeutils/ddeutil-observe)](https://github.com/ddeutils/ddeutil-observe/blob/main/LICENSE)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The **Lightweight Observe Application** project was created for easy to
make an observe application that getting logs, audits, or trigger status
from any data framework storage and endpoint APIs.
This project focuses on the `ddeutil-workflow` tool first :dart:.

> [!WARNING]
> This project is the best fit integration with `ddeutil-workflow` package.
> The first propose is monitor and observe from worker nodes that deploy the
> workflow application on a target self-hosted.

> [!NOTE]
> I will use this project to be my Fundamental Frontend learning.

## 📦 Installation

```shell
pip install -U ddeutil-observe
```

> :egg: **Docker Images** supported:
>
> | Docker Image               | Python Version | Support |
> |----------------------------|----------------|:-------:|
> | ddeutil-observe:latest     | `3.9`          |   :x:   |
> | ddeutil-observe:python3.10 | `3.10`         |   :x:   |
> | ddeutil-observe:python3.11 | `3.11`         |   :x:   |
> | ddeutil-observe:python3.12 | `3.12`         |   :x:   |
> | ddeutil-observe:python3.12 | `3.13`         |   :x:   |

> [!NOTE]
> If you want to increase this application performance, you can install the
> performance option, `pip install ddeutil-observe[perf]` (It does not edit
> code, it's just routing other faster packages).

## :beers: Getting Started

For the first phase, I will use the SQLite be a backend database that keep
authentication and workflows data.

### Login Page

![Login Page](./docs/img/login-page.png?raw=true)

### Main Page

![Workflow Page](./docs/img/workflow-page.png?raw=true)

![Workflow Detail Page](./docs/img/workflow-detail-page.png?raw=true)

![Workflow Trace Page](./docs/img/workflow-trace-page.png?raw=true)

## :cookie: Configuration

> [!IMPORTANT]
> The config value that you will set on the environment should combine with
> prefix, component, and name which is `OBSERVE_{component}_{name}` (Upper case).

| Environment                      | Component | Default                            | Description                                                                                     |
|:---------------------------------|:---------:|:-----------------------------------|:------------------------------------------------------------------------------------------------|
| **ENVIRONMENT**                  |   Core    | `development`                      | Application environment (development, staging, production). Chrome DevTools only enabled in dev |
| **TIMEZONE**                     |   Core    | `UTC`                              | A timezone that use on all components of this application                                       |
| **SQLALCHEMY_DB_ASYNC_URL**      |   Core    | `sqlite+aiosqlite:///./observe.db` | A database url of the application backend side                                                  |
| **ACCESS_SECRET_KEY**            |   Core    | `secrets.token_urlsafe(32)`        | A secret key that use to hash the access token with jwt package                                 |
| **ACCESS_TOKEN_EXPIRE_MINUTES**  |   Core    | `30`                               | Expire period of the access token in minute unit                                                |
| **REFRESH_SECRET_KEY**           |   Core    | `secrets.token_urlsafe(32)`        | A secret key that use to hash the refresh token with jwt package                                |
| **REFRESH_TOKEN_EXPIRE_MINUTES** |   Core    | `60 * 24 * 8`                      | Expire period of the refresh token in minute unit                                               |
| **ADMIN_USER**                   |    Web    | `observe`                          | An username of superuser                                                                        |
| **ADMIN_PASS**                   |    Web    | `observe`                          | A password of superuser                                                                         |
| **ADMIN_EMAIL**                  |    Web    | `observe@mail.com`                 | An email of superuser                                                                           |
| **DEBUG_MODE**                   |    Log    | `true`                             | Logging mode                                                                                    |
| **SQLALCHEMY_DEBUG_MODE**        |    Log    | `true`                             | Database Logging mode that will logging every execution statement before and after connection   |

## :rocket: Deployment

```shell
(env) $ uvicorn src.ddeutil.observe.app:app \
  --host 127.0.0.1 \
  --port 88 \
  --no-access-log
```

> [!NOTE]
> If this package already deploy, it is able to use
> ```shell
> (env) $ uvicorn ddeutil.workflow.api:app \
>   --host 127.0.0.1 \
>   --port 88 \
>   --workers 4 \
>   --no-access-log
> ```

## :speech_balloon: Contribute

I do not think this project will go around the world because it has specific propose,
and you can create by your coding without this project dependency for long term
solution. So, on this time, you can open [the GitHub issue on this project :raised_hands:](https://github.com/ddeutils/ddeutil-observe/issues)
for fix bug or request new feature if you want it.
