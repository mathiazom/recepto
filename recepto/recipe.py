import re
from urllib.request import Request, urlopen

from recipe_scrapers import scrape_html, __version__ as scraper_version

HEADERS = {
    "User-Agent": f"Mozilla/5.0 (compatible; Windows NT 10.0; Win64; x64; rv:{scraper_version}) recipe-scrapers/{scraper_version}"
}
FETCH_TIMEOUT_SECONDS = 10


def process_recipe(recipe_url):
    print(f"Grabbing recipe from {recipe_url}")
    if not recipe_url.startswith(("http://", "https://")):
        raise ValueError(f"Not an http(s) URL: {recipe_url}")
    try:
        with urlopen(Request(recipe_url, headers=HEADERS), timeout=FETCH_TIMEOUT_SECONDS) as response:
            html = response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    except Exception as e:
        raise Exception(f"Failed to retrieve HTML content from {recipe_url}.") from e
    recipe = scrape_html(html, recipe_url, supported_only=False)
    print(f"Identified recipe for '{recipe.title()}' from {recipe.host()}")
    return recipe_as_md(recipe, recipe_url)


def recipe_as_md(recipe, url):
    md = f"# {recipe.title()}\n\n"
    md += f">{url}  \n\n"
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
