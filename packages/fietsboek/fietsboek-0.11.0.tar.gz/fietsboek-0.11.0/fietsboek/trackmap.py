"""Module to render tracks to static images on OSM tiles."""

import io
import math

from gpxpy.gpx import GPX
from PIL import Image, ImageDraw

from .config import TileLayerConfig
from .views.tileproxy import TileRequester

TILE_SIZE = 256


def to_web_mercator(lat: float, lon: float, zoom: int) -> tuple[int, int]:
    """Convert a pari of latitude/longitude coordinates to web mercator form.

    :param lat: Latitude (in degrees).
    :param lon: Longitude (in degrees).
    :param zoom: Zoom level.
    :return: The web mercator x/y coordinates. Both will be between 0 and
        2**zoom * 256.
    """
    width = height = TILE_SIZE

    la = math.radians(lon)
    phi = math.radians(lat)

    x = float(2**zoom) / (2 * math.pi) * width * (la + math.pi)
    y = (
        float(2**zoom)
        / (2 * math.pi)
        * height
        * (math.pi - math.log(math.tan((math.pi / 4 + phi / 2))))
    )

    return (int(math.floor(x)), int(math.floor(y)))


class TrackMapRenderer:
    """A renderer that renders GPX tracks onto small map excerpts."""

    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        track: GPX,
        requester: TileRequester,
        size: tuple[int, int],
        layer: TileLayerConfig,
    ):
        self.track = track
        self.requester = requester
        self.size = size
        self.layer = layer
        self.maxzoom = layer.zoom
        self.color = (0, 0, 255)
        self.line_width = 5

    def render(self) -> Image.Image:
        """Render the track.

        :return: The image containing the rendered preview.
        """
        zoom, bbox = self._find_zoom()
        image = Image.new("RGB", self.size)
        start_x, start_y = self._draw_base(image, zoom, bbox)
        self._draw_lines(image, zoom, start_x, start_y)
        return image

    def _find_zoom(self) -> tuple[int, tuple[int, int, int, int]]:
        for zoom in range(self.maxzoom or 19, 0, -1):
            min_x, max_x = 2**zoom * TILE_SIZE, 0
            min_y, max_y = 2**zoom * TILE_SIZE, 0

            for point in self.track.walk(only_points=True):
                x, y = to_web_mercator(point.latitude, point.longitude, zoom)
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

                if max_x - min_x > self.size[0] or max_y - min_y > self.size[1]:
                    break
            else:
                return zoom, (min_x, max_x, min_y, max_y)

        return 1, (0, 512, 0, 512)

    def _draw_base(self, image, zoom, bbox):
        min_x, max_x, min_y, max_y = bbox
        # We center the track by centering its bounding box
        start_x = min_x - (self.size[0] - (max_x - min_x)) // 2
        start_y = min_y - (self.size[1] - (max_y - min_y)) // 2

        offset_x = start_x // TILE_SIZE * TILE_SIZE - start_x
        offset_y = start_y // TILE_SIZE * TILE_SIZE - start_y

        for i in range(int(math.ceil(self.size[0] / TILE_SIZE)) + 1):
            for j in range(int(math.ceil(self.size[1] / TILE_SIZE)) + 1):
                tile = self._load_tile(zoom, start_x // TILE_SIZE + i, start_y // TILE_SIZE + j)
                image.paste(tile, (i * TILE_SIZE + offset_x, j * TILE_SIZE + offset_y))

        return start_x, start_y

    def _load_tile(self, zoom, x, y) -> Image.Image:
        tile_data = self.requester.load_tile(self.layer, zoom, x, y)
        if not tile_data:
            return Image.new("RGB", (TILE_SIZE, TILE_SIZE))
        return Image.open(io.BytesIO(tile_data))

    def _draw_lines(self, image, zoom, start_x, start_y):
        coords = (
            to_web_mercator(point.latitude, point.longitude, zoom)
            for point in self.track.walk(only_points=True)
        )
        coords = [(x - start_x, y - start_y) for x, y in coords]

        draw = ImageDraw.Draw(image)
        draw.line(coords, fill=self.color, width=self.line_width, joint="curve")


def render(track: GPX, layer: TileLayerConfig, requester: TileRequester) -> Image.Image:
    """Shorthand to construct a :class:`TrackMapRenderer` and render the preview.

    :param track: Parsed track to render.
    :param layer: The tile layer to take the map tiles from.
    :param requester: The requester which will be used to request the tiles.
    :return: The image containing the rendered preview.
    """
    return TrackMapRenderer(track, requester, (300, 300), layer).render()


__all__ = ["to_web_mercator", "TrackMapRenderer", "render"]
