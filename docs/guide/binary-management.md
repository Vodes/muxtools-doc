# Binary Management

You can now let muxtools handle most of the binaries you need for a project.<br>
That means you don't have to throw everything into PATH or keep a folder of random exes next to every script.

It'll install the versions you ask for and make sure your scripts use those.

!!! note
    Every main command has a TUI interface as well.<br>
    That means everything from `muxtools binaries` to `binaries install`, `binaries remove` will open an interface in your terminal that you can navigate freely.<br>
    The `-h`/`--help` sections for each also have some usage examples that should be pretty clear.

## Setup

First you need a project config. You can put it in your `pyproject.toml` or just use a separate `muxtools.toml`.

```sh
# Pick whichever config file you prefer
muxtools init --pyproject -l
muxtools init --standalone -l
```

`-l` means project-local binaries.<br>
`-g` enables global (user-wide) binaries. This might obviously be preferable if you don't want to have binaries in every project.<br>
muxtools will still pick the exact version (or newest, depending on your constraints) you have defined in your config.

If you just run `muxtools init` in a terminal it'll ask you about both the config file and where you want the binaries.

=== "pyproject.toml"

    ```toml
    [tool.muxtools]
    show_name = "Nice Series"

    [tool.muxtools.binaries]
    prefer = "local"
    packages = [
        "ffmpeg",
        "opus-tools",
    ]
    ```

=== "muxtools.toml"

    ```toml
    [muxtools]
    show_name = "Nice Series"

    [muxtools.binaries]
    prefer = "local"
    packages = [
        "ffmpeg",
        "opus-tools",
    ]
    ```

If you want to pin something, just add the version after it. `"x265==4.2"` for example.<br>
The version list comes from the muxtools binary catalog, so `muxtools binaries add x265` is usually easier than writing it out yourself.

## The usual way

From the project directory you can just do this:

```sh
muxtools binaries add ffmpeg
muxtools binaries add opusenc
muxtools binaries sync
muxtools binaries list
```

`add` installs the package and writes it to your config. Passing `opusenc` is fine even though the actual package is called `opus-tools`.<br>
`sync` is handy after you pull a project somewhere else or after manually changing the package list. It'll install anything the config still needs.

`list` shows all installed versions. The one currently picked by the project gets a `*` next to it.

You can also leave the package name out for `add`, `install` or `remove` and pick from a prompt instead. Useful if you forgot what the package was called or just want to grab a few things at once.

!!! tip
    Some things have shorthands that may be obvious to some.<br>
    The `muxtools` command will also be registered as `mt` for example.<br>
    Same for `binaries` with `bin`<br><br>
    Basically: If you use [uv](<https://docs.astral.sh/uv>) you can do `uv run mt bin` in your project to open the TUI<br>
    Or even `uvx muxtools binaries` to install binaries globally without any project.

## Other places and commands

If you want one install shared between all your projects, use `-g` for the user-global location.

```sh
muxtools binaries install -g "x265==4.2"
muxtools binaries list -g
```

`install` is the same basic thing as `add`, except it doesn't change the project config.<br>
For removing things you can use `muxtools binaries remove x265` or the shorter `muxtools binaries rm x265`.

`muxtools binaries rm '*'` cleans up unused project-local versions while keeping the ones your config selects. It'll ask before removing anything, unless you pass `-y` for a script.

If you already have everything installed yourself, initialize with `-s` or set `prefer = "system"`.<br>
Muxtools will then look in PATH instead of downloading anything. `prefer = "global"` does the same thing as local mode but uses your shared user-global installs.

!!! warning
    Both the **local** and **global** scope will still let your scripts fallback to what may be in `PATH` if no versions are declared in the project. 

`--offline` works with `add`, `install` and `sync` when you only want to use the cached catalog and binaries you already have.<br>
Not every dependency has a managed package yet, so check [External Dependencies](external-dependencies.md) when you need something that isn't here.
