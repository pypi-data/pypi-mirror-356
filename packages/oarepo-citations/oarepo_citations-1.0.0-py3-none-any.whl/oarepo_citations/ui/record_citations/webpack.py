from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": {
            "entry": {
                "record_citations": "./js/record_citations/custom-components.js",
                "record_citations_dropdown": "./js/record_citations/dropdown/index.js",
                "record_citations_modal": "./js/record_citations/modal/index.js",
            },
            "dependencies": {},
            "devDependencies": {},
            "aliases": {"@js/record_citations": "./js/record_citations"},
        }
    },
)
