from flask import Flask, render_template, redirect
import datetime
import json

CONFIG_PATH = "config.json"

"""
A menu item with a link. Can't contain sub-items.
"""
class MenuItem:
    def __init__(self, shortName: str, longName: str, href: str="#"):
        self.shortName = shortName
        self.longName = longName
        self.href = href
        # TODO: Support current page highlighting
    
    def isGroup(self): return False

"""
A menu item that is not a link, but only contains sub-items.
"""
class MenuItemGroup(MenuItem):
    def __init__(self, shortName: str, longName: str, subItems: tuple[MenuItem]):
        super().__init__(shortName=shortName, longName=longName, href="")
        for item in subItems: assert(type(item) == MenuItem)
        self.subItems = subItems

    def isGroup(self): return True

print("Loading config from "+CONFIG_PATH)
with open(CONFIG_PATH) as configFile:
    config = json.load(configFile)

"""
Load menu from config file.
"""
menuItems = []
for item in config["menu"]:
    assert(type(item) == dict)
    if "subItems" in item: # If this is a menu item group
        assert("href" not in item)
        group = MenuItemGroup(shortName=item["shortName"], longName=item["longName"], subItems=[]) #type: ignore
        for subitem in item["subItems"]:
            group.subItems.append(MenuItem(**subitem)) #type: ignore
        menuItems.append(group)
    else: # If this is a simple menu item
        menuItems.append(MenuItem(**item))

globalVals = {
    "mainSiteTitle": config["mainSiteTitle"],
    "copyrightYear": datetime.datetime.now().year,
    "copyrightHolder": config["copyrightHolder"],
    "menuItems": menuItems,
}

app = Flask(__name__)

@app.route("/", defaults={"path": "index"})
@app.route("/<path:path>")
def renderPage(path):
    # Remove html extension
    if str(path).endswith(".html"):
        return redirect("/"+str(path).replace(".html", ""))

    # The 404 page has a special template
    if path == "404":
        return render_template("404.html", **globalVals), 404

    try:
        confPath = "pages/"+path+".json"
        confFile = open(confPath, "r")
        pageConf = json.load(confFile)
        confFile.close()
        return render_template("template.html", **globalVals, **pageConf)
    except FileNotFoundError:
        return redirect("/404")