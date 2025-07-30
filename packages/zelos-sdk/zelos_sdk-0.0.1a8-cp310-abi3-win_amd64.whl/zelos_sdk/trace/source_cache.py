from typing import Any, Dict, Union
import logging
import time

# Cannot import zelos_sdk here, it will cause a circular import. Pull in the native module directly instead.
from zelos_sdk import TraceEventFieldMetadata, TraceSource, TraceSourceEvent

log = logging.getLogger(__name__)


class TraceSourceCacheLastField:
    """A cached field that stores the last logged value.

    Example:
        field = event.rpm       # Get field
        field.get()             # Get cached value
        field.name              # Get full path like "motor_stats.rpm"
    """

    def __init__(self, name: str, metadata: TraceEventFieldMetadata, full_path: str) -> None:
        self.name = full_path  # Use full path as the name
        self.field_name = name  # Keep the original field name for internal use
        self.metadata = metadata
        self.value: Any = None

    def get(self) -> Any:
        """Get the cached value."""
        return self.value

    def set(self, value: Any) -> None:
        """Set the cached value."""
        self.value = value

    @property
    def data_type(self):
        """Get the field's data type."""
        return self.metadata.data_type

    def __repr__(self) -> str:
        return f"TraceSourceCacheLastField(name='{self.name}', value={self.value})"


class TraceSourceCacheLastEvent:
    """A cached event that provides access to fields and submessages.

    Example:
        event = source.motor_stats
        event.rpm.get()              # Get field value
        event.thermal.temp.get()     # Get nested field value
        event.log(rpm=3500)          # Log new values
    """

    def __init__(self, name: str, event: TraceSourceEvent, source: "TraceSourceCacheLast") -> None:
        self.name = name  # This is already the full path
        self.event = event
        self.source = source
        self.fields: Dict[str, TraceSourceCacheLastField] = {}
        self.submessages: Dict[str, "TraceSourceCacheLastEvent"] = {}

        # Initialize fields from the event schema
        for field_meta in event.schema:
            field_full_path = f"{self.name}.{field_meta.name}"
            self.fields[field_meta.name] = TraceSourceCacheLastField(field_meta.name, field_meta, field_full_path)

    def get_field(self, name: str) -> TraceSourceCacheLastField:
        """Get a field by name, even if there's a submessage with the same name."""
        if name in self.fields:
            return self.fields[name]
        raise AttributeError(f"Event {self.name} has no field {name}")

    def get_submessage(self, name: str) -> "TraceSourceCacheLastEvent":
        """Get a submessage by name."""
        if name in self.submessages:
            return self.submessages[name]
        raise AttributeError(f"Event {self.name} has no submessage {name}")

    def __getattr__(self, name: str) -> Any:
        # First check if it's already cached as a submessage
        if name in self.submessages:
            return self.submessages[name]

        # Then check if it's a field
        if name in self.fields:
            return self.fields[name]

        # Check if it's a field in the event schema that hasn't been cached yet
        try:
            field_meta = next(f for f in self.event.schema if f.name == name)
            field_full_path = f"{self.name}.{name}"
            field = TraceSourceCacheLastField(name, field_meta, field_full_path)
            self.fields[name] = field
            return field
        except StopIteration:
            pass  # Not a field, continue to check for submessages

        # Try to get it as a submessage from the source (only if it exists)
        submessage_name = f"{self.name}/{name}"
        try:
            cached_event = self.source._get_cached_event(submessage_name)
            self.submessages[name] = cached_event
            return cached_event
        except KeyError:
            # Neither a field nor a submessage
            raise AttributeError(
                f"Event {self.name} has no field or submessage '{name}'. "
                f"Available fields: {list(self.fields.keys())}, "
                f"Available submessages: {list(self.submessages.keys())}"
            )

    def log(self, **kwargs: Any) -> None:
        """Log values to this event and update the cache."""
        self.source.log(self.name, kwargs)

    def log_at(self, time_ns: int, **kwargs: Any) -> None:
        """Log values to this event at a specific time and update the cache."""
        self.source.log_at(time_ns, self.name, **kwargs)

    def _update_cache(self, data: Dict[str, Any]) -> None:
        """Update the cached field values"""
        for field_name, value in data.items():
            self.fields[field_name].set(value)


