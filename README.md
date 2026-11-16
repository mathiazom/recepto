# 🧑‍🍳 recepto

[![recepto](https://img.shields.io/badge/ghcr.io-mathiazom%2Frecepto-blue?logo=docker)](https://github.com/users/mathiazom/packages/container/package/recepto)

Convert web recipes to Markdown

> Depends on [hhursev/recipe-scrapers](https://github.com/hhursev/recipe-scrapers). If you stumble upon an unsupported website, head over there and file an issue or submit a fix 💪

## Run

```sh
uv run recepto/main.py
```
or, with Docker:
```sh
docker compose -f docker/docker-compose.dev.yml up --build
```

Then open `http://localhost:8000/<recipe url>`, e.g. http://localhost:8000/https://www.bbcgoodfood.com/recipes/easy-pancakes
