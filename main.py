import re
from recipe_scrapers import scrape_me

from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/{recipe_url:path}")
def process_recipe(recipe_url):
    print(f"Grabbing recipe from {recipe_url}")
    recipe = scrape_me(recipe_url)
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
