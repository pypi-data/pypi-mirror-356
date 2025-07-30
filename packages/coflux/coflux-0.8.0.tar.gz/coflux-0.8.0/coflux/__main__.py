import asyncio
import functools
import os
import subprocess
import sys
import time
import types
import typing as t
from pathlib import Path

import click
import httpx
import tomlkit
import watchfiles

from . import Worker, config, decorators, loader, models

T = t.TypeVar("T")


def _callback(_changes: set[tuple[watchfiles.Change, str]]) -> None:
    print("Change detected. Reloading...")


def _api_request(method: str, host: str, action: str, **kwargs) -> t.Any:
    with httpx.Client() as client:
        response = client.request(method, f"http://{host}/api/{action}", **kwargs)
        # TODO: return errors
        response.raise_for_status()
        is_json = response.headers.get("Content-Type") == "application/json"
        return response.json() if is_json else None


def _encode_provides(
    provides: dict[str, list[str] | str | bool] | None,
) -> tuple[str, ...] | None:
    if not provides:
        return None
    return tuple(
        f"{k}:{str(v).lower() if isinstance(v, bool) else v}"
        for k, vs in provides.items()
        for v in (vs if isinstance(vs, list) else [vs])
    )


def _parse_provides(argument: tuple[str, ...] | None) -> dict[str, list[str]]:
    if not argument:
        return {}
    result: dict[str, list[str]] = {}
    for part in (p for a in argument for p in a.split(" ") if p):
        key, value = part.split(":", 1) if ":" in part else (part, "true")
        result.setdefault(key, []).append(value)
    return result


def _load_module(
    module: types.ModuleType,
) -> dict[str, tuple[models.Target, t.Callable]]:
    attrs = (getattr(module, k) for k in dir(module))
    return {
        a.name: (a.definition, a.fn)
        for a in attrs
        if isinstance(a, decorators.Target) and not a.definition.is_stub
    }


def _load_modules(
    modules: list[types.ModuleType | str],
) -> dict[str, dict[str, tuple[models.Target, t.Callable]]]:
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    targets = {}
    for module in list(modules):
        if isinstance(module, str):
            module = loader.load_module(module)
        targets[module.__name__] = _load_module(module)
    return targets


def _register_manifests(
    project_id: str,
    space_name: str,
    host: str,
    targets: dict[str, dict[str, tuple[models.Target, t.Callable]]],
) -> None:
    manifests = {
        module: {
            "workflows": {
                workflow_name: {
                    "parameters": [
                        {
                            "name": p.name,
                            "annotation": p.annotation,
                            "default": p.default,
                        }
                        for p in definition.parameters
                    ],
                    "waitFor": list(definition.wait_for),
                    "cache": (
                        definition.cache
                        and {
                            "params": definition.cache.params,
                            "maxAge": definition.cache.max_age,
                            "namespace": definition.cache.namespace,
                            "version": definition.cache.version,
                        }
                    ),
                    "defer": (
                        definition.defer
                        and {
                            "params": definition.defer.params,
                        }
                    ),
                    "delay": definition.delay,
                    "retries": (
                        definition.retries
                        and {
                            "limit": definition.retries.limit,
                            "delayMin": definition.retries.delay_min,
                            "delayMax": definition.retries.delay_max,
                        }
                    ),
                    "requires": definition.requires,
                    "instruction": definition.instruction,
                }
                for workflow_name, (definition, _) in target.items()
                if definition.type == "workflow"
            },
            "sensors": {
                sensor_name: {
                    "parameters": [
                        {
                            "name": p.name,
                            "annotation": p.annotation,
                            "default": p.default,
                        }
                        for p in definition.parameters
                    ],
                    "requires": definition.requires,
                    "instruction": definition.instruction,
                }
                for sensor_name, (definition, _) in target.items()
                if definition.type == "sensor"
            },
        }
        for module, target in targets.items()
    }
    # TODO: handle response?
    _api_request(
        "POST",
        host,
        "register_manifests",
        json={
            "projectId": project_id,
            "spaceName": space_name,
            "manifests": manifests,
        },
    )


def _init(
    *modules: types.ModuleType | str,
    project: str,
    space: str,
    host: str,
    provides: dict[str, list[str]],
    serialiser_configs: list[config.SerialiserConfig],
    blob_threshold: int,
    blob_store_configs: list[config.BlobStoreConfig],
    concurrency: int,
    launch_id: str | None,
    register: bool,
) -> None:
    try:
        targets = _load_modules(list(modules))
        if register:
            _register_manifests(project, space, host, targets)

        with Worker(
            project,
            space,
            host,
            provides,
            serialiser_configs,
            blob_threshold,
            blob_store_configs,
            concurrency,
            launch_id,
            targets,
        ) as worker:
            asyncio.run(worker.run())
    except KeyboardInterrupt:
        pass


