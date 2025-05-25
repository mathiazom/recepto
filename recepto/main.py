import os
import re
from pathlib import Path

import requests
from fastapi import FastAPI, Response
from recipe_scrapers import scrape_html, __version__ as scraper_version
from starlette.responses import FileResponse

HEADERS = {
    "User-Agent": f"Mozilla/5.0 (compatible; Windows NT 10.0; Win64; x64; rv:{scraper_version}) recipe-scrapers/{scraper_version}"
}

app = FastAPI(redoc_url="/", docs_url=None)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(Path(os.path.dirname(os.path.realpath(__file__))) / "favicon.ico")


@app.get("/{recipe_url:path}")
def process_recipe(recipe_url):
    print(f"Grabbing recipe from {recipe_url}")
    try:
        html = requests.get(url=recipe_url, headers=HEADERS).text
    except Exception as e:
        raise Exception(f"Failed to retrieve HTML content from {recipe_url}.") from e
    recipe = scrape_html(html, recipe_url, supported_only=False)
    print(f"Identified recipe for '{recipe.title()}' from {recipe.host()}")
    return Response(content=recipe_as_md(recipe, recipe_url), media_type="text/plain")


def recipe_as_md(recipe, url):
    md = f">{url}  \n\n"
    md += f"![{recipe.title()}]({recipe.image()})  \n"
    md += "## Ingredienser\n\n"
    for i in recipe.ingredients():
        p = re.compile("--- (.*?) ---")
        m = p.match(i)
        if m is not None:
            md += f"\n***{m.group(1)}***  \n"
        else:
            md += f"{i}  \n"
    md += "\n## Fremgangsmåte\n\n"
    for s in recipe.instructions().split("\n"):
        md += f"1. {s}\n"
    return md
