"""
File mapping for tracking block/sector status.

Pure data structure for tracking status of byte ranges without
any file format dependencies.
"""

import bisect
import logging

# Prevents sort (not a number, so not less, greater or equal to itself)
NO_SORT = float("nan")

# Block status codes
STATUS_OK = "+"  # Successfully read
STATUS_ERROR = "-"  # Read error
STATUS_UNTRIED = "?"  # Not tried yet
STATUS_TRIMMED = "/"  # Trimmed (not tried because of read error)
STATUS_SLOW = "*"  # Non-trimmed, non-scraped (slow reads)
STATUS_SCRAPED = "#"  # Non-trimmed, scraped (slow reads completed)

# Helper sets for fast status categorization
CACHED = {STATUS_OK, STATUS_SLOW, STATUS_SCRAPED}  # Have data
UNCACHED = {STATUS_UNTRIED}  # Need data
ERROR = {STATUS_ERROR, STATUS_TRIMMED}  # Can't get data
STATUSES = CACHED | UNCACHED | ERROR  # All valid statuses

log = logging.getLogger(__name__)


class FileMap:
    """
    Tracks status of byte ranges using efficient transition-based representation.

    Pure data structure with no file format dependencies.
    Uses slice notation: filemap[start:end] = status
    """

    def __init__(self, size: int):
        """Initialize with device/file size."""
        self.size = size
        self.pass_ = 1  # ddrescue compatibility

        # Transitions list: (position, NO_SORT, status)
        # Each entry marks where status changes
        # Initialize with empty device (all untried), with a duplicate status at the end
        # for ease of insert
        self.transitions = [(0, NO_SORT, STATUS_UNTRIED), (size, NO_SORT, STATUS_UNTRIED)]

    def __setitem__(self, key, status):
        """Set status for range using slice notation: filemap[start:end] = status"""
        if isinstance(key, slice):
            # Check bounds before calling indices() which clamps values
            if key.start is not None and key.start < 0:
                raise ValueError(f"Negative start index: {key.start}")
            if key.stop is not None and key.stop > self.size:
                raise ValueError(f"Stop index beyond device size: {key.stop} > {self.size}")

            start, stop, step = key.indices(self.size)
            if step != 1:
                raise ValueError("Step not supported")
            self._set_status_range(start, stop - 1, status)
        else:
            # Single offset
            self._set_status_range(key, key, status)

    def __getitem__(self, key):
        """Get status for range using slice notation: filemap[start:end] returns transitions"""
        if isinstance(key, slice):
            # Check bounds before calling indices() which clamps values
            if key.start is not None and key.start < 0:
                raise ValueError(f"Negative start index: {key.start}")
            if key.stop is not None and key.stop > self.size:
                raise ValueError(f"Stop index beyond device size: {key.stop} > {self.size}")

            start, stop, step = key.indices(self.size)
            if step != 1:
                raise ValueError("Step not supported")

            # Return empty list for empty range
            if start >= stop:
                return []

            return self._get_transitions_range(start, stop - 1)
        else:
            # Single offset
            return self._get_status_at(key)

    def _get_transitions_range(self, start: int, end: int) -> list[tuple]:
        """Get transitions covering range with synthetic start/end positions."""
        # Find transitions that fall within our range [start, end]
        # We want transitions where start < transition.pos <= end
        result = []

        # Get status at start position
        start_search = (start + 1, NO_SORT, "")
        start_idx = bisect.bisect_left(self.transitions, start_search)
        start_transition_idx = max(0, start_idx - 1)
        start_status = self.transitions[start_transition_idx][2]

        # Add synthetic start
        result.append((start, NO_SORT, start_status))

        # Add all transitions that fall within (start, end]
        for i in range(len(self.transitions)):
            pos = self.transitions[i][0]
            if start < pos <= end:
                result.append(self.transitions[i])

        # Get status at end position (might be different from start if we crossed transitions)
        end_search = (end + 1, NO_SORT, "")
        end_idx = bisect.bisect_left(self.transitions, end_search)
        end_transition_idx = max(0, end_idx - 1)
        end_status = self.transitions[end_transition_idx][2]

        # Add synthetic end
        result.append((end, NO_SORT, end_status))

        return result

    def _get_status_at(self, offset: int) -> str:
        """Get status at single offset using efficient bisect lookup."""
        # Search for (offset + 1, ...) to find the transition that starts after offset
        search_key = (offset + 1, NO_SORT, "")
        idx = bisect.bisect_left(self.transitions, search_key)

        # The transition covering offset is at idx-1 (or 0 if idx is 0)
        transition_idx = max(0, idx - 1)

        return self.transitions[transition_idx][2]

    def _set_status_range(self, start: int, end: int, status: str) -> None:
        """Set the status for a range of bytes."""
        log.debug("Setting status %s for range [%d, %d]", status, start, end)

        start_key = (start, NO_SORT, status)
        end_key = (end + 1, NO_SORT, STATUS_UNTRIED)

        # Find indices using binary search
        start_idx = bisect.bisect_left(self.transitions, start_key)
        end_idx = bisect.bisect_right(self.transitions, end_key)

        # Determine before and after indices
        before_idx = max(start_idx - 1, 0)
        after_idx = min(end_idx, len(self.transitions) - 1)

        # Get the 5 variables we need
        before_status = self.transitions[before_idx][2]  # before_start.status
        before_pos = self.transitions[before_idx][0]  # before_start.pos
        after_status = self.transitions[after_idx][2]  # after.status
        after_pos = self.transitions[after_idx][0]  # after.pos

        # Find before_end: what status exists at end+1 position before our change
        before_end_idx = max(0, end_idx - 1)
        before_end_status = self.transitions[before_end_idx][2]

        splice = []
        if before_pos == start:
            # overwrite the start position
            splice.append(start_key)
        else:
            splice.append((before_pos, NO_SORT, before_status))
            if before_status != status:
                # if the status is different, we need to add a new entry
                splice.append(start_key)

        if before_end_status != status or end_idx == len(self.transitions):
            splice.append((end + 1, NO_SORT, before_end_status))
        if end + 1 < after_pos:
            splice.append((after_pos, NO_SORT, after_status))

        self.transitions[before_idx : after_idx + 1] = splice

    @property
    def pos(self) -> int:
        """Current position - first untried byte."""
        for position, _, status in self.transitions:
            if status == STATUS_UNTRIED:
                return position
        raise ValueError("FileMap transitions corrupted.")

    @property
    def status(self) -> str:
        """Current status - highest priority status found in transitions."""
        if len(self.transitions) < 2:
            raise ValueError("FileMap transitions corrupted")

        # ddrescue priority order: error > untried > trimmed > slow > scraped > ok
        priority_order = [STATUS_ERROR, STATUS_UNTRIED, STATUS_TRIMMED, STATUS_SLOW, STATUS_SCRAPED, STATUS_OK]

        statuses = {self.transitions[i][2] for i in range(len(self.transitions) - 1)}

        for status in priority_order:
            if status in statuses:
                return status

        raise ValueError("FileMap transitions corrupted")