@click.group()
def cli():
    pass


@cli.command("server")
@click.option(
    "-p",
    "--port",
    type=int,
    default=7777,
    help="Port to run server on",
)
@click.option(
    "-d",
    "--data-dir",
    type=click.Path(file_okay=False, path_type=Path, resolve_path=True),
    default="./data/",
    help="The directory to store data",
)
@click.option(
    "--image",
    default="ghcr.io/bitroot/coflux",
    help="The Docker image to run",
)
def server(port: int, data_dir: Path, image: str):
    """
    Start a local server.

    This is just a wrapper around Docker (which must be installed and running), useful for running the server in a development environment.
    """
    command = [
        "docker",
        "run",
        "--pull",
        ("missing" if image.startswith("sha256:") else "always"),
        "--publish",
        f"{port}:7777",
        "--volume",
        f"{data_dir}:/data",
        image,
    ]
    process = subprocess.run(command)
    sys.exit(process.returncode)


def _config_path():
    return Path.cwd().joinpath("coflux.toml")


def _read_config(path: Path) -> tomlkit.TOMLDocument:
    if path.exists():
        with path.open("r") as f:
            return tomlkit.load(f)
    else:
        # TODO: add instructions?
        return tomlkit.document()


def _write_config(path: Path, data: tomlkit.TOMLDocument):
    with path.open("w") as f:
        tomlkit.dump(data, f)


@functools.cache
def _load_config() -> config.Config:
    path = _config_path()
    return config.Config.model_validate(_read_config(path).unwrap())


@cli.command("configure")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    default=_load_config().project,
    show_default=True,
    prompt=True,
)
@click.option(
    "space",
    "-w",
    "--space",
    help="Space name",
    default=_load_config().space,
    show_default=True,
    prompt=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    default=_load_config().server.host,
    show_default=True,
    prompt=True,
)
def configure(
    host: str | None,
    project: str | None,
    space: str | None,
):
    """
    Populate/update the configuration file.
    """
    # TODO: connect to server to check details?
    click.secho("Writing configuration...", fg="black")

    path = _config_path()
    data = _read_config(path)
    data["project"] = project
    data["space"] = space
    data.setdefault("server", {})["host"] = host
    _write_config(path, data)

    click.secho(
        f"Configuration written to '{path.relative_to(Path.cwd())}'.", fg="green"
    )


@cli.group()
def spaces():
    """
    Manage spaces.
    """
    pass


@spaces.command("create")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    envvar="COFLUX_PROJECT",
    default=_load_config().project,
    show_default=True,
    required=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    envvar="COFLUX_HOST",
    default=_load_config().server.host,
    show_default=True,
    required=True,
)
@click.option(
    "--base",
    help="The base space to inherit from",
)
@click.argument("name")
def spaces_create(
    project: str,
    host: str,
    base: str | None,
    name: str,
):
    """
    Creates a space within the project.
    """
    base_id = None
    if base:
        spaces = _api_request("GET", host, "get_spaces", params={"project": project})
        space_ids_by_name = {w["name"]: id for id, w in spaces.items()}
        base_id = space_ids_by_name.get(base)
        if not base_id:
            click.BadOptionUsage("base", "Not recognised")

    # TODO: handle response
    _api_request(
        "POST",
        host,
        "create_space",
        json={
            "projectId": project,
            "name": name,
            "baseId": base_id,
        },
    )
    click.secho(f"Created space '{name}'.", fg="green")


@spaces.command("update")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    envvar="COFLUX_PROJECT",
    default=_load_config().project,
    show_default=True,
    required=True,
)
@click.option(
    "-w",
    "--space",
    help="The (current) name of the space",
    envvar="COFLUX_SPACE",
    default=_load_config().space,
    show_default=True,
    required=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    envvar="COFLUX_HOST",
    default=_load_config().server.host,
    show_default=True,
    required=True,
)
@click.option(
    "--name",
    help="The new name of the space",
)
@click.option(
    "--base",
    help="The new base space to inherit from",
)
@click.option(
    "--no-base",
    is_flag=True,
    help="Unset the base space",
)
def spaces_update(
    project: str,
    space: str,
    host: str,
    name: str | None,
    base: str | None,
    no_base: bool,
):
    """
    Updates a space within the project.
    """
    spaces = _api_request("GET", host, "get_spaces", params={"project": project})
    space_ids_by_name = {w["name"]: id for id, w in spaces.items()}
    space_id = space_ids_by_name.get(space)
    if not space_id:
        raise click.BadOptionUsage("space", "Not recognised")

    base_id = None
    if base:
        base_id = space_ids_by_name.get(base)
        if not base_id:
            raise click.BadOptionUsage("base", "Not recognised")

    payload = {
        "projectId": project,
        "spaceId": space_id,
    }
    if name is not None:
        payload["name"] = name

    if base is not None:
        payload["baseId"] = base_id
    elif no_base is True:
        payload["baseId"] = None

    # TODO: handle response
    _api_request("POST", host, "update_space", json=payload)

    click.secho(f"Updated space '{name or space}'.", fg="green")


