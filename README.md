# "FB2 zips search"

> [!WARNING]
>
> - The project was created during one night shift while working as a security guard.
> - The code quality is extremely low the structure is horrible!
> - Pull requests are very welcome.

TL;DR

- modify volumes configuration in `docker-compose.yaml` to point to folder with FB2 zip files
- run `docker compose up -d`
- open `http://localhost:8000` in browser

## Development

Useful commands

- `pip install pandas numpy fastapi[standard]`
- `fastapi dev api.py` for local development
- `docker compose up --force-recreate --build web` to rebuild and rerun the container
