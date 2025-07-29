from __future__ import annotations

import dataclasses
from typing import Any, Callable, Optional

import jax
import orbax.checkpoint as ocp
import yaml
from etils import epath
from orbax.checkpoint import options as options_lib
from orbax.checkpoint._src import asyncio_utils
from orbax.checkpoint._src.futures import future

from . import serialization  # Register dataclass support # noqa: F401

PyTree = Any


def get_abstract(pytree):
    def to_struct(x):
        if isinstance(x, jax.Array):
            return jax.ShapeDtypeStruct(x.shape, x.dtype)
        return x

    return jax.tree.map(to_struct, pytree)


def load_abstract(directory: epath.Path):
    with (directory / "state.yaml").open("r") as f:
        return yaml.load(f, Loader=yaml.Loader)


def save_abstract(directory: epath.Path, item: PyTree):
    with (directory / "state.yaml").open("w") as f:
        yaml.dump(get_abstract(item), f)


def jax_struct_representer(dumper, data):
    return dumper.represent_mapping(
        "tag:yaml.org,2002:python/object/apply:jax.ShapeDtypeStruct",
        {"kwds": {"shape": data.shape, "dtype": str(data.dtype)}},
    )


yaml.add_representer(jax.ShapeDtypeStruct, jax_struct_representer)


class CheckpointHandler(ocp.StandardCheckpointHandler):
    async def _save_fn(self, item: PyTree, directory: epath.Path) -> None:
        if not ocp.utils.is_primary_host(self._impl._primary_host):
            return
        save_abstract(directory, item)
        try:
            load_abstract(directory)
        except yaml.YAMLError as e:
            raise ValueError(
                "Unable to properly serialize the state. Consider using flax_orbax.serialization.wrap to capture "
            ) from e

    async def async_save(
        self,
        directory: epath.Path,
        item: Optional[PyTree] = None,
        save_args: Optional[PyTree] = None,
        args: Optional[SaveArgs] = None,
    ):
        futures = [
            future.CommitFutureAwaitingContractedSignals(
                self._save_fn(item or args.item, directory), name="yaml_save"
            )
        ]
        pytree_futures = await super().async_save(
            directory, item=item, save_args=save_args, args=args
        )
        return futures + pytree_futures

    def save(self, directory: epath.Path, item=None, save_args=None, args=None):
        async def async_save(directory, item, save_args, args):
            commit_futures = await self.async_save(directory, item, save_args, args)
            if commit_futures:
                for f in commit_futures:
                    f.result()

        asyncio_utils.run_sync(async_save(directory, item, save_args, args))

    def restore(self, directory: epath.Path, item=None, args=None):
        if not args:
            args = RestoreArgs(item=item)
        if args.item is None:
            args.item = load_abstract(directory)
        if args.sharding is not None:
            args.item = _set_sharding(args.item, args.sharding)

        try:
            return super().restore(directory, args=args)
        except ValueError as e:
            sharding = args.fallback_sharding
            if sharding is None:
                raise ValueError(
                    "Please specify a sharding or fallback sharding in RestoreArgs"
                ) from e
            args.item = _set_sharding(args.item, args.sharding)
            return super().restore(directory, args=args)


def _set_sharding(item, sharding):
    sharding = jax.tree.map(
        lambda subsharding, subtree: jax.tree.map(lambda _: subsharding, subtree),
        sharding,
        item,
    )
    item = jax.tree.map(
        lambda x, s: jax.ShapeDtypeStruct(x.shape, x.dtype, sharding=s), item, sharding
    )
    return item


class Checkpointer(ocp.AsyncCheckpointer):
    def __init__(
        self,
        *,
        async_options: options_lib.AsyncOptions = options_lib.AsyncOptions(),
        multiprocessing_options: options_lib.MultiprocessingOptions = options_lib.MultiprocessingOptions(),
        file_options: options_lib.FileOptions = options_lib.FileOptions(),
        checkpoint_metadata_store=None,
        temporary_path_class=None,
        **kwargs,
    ):
        super().__init__(
            CheckpointHandler(
                multiprocessing_options=multiprocessing_options,
                **kwargs,
            ),
            async_options=async_options,
            multiprocessing_options=multiprocessing_options,
            file_options=file_options,
            checkpoint_metadata_store=checkpoint_metadata_store,
            temporary_path_class=temporary_path_class,
        )

    def save(
        self,
        directory: epath.PathLike,
        state: PyTree,
        *,
        save_args: Optional[PyTree] = None,
        force: bool = False,
        custom_metadata: dict[str, Any] | None = None,
    ):
        """Saves a checkpoint asynchronously (does not block).

        Args:
        directory: Path where the checkpoint will be saved.
        state: a PyTree of arrays to be saved.
        save_args: a PyTree with the same structure of `item`, which consists of
            `ocp.SaveArgs` objects as values. `None` can be used for values where no
            `SaveArgs` are specified. Only necessary for fine-grained customization
            of saving behavior for individual parameters.
        force: See superclass documentation.
        custom_metadata: a dictionary of custom metadata to be written to the
            checkpoint directory via StepMetadata.
        """
        super().save(
            directory,
            args=SaveArgs(state, save_args),
            force=force,
            custom_metadata=custom_metadata,
        )

    def restore(
        self,
        directory: epath.Path,
        target: Optional[PyTree] = None,
        sharding: jax.sharding.Sharding | Callable | None = None,
        *,
        strict: bool = True,
    ) -> Any:
        """Restores a checkpoint.

        Args:
        directory: Path where the checkpoint will be saved.
        target: a PyTree representing the expected structure of the checkpoint.
            Values may be either real array or scalar values, or they may be
            jax.ShapeDtypeStruct. If real values are provided, that value will be
            restored as the given type, with the given properties. If
            jax.ShapeDtypeStruct is provided, the value will be restored as
            np.ndarray, unless `sharding` is specified. If `item` is a custom PyTree
            class, the tree will be restored with the same structure as provided. If
            not provided, restores as a serialized nested dict representation of the
            custom class.
        strict: if False, restoration allows silent truncating/padding of arrays
            if the stored array shape does not match the target shape. Otherwise,
            raises an error.

        Returns:
        The restored checkpoint.
        """
        return super().restore(
            directory,
            args=RestoreArgs(target, strict=strict, sharding=sharding),
        )


class SaveArgs(ocp.args.StandardSave):
    pass


@dataclasses.dataclass
class RestoreArgs(ocp.args.StandardRestore):
    sharding: jax.sharding.Sharding | Callable | None = None
    pass


ocp.checkpoint_args.register_with_handler(
    CheckpointHandler, for_save=True, for_restore=False
)(SaveArgs)
ocp.checkpoint_args.register_with_handler(
    CheckpointHandler, for_save=False, for_restore=True
)(RestoreArgs)