@spaces.command("archive")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    envvar="COFLUX_PROJECT",
    default=_load_config().project,
    show_default=True,
    required=True,
)
@click.option(
    "-w",
    "--space",
    help="Space name",
    envvar="COFLUX_SPACE",
    default=_load_config().space,
    show_default=True,
    required=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    envvar="COFLUX_HOST",
    default=_load_config().server.host,
    show_default=True,
    required=True,
)
def spaces_archive(
    project: str,
    space: str,
    host: str,
):
    """
    Archives a space.
    """
    spaces = _api_request("GET", host, "get_spaces", params={"project": project})
    space_ids_by_name = {w["name"]: id for id, w in spaces.items()}
    space_id = space_ids_by_name.get(space)
    if not space_id:
        raise click.BadOptionUsage("space", "Not recognised")

    _api_request(
        "POST",
        host,
        "archive_space",
        json={
            "projectId": project,
            "spaceId": space_id,
        },
    )
    click.secho(f"Archived space '{space}'.", fg="green")


@cli.group()
def pools():
    """
    Manage pools.
    """
    pass


@pools.command("update")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    envvar="COFLUX_PROJECT",
    default=_load_config().project,
    show_default=True,
    required=True,
)
@click.option(
    "-w",
    "--space",
    help="Space name",
    envvar="COFLUX_SPACE",
    default=_load_config().space,
    show_default=True,
    required=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    envvar="COFLUX_HOST",
    default=_load_config().server.host,
    show_default=True,
    required=True,
)
@click.option(
    "modules",
    "-m",
    "--module",
    help="Modules to be hosted by workers in the pool",
    multiple=True,
    required=True,
)
@click.option(
    "--provides",
    help="Features that workers in the pool provide (to be matched with features that tasks require)",
    multiple=True,
)
@click.option(
    "--launcher",
    type=click.Choice(["docker"]),
    help="The type of launcher to use",
)
@click.option(
    "--image",
    help="The Docker image. Only valid for --launcher=docker.",
)
@click.argument("name")
def pools_update(
    project: str,
    space: str,
    host: str,
    modules: tuple[str, ...],
    provides: tuple[str, ...] | None,
    launcher: t.Literal["docker"] | None,
    image: str | None,
    name: str,
):
    """
    Updates a pool.
    """
    provides_ = _parse_provides(provides)
    launcher_ = None
    if launcher == "docker":
        launcher_ = {"type": "docker", "image": image}
    pool = {"modules": list(modules), "provides": provides_, "launcher": launcher_}
    _api_request(
        "POST",
        host,
        "update_pool",
        json={"projectId": project, "spaceName": space, "poolName": name, "pool": pool},
    )


@pools.command("delete")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    envvar="COFLUX_PROJECT",
    default=_load_config().project,
    show_default=True,
    required=True,
)
@click.option(
    "-w",
    "--space",
    help="Space name",
    envvar="COFLUX_SPACE",
    default=_load_config().space,
    show_default=True,
    required=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    envvar="COFLUX_HOST",
    default=_load_config().server.host,
    show_default=True,
    required=True,
)
@click.argument("name")
def pools_delete(project: str, space: str, host: str, name: str):
    """
    Deletes a pool.
    """
    _api_request(
        "POST",
        host,
        "update_pool",
        json={"projectId": project, "spaceName": space, "poolName": name, "pool": None},
    )


@cli.command("register")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    envvar="COFLUX_PROJECT",
    default=_load_config().project,
    show_default=True,
    required=True,
)
@click.option(
    "-w",
    "--space",
    help="Space name",
    envvar="COFLUX_SPACE",
    default=_load_config().space,
    show_default=True,
    required=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    envvar="COFLUX_HOST",
    default=_load_config().server.host,
    show_default=True,
    required=True,
)
@click.argument("module_name", nargs=-1)
def register(
    project: str,
    space: str,
    host: str,
    module_name: tuple[str, ...],
) -> None:
    """
    Register modules with the server.

    Paths to scripts can be passed instead of module names.

    Options will be loaded from the configuration file, unless overridden as arguments (or environment variables).
    """
    if not module_name:
        raise click.ClickException("No module(s) specified.")
    targets = _load_modules(list(module_name))
    _register_manifests(project, space, host, targets)
    click.secho("Manifest(s) registered.", fg="green")


