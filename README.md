# muxtools documentation

```sh
uv sync --frozen
uv run --frozen python scripts/prepare_api.py
uv run --frozen zensical serve
```

For a production build, replace the last command with
`uv run --frozen zensical build --clean --strict`.
Rerun the preparation step after updating dependencies or editing their sources.
It copies the installed packages into the ignored `.api-sources/` directory,
including packages installed in editable mode.

## Module pages

`api-autonav` generates module pages and navigation under `reference/`.
The global mkdocstrings defaults in `zensical.toml` use source order and hide
objects without docstrings. If a module would otherwise have no visible contents,
the module template retries with `show_if_no_docstring = true`, keeping the
configured member filters. Modules with visible documentation keep the default.
Set exceptions with `module_options`:

```toml
[project.plugins.api-autonav.module_options.'^muxtools\.audio\.tools$']
show_if_no_docstring = true
```

Patterns match fully qualified module names. Anchor a pattern with `^` and `$`
to target one module. Other mkdocstrings options, such as `members`,
`inherited_members`, and `show_signature`, can be set in the same table.

To disable the empty-module fallback for a particular module:

```toml
[project.plugins.api-autonav.module_options.'^muxtools\.utils\.language_util$']
extra = { show_undocumented_if_empty = false }
```

For a custom page, exclude its module from `api-autonav`, write a Markdown page
with `:::` directives, and add it to `nav`.
See `docs/muxtools/helpers/bitstream_filters.md` and its matching `exclude`
and navigation entries in `zensical.toml` for a working example.
