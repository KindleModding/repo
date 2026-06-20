from jinja2 import Environment, PackageLoader, select_autoescape
import tomllib
import json

env = Environment(
    loader=PackageLoader("build_index"),
    autoescape=select_autoescape()
)

template = env.get_template("index.html")

with open("./index_builder/config.toml", 'rb') as file:
    config = tomllib.load(file)

with open("./manifest.json") as file:
    manifest = json.loads(file.read())

with open("./index.html", 'w') as file:
    file.write(template.render({
        "manifest": manifest,
        "show_url": config["show_url"],
        "url": config["url"],
        "package_ids": sorted(list(manifest["packages"].keys())),
        "is_empty": len(manifest["packages"]) == 0
    }))