@cli.command("worker")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    envvar="COFLUX_PROJECT",
    default=_load_config().project,
    show_default=True,
    required=True,
)
@click.option(
    "-w",
    "--space",
    help="Space name",
    envvar="COFLUX_SPACE",
    default=_load_config().space,
    show_default=True,
    required=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    envvar="COFLUX_HOST",
    default=_load_config().server.host,
    show_default=True,
    required=True,
)
@click.option(
    "--provides",
    help="Features that this worker provides (to be matched with features that tasks require)",
    multiple=True,
    envvar="COFLUX_PROVIDES",
    default=_encode_provides(_load_config().provides),
    show_default=True,
)
@click.option(
    "--launch",
    help="The launch ID",
    envvar="COFLUX_LAUNCH",
)
@click.option(
    "--concurrency",
    type=int,
    help="Limit on number of executions to process at once",
    default=_load_config().concurrency,
    show_default=True,
)
@click.option(
    "--watch",
    is_flag=True,
    default=False,
    help="Enable auto-reload when code changes",
)
@click.option(
    "--register",
    is_flag=True,
    default=False,
    help="Automatically register modules",
)
@click.option(
    "--dev",
    is_flag=True,
    default=False,
    help="Enable development mode (implies `--watch` and `--register`)",
)
@click.argument("module_name", nargs=-1)
def worker(
    project: str,
    space: str,
    host: str,
    provides: tuple[str, ...] | None,
    launch: str | None,
    concurrency: int,
    watch: bool,
    register: bool,
    dev: bool,
    module_name: tuple[str, ...],
) -> None:
    """
    Start a worker.

    Hosts the specified modules. Paths to scripts can be passed instead of module names.

    Options will be loaded from the configuration file, unless overridden as arguments (or environment variables).
    """
    if not module_name:
        raise click.ClickException("No module(s) specified.")
    provides_ = _parse_provides(provides)
    config = _load_config()
    args = (*module_name,)
    kwargs = {
        "project": project,
        "space": space,
        "host": host,
        "provides": provides_,
        "serialiser_configs": config and config.serialisers,
        "blob_threshold": config and config.blobs and config.blobs.threshold,
        "blob_store_configs": config and config.blobs and config.blobs.stores,
        "concurrency": concurrency,
        "launch_id": launch,
        "register": register or dev,
    }
    if watch or dev:
        filter = watchfiles.PythonFilter()
        watchfiles.run_process(
            ".",
            target=_init,
            args=args,
            kwargs=kwargs,
            callback=_callback,
            watch_filter=filter,
        )
    else:
        _init(*args, **kwargs)


@cli.command("submit")
@click.option(
    "-p",
    "--project",
    help="Project ID",
    envvar="COFLUX_PROJECT",
    default=_load_config().project,
    show_default=True,
    required=True,
)
@click.option(
    "-w",
    "--space",
    help="Space name",
    envvar="COFLUX_SPACE",
    default=_load_config().space,
    show_default=True,
    required=True,
)
@click.option(
    "-h",
    "--host",
    help="Host to connect to",
    envvar="COFLUX_HOST",
    default=_load_config().server.host,
    show_default=True,
    required=True,
)
@click.argument("module")
@click.argument("target")
@click.argument("argument", nargs=-1)
def submit(
    project: str,
    space: str,
    host: str,
    module: str,
    target: str,
    argument: tuple[str, ...],
) -> None:
    """
    Submit a workflow to be run.
    """
    # TODO: support overriding options?
    workflow = _api_request(
        "GET",
        host,
        "get_workflow",
        params={
            "project": project,
            "space": space,
            "module": module,
            "target": target,
        },
    )
    execute_after = (
        int((time.time() + workflow["delay"]) * 1000) if workflow["delay"] else None
    )
    # TODO: handle response
    _api_request(
        "POST",
        host,
        "submit_workflow",
        json={
            "projectId": project,
            "spaceName": space,
            "module": module,
            "target": target,
            "arguments": [["json", a] for a in argument],
            "waitFor": workflow["waitFor"],
            "cache": workflow["cache"],
            "defer": workflow["defer"],
            "executeAfter": execute_after,
            "retries": workflow["retries"],
            "requires": workflow["requires"],
        },
    )
    click.secho("Workflow submitted.", fg="green")
    # TODO: follow logs?
    # TODO: wait for result?


if __name__ == "__main__":
    cli()
