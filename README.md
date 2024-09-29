# "FB2 zips search"

TL;DR

- modify volumes configuration in `docker-compose.yaml` to point to folder with FB2 zip files
- run `docker compose up -d`
- open `http://localhost:8000` in browser

> [!WARNING]
>
> - The project was created during one night security guard shift.
> - The code quality is extremely low the structure is horrible!
> - Pull requests are very welcome.

## Structure

```bash
# Code
├── Dockerfile
├── docker-compose.yaml
├── api.py                         - FastAPI server
└── static                         - frontend part of the project
    ├── bootstrap-icons.min.css
    ├── bootstrap.bundle.min.js
    ├── bootstrap.min.css
    ├── fonts
    │   └── bootstrap-icons.woff2
    ├── index.html
    └── mithril.min.js

# Data and tools
├── index.json.zip                 - filtered and zipped index file (removed
│                                    books about love_, sex, erotic, popadancy,
│                                    fantasy, litrpg)
├── books                          - arhives with FB2 books (ignored by git)
│   ├── d.fb2-009373-367300.zip
│   └── ...
├── parse.py                       - parser for unzipped_inpx folder
└── unzipped_inpx                  - unzipped .inpx file (ignored by git)
    ├── collection.info
    ├── d.fb2-009373-367300.inp
    ├── ...
    ├── fb2-168103-172702.inp
    └── version.info
```

## Development

Useful commands

- `pip install pandas numpy fastapi[standard]`
- `fastapi dev api.py` for local development
- `docker compose up --force-recreate --build web` to rebuild and rerun the container

## References

- [FastAPI](https://fastapi.tiangolo.com/)
- [Mithril](https://mithril.js.org/)
- [Go .inpx parser](https://github.com/dennwc/inpx/blob/master/inpx.go)
