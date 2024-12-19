# **SPORT HUB STORE**

### [SPORT HUB](https://teamchallenge-sport-store-frontend.vercel.app) is an e-commerce platform for hassle-free shopping.

### In this project implemented:

- Product catalogue: structure of presentation, search, sorting, product filters.


- Shopping cart and checkout: adding, updating, deleting products to the shopping cart, and checkout.


- User's personal account: the ability to register, confirm the user's email, authorise and manage personal data, view
  the order history for a certain period.


- Admin panel: an interface for managing the store, adding products, categories, users, etc.


- Integration with the NOVA POST API: the possibility of delivery by courier, to a branch, and parcel locker.


- Integration with LiqPay: the ability to pay by card, get invoice.

![Logo](docs/logo.png)

## Stack:

[![Stack](https://skillicons.dev/icons?i=python,docker,postgres,django,gcp&theme=dark&perline=10)](https://skillicons.dev)

## Installation:

### Clone this repository using GitHub Desktop:

![Clone](docs/gitinstal.png)

## Preparations:

### .env:

Please, make sure that you have a .env in the root folder. Feel free to specify values of environmental variables as you
wish, but make sure that your .env file structured like .env.example.

## Start develop with Docker:

Firstly, you need to have Docker installed in your system. If you haven't installed Docker yet,
visit https://docs.docker.com/get-docker/

## Commands:

- To list available commands for make:
  ```shell
  $ make

  Please use `make <target>' where <target> is one of
  build_and_run             Run and build application
  drop_all_containers       Drop all containers
  help                      Display help message
  migrate                   Make migrate
  open_log                  Open api log
  open_shell                Open shell to the app container
  run_app                   Run application
  run_migrate               Run migrate
  super_user                Make super user
  ```

- Run and build application:

      make build_and_run

- Run application:

      make build_and_run

## DB migration:

- Make migrations of the DB:

      make migrate

- Migrate the DB:

      make run_migrate

## Poetry:

In this project used [Poetry](https://python-poetry.org/) environment

- Load all needed packages

      poetry install

- Add new package

      poetry add <package_name>

## Swagger:

- Show OpenApi schema

      http://host:port/swagger/

## Deployment:

We chose [Google Cloud Platform](https://cloud.google.com) to deploy our project

## Contributors:

- [Vita Yushchyk](https://github.com/vitayushchyk)
- [Mykola Chaiun](https://github.com/KolyaChaun)
