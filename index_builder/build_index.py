from jinja2 import Environment, PackageLoader, select_autoescape
import tomllib
import json

KPM_MANIFEST_VERSION = 1

env = Environment(
    loader=PackageLoader("build_index"),
    autoescape=select_autoescape()
)

template = env.get_template("index.html")

with open("./index_builder/config.toml", 'rb') as file:
    config = tomllib.load(file)

with open("./manifest.json") as file:
    manifest = json.loads(file.read())

if (manifest["manifest_version"] != KPM_MANIFEST_VERSION):
    print(f"Expected manifest version {KPM_MANIFEST_VERSION}, got {manifest['manifest_version']}")
    exit(1)

assert(not ' ' in manifest["id"])
assert(manifest["id"].isalnum())
for package_id in manifest["packages"]:
    for letter in package_id:
        assert(letter.islower() and (letter.isalnum() or letter in ['-', '_']))

with open("./index.html", 'w') as file:
    file.write(template.render({
        "manifest": manifest,
        "show_url": config["show_url"],
        "url": config["url"],
        "package_ids": sorted(list(manifest["packages"].keys())),
        "is_empty": len(manifest["packages"]) == 0
    }))