class TraceSourceCacheLast:
    """A TraceSource wrapper that caches the last value of each field.

    Example:
        source = TraceSourceCacheLast("motor_controller")
        source.add_event("motor_stats", [
            TraceEventFieldMetadata("rpm", DataType.Float64),
            TraceEventFieldMetadata("torque", DataType.Float64, "Nm")
        ])

        # Log some data
        source.log("motor_stats", {"rpm": 3500.0, "torque": 42.8})

        # Access cached values
        assert source.motor_stats.rpm.get() == 3500.0
        assert source.motor_stats.torque.get() == 42.8

        # Dictionary-style access
        assert source["motor_stats"].rpm.get() == 3500.0
        assert source["motor_stats/rpm"] == 3500.0

        # Log via event object
        source.motor_stats.log(rpm=3250.0, torque=45.2)
    """

    def __init__(self, name: str) -> None:
        self.source = TraceSource(name)
        self.events: Dict[str, TraceSourceCacheLastEvent] = {}

    def get_source(self) -> TraceSource:
        """Get the underlying TraceSource."""
        return self.source

    def _get_or_create_cached_event(self, name: str) -> TraceSourceCacheLastEvent:
        """Get or create a cached event, consolidating the creation logic."""
        if name in self.events:
            return self.events[name]

        # Try to get the event from the underlying source first
        try:
            event = self.source.get_event(name)
            cached_event = TraceSourceCacheLastEvent(name, event, self)
            self.events[name] = cached_event

            # If this is a nested event, ensure all parent events are created and linked
            if "/" in name:
                self._ensure_parent_hierarchy(name, cached_event)

            return cached_event
        except KeyError:
            # Event doesn't exist in the source, this should raise an error
            raise KeyError(f"Event '{name}' not found in source")

    def _ensure_parent_hierarchy(self, event_name: str, cached_event: TraceSourceCacheLastEvent) -> None:
        """Ensure all parent events in the hierarchy are created and properly linked."""
        parts = event_name.split("/")

        # Build the hierarchy from top to bottom
        for i in range(len(parts) - 1):
            parent_path = "/".join(parts[: i + 1])
            child_name = parts[i + 1]

            # Ensure parent exists
            if parent_path not in self.events:
                try:
                    parent_event = self.source.get_event(parent_path)
                    self.events[parent_path] = TraceSourceCacheLastEvent(parent_path, parent_event, self)
                except KeyError:
                    # Parent doesn't exist in source, skip this level
                    continue

            # Link child to parent
            parent_cached = self.events[parent_path]
            if i == len(parts) - 2:  # This is the direct parent of our target event
                parent_cached.submessages[child_name] = cached_event
            else:  # This is an intermediate parent, link to the next level
                next_child_path = "/".join(parts[: i + 2])
                if next_child_path in self.events:
                    parent_cached.submessages[child_name] = self.events[next_child_path]

    def add_event(self, name: str, schema) -> TraceSourceCacheLastEvent:
        """Add an event to the source and create a cached version."""
        event = self.source.add_event(name, schema)
        cached_event = TraceSourceCacheLastEvent(name, event, self)
        self.events[name] = cached_event
        return cached_event

    def log(self, name: str, data: Dict[str, Any]) -> None:
        """Log data to an event and update the cache."""
        self.log_at(time_ns=time.time_ns(), name=name, data=data)

    def log_at(self, time_ns: int, name: str, data: Dict[str, Any]) -> None:
        """Log data to an event at a specific time and update the cache."""
        log.debug(f"Logging {name} at {time_ns} with data {data}")
        self.source.log_at(time_ns, name, data)

        # Ensure the event is in our cache (it might have been created dynamically)
        self._get_or_create_cached_event(name)

        if name in self.events:
            # Update the cache after logging
            self._update_event_cache(name, data)
        else:
            raise ValueError(f"Event {name} not found")

    def _update_event_cache(self, name: str, data: Dict[str, Any]) -> None:
        """Update the cache for a specific event after logging"""
        cached_event = self.events[name]
        cached_event._update_cache(data)

    def _get_cached_event(self, name: str) -> TraceSourceCacheLastEvent:
        """Get a cached event if it exists, without creating it."""
        return self.events[name]

    def _get_cached_field(self, name: str) -> TraceSourceCacheLastField:
        """Get a cached field if it exists, without creating it."""
        # Remove the last part of the name
        # ex: "my_event/foo/bar" -> event_name="my_event/foo", field_name="bar"
        try:
            event_name, field_name = name.rsplit("/", 1)
            return self.events[event_name].get_field(field_name)
        except Exception:
            raise KeyError(f"Field '{name}' not found")

    def __getattr__(self, name: str) -> TraceSourceCacheLastEvent:
        """Get an event by attribute access. Only returns existing events."""
        try:
            return self._get_cached_event(name)
        except KeyError as e:
            raise AttributeError(str(e))

    def __getitem__(self, key: str) -> Union[TraceSourceCacheLastEvent, TraceSourceCacheLastField, Any]:
        """Support dictionary-style access for events and fields.

        Examples:
            source["my_event"]              # Returns TraceSourceCacheLastEvent
            source["my_event/subevent"]     # Returns nested TraceSourceCacheLastEvent
            source["my_event/field"]        # Returns TraceSourceCacheLastField object
            source["event/sub/field"]       # Returns deeply nested TraceSourceCacheLastField object
        """
        try:
            return self._get_cached_event(key)
        except KeyError:
            pass

        try:
            return self._get_cached_field(key)
        except KeyError:
            pass

        raise KeyError(f"Event or field path '{key}' not found")
