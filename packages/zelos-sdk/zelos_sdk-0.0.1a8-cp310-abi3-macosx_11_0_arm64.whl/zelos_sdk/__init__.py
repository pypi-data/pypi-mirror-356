# Disable ruff reformatting of imports in this file and complaining about wildcard imports
# ruff: noqa: I001, F403

# Import the rust module into the root of our package
# https://github.com/PyO3/pyo3/issues/759#issuecomment-1813396106
from .zelos_sdk import *

# This requires the rust module to be imported first
from .trace import TraceSourceCacheLast, TraceSourceCacheLastEvent, TraceSourceCacheLastField

# Explicit imports with 'as' aliases to satisfy type checkers
from .zelos_sdk import (
    TracePublishClient as TracePublishClient,
    TracePublishClientConfig as TracePublishClientConfig,
    TraceSource as TraceSource,
    enable_logging as enable_logging,
    init_global_client as init_global_client,
    init_global_source as init_global_source,
)

from typing import Optional


def init(
    name: Optional[str] = None,
    *,
    url: Optional[str] = None,
    client_config: Optional[TracePublishClientConfig] = None,
    log_level: Optional[str] = None,
    default: bool = True,
) -> None:
    """
    Initialize the Zelos SDK tracing system.

    Args:
        name: A unique identifier for your application. Defaults to "py".
        client_config: Configuration options for the TracePublishClient.
            Can include: url, batch_size, batch_timeout_ms.
        log_level: Logging level to enable, None disables logging.
        default: Whether to initialize global defaults. If False, only enables
            logging without setting up global client/source.

    Examples:
        >>> # Initialize with defaults
        >>> init()
        >>>
        >>> # Initialize with custom name
        >>> init("my_app")
        >>>
        >>> # Initialize with custom config
        >>> init(
        ...     "my_app",
        ...     client_config=TracePublishClientConfig(
        ...         url="grpc://localhost:2300",
        ...     ),
        ...     log_level="debug"
        ... )
        >>>
        >>> # Initialize only logging, no global defaults
        >>> init(log_level="debug", default=False)
    """

    # Enable logging if requested
    if log_level is not None:
        enable_logging(log_level)

    # Only initialize global defaults if requested
    if default:
        # Initialize the global client
        client_config = client_config or TracePublishClientConfig()
        if url is not None:
            client_config.url = url
        init_global_client(client_config)

        # Initialize the global source
        init_global_source(name)


__all__ = [
    "TraceSourceCacheLast",
    "TraceSourceCacheLastEvent",
    "TraceSourceCacheLastField",
    "init",
]
