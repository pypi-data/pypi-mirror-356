"""Module for a yearly/monthly track summary."""

import datetime
from dataclasses import dataclass
from typing import Optional

from . import util
from .models.track import TrackWithMetadata


class Summary:
    """A summary of a user's tracks.

    :ivar years: Mapping of year to :class:`YearSummary`.
    :vartype years: dict[int, YearSummary]
    :ivar ascending: If ``True``, years will be sorted from old-to-new,
        otherwise they will be sorted new-to-old.
    :vartype ascending: bool
    """

    def __init__(self, ascending: bool = True):
        self.years: dict[int, YearSummary] = {}
        self.ascending = ascending

    def __iter__(self):
        items = list(self.years.values())
        items.sort(key=lambda y: y.year, reverse=not self.ascending)
        return iter(items)

    def __len__(self) -> int:
        return len(self.all_tracks())

    def all_tracks(self) -> list[TrackWithMetadata]:
        """Returns all tracks of the summary.

        :return: All tracks.
        """
        return [track for year in self for month in year for track in month.all_tracks()]

    def add(self, track: TrackWithMetadata):
        """Add a track to the summary.

        This automatically inserts the track into the right yearly summary.

        :raises ValueError: If the given track has no date set.
        :param track: The track to insert.
        :type track: fietsboek.model.track.Track
        """
        if track.date is None:
            raise ValueError("Cannot add a track without date")
        year = track.date.year
        self.years.setdefault(year, YearSummary(year, self.ascending)).add(track)

    @property
    def total_length(self) -> float:
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        """
        return sum(track.length for track in self.all_tracks())

    def stats(self) -> "CumulativeStats":
        """Returns the stats for all tracks in this summary.

        :return: The stats.
        """
        return CumulativeStats.from_tracks(self.all_tracks())


class YearSummary:
    """A summary over a single year.

    :ivar year: Year number.
    :ivar months: Mapping of month to :class:`MonthSummary`.
    :ivar ascending: If ``True``, months will be sorted from old-to-new,
        otherwise they will be sorted new-to-old.
    :vartype ascending: bool
    """

    def __init__(self, year: int, ascending: bool = True):
        self.year: int = year
        self.months: dict[int, MonthSummary] = {}
        self.ascending = ascending

    def __iter__(self):
        items = list(self.months.values())
        items.sort(key=lambda x: x.month, reverse=not self.ascending)
        return iter(items)

    def __len__(self) -> int:
        return len(self.all_tracks())

    def all_tracks(self) -> list[TrackWithMetadata]:
        """Returns all tracks of the summary.

        :return: All tracks.
        """
        return [track for month in self for track in month]

    def add(self, track: TrackWithMetadata):
        """Add a track to the summary.

        This automatically inserts the track into the right monthly summary.

        :raises ValueError: If the given track has no date set.
        :param track: The track to insert.
        """
        if track.date is None:
            raise ValueError("Cannot add a track without date")
        month = track.date.month
        self.months.setdefault(month, MonthSummary(month)).add(track)

    @property
    def total_length(self) -> float:
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        """
        return sum(track.length for track in self.all_tracks())

    def stats(self) -> "CumulativeStats":
        """Returns the stats for all tracks in this summary.

        :return: The stats.
        """
        return CumulativeStats.from_tracks(self.all_tracks())


class MonthSummary:
    """A summary over a single month.

    :ivar month: Month number (1-12).
    :ivar tracks: List of tracks in this month.
    """

    def __init__(self, month):
        self.month: int = month
        self.tracks: list[TrackWithMetadata] = []

    def __iter__(self):
        items = self.tracks[:]
        # We know that sorting by date works, we even assert that all tracks
        # have a date set.
        items.sort(key=lambda t: t.date)  # type: ignore
        return iter(items)

    def __len__(self) -> int:
        return len(self.all_tracks())

    def all_tracks(self) -> list[TrackWithMetadata]:
        """Returns all tracks of the summary.

        :return: All tracks.
        """
        return self.tracks[:]

    def add(self, track: TrackWithMetadata):
        """Add a track to the summary.

        :raises ValueError: If the given track has no date set.
        :param track: The track to insert.
        """
        if track.date is None:
            raise ValueError("Cannot add a track without date")
        self.tracks.append(track)

    @property
    def total_length(self) -> float:
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        """
        return sum(track.length for track in self.all_tracks())

    def stats(self) -> "CumulativeStats":
        """Returns the stats for all tracks in this summary.

        :return: The stats.
        """
        return CumulativeStats.from_tracks(self.all_tracks())


@dataclass
class CumulativeStats:
    """Cumulative user stats.

    The values start out with default values, and tracks can be merged in via
    :meth:`add`.
    """

    # pylint: disable=too-many-instance-attributes

    count: int = 0
    """Number of tracks added."""

    length: float = 0.0
    """Total length, in meters."""

    uphill: float = 0.0
    """Total uphill, in meters."""

    downhill: float = 0.0
    """Total downhill, in meters."""

    moving_time: datetime.timedelta = datetime.timedelta(0)
    """Total time spent moving."""

    stopped_time: datetime.timedelta = datetime.timedelta(0)
    """Total time standing still."""

    max_speed: float = 0.0
    """Overall maximum speed, in m/s."""

    longest_distance_track: Optional[TrackWithMetadata] = None
    """The track with the longest distance."""

    shortest_distance_track: Optional[TrackWithMetadata] = None
    """The track with the shortest distance."""

    longest_duration_track: Optional[TrackWithMetadata] = None
    """The track with the longest time."""

    shortest_duration_track: Optional[TrackWithMetadata] = None
    """The track with the shortest time."""

    @classmethod
    def from_tracks(cls, tracks: list[TrackWithMetadata]) -> "CumulativeStats":
        """Create a new stats collection from this list of tracks.

        :param tracks: List of tracks.
        :return: The stats.
        """
        stats = cls()
        for track in tracks:
            stats.add(track)
        return stats

    def add(self, track: TrackWithMetadata):
        """Adds a track to this stats collection.

        :param track: The track to add, with accompanying metadata.
        """
        self.count += 1
        self.length += track.length
        self.uphill += track.uphill
        self.downhill += track.downhill
        self.moving_time += track.moving_time
        self.stopped_time += track.stopped_time
        self.max_speed = max(self.max_speed, track.max_speed)

        if self.longest_distance_track is None or self.longest_distance_track.length < track.length:
            self.longest_distance_track = track

        if (
            self.shortest_distance_track is None
            or self.shortest_distance_track.length > track.length
        ):
            self.shortest_distance_track = track

        if (
            self.longest_duration_track is None
            or self.longest_duration_track.duration < track.duration
        ):
            self.longest_duration_track = track

        if (
            self.shortest_duration_track is None
            or self.shortest_duration_track.duration > track.duration
        ):
            self.shortest_duration_track = track

    @property
    def avg_speed(self) -> float:
        """Average speed, in m/s."""
        if not self.moving_time:
            return 0.0
        return self.length / self.moving_time.total_seconds()

    @property
    def avg_length(self) -> float:
        """Average length, in m."""
        if not self.count:
            return 0
        return self.length / self.count

    @property
    def avg_duration(self) -> datetime.timedelta:
        """Average duration of a track.

        Note that this property is automatically rounded to seconds.
        """
        if not self.count:
            return datetime.timedelta()
        return util.round_to_seconds((self.moving_time + self.stopped_time) / self.count)


__all__ = ["Summary", "YearSummary", "MonthSummary", "CumulativeStats"]
