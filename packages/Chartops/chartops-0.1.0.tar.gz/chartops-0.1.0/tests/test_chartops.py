#!/usr/bin/env python

"""Tests for `chartops` package."""


import unittest
import tempfile
from pathlib import Path

from chartops import chartops
from ipyleaflet import LayersControl, GeoJSON
import pandas as pd
import geopandas as gpd


class TestChartops(unittest.TestCase):
    """Tests for `chartops` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.map = chartops.Map()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_map_initial_state(self) -> None:
        self.assertEqual(len(self.map.layers), 1)

    def test_adding_a_basemap(self) -> None:
        self.map.add_basemap("Esri.WorldImagery")
        self.assertEqual(len(self.map.layers), 2)

    def test_adding_multiple_basemaps(self) -> None:
        self.map.add_basemap("Esri.WorldImagery")
        self.map.add_basemap("OpenTopoMap")
        self.assertEqual(len(self.map.layers), 3)

    def test_adding_an_invalid_basemap(self) -> None:
        with self.assertRaises(AttributeError):
            self.map.add_basemap("Invalid.BasemapName")

    def test_adding_layer_control(self) -> None:
        self.map.add_layer_control()
        control = self.map.controls[-1]
        self.assertIsInstance(control, LayersControl)

    def test_adding_different_position_in_layer_control(self) -> None:
        self.map.add_layer_control("topleft")
        control = self.map.controls[-1]
        position = getattr(control, "position")
        self.assertEqual(position, "topleft")

    def test_adding_invalid_position_in_layer_control(self) -> None:
        with self.assertRaises(ValueError):
            self.map.add_layer_control("invalid")

    def test_adding_layer_control_with_all_positions(self) -> None:
        positions = ["topright", "topleft", "bottomright", "bottomleft"]
        for position in positions:
            map_instance = chartops.Map()
            map_instance.add_layer_control(position)
            control = map_instance.controls[-1]
            self.assertIsInstance(control, LayersControl)
            self.assertEqual(getattr(control, "position"), position)

    def test_adding_a_vector_layer_from_a_url(self) -> None:
        self.map.add_vector(
            "https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/europe_110.geo.json"
        )
        layer = self.map.layers[-1]
        self.assertIsInstance(layer, GeoJSON)

    def test_adding_a_vector_layer_from_shapefile(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data = {
                "City": ["Tokyo", "New York", "London", "Paris"],
                "Latitude": [35.6895, 40.7128, 51.5074, 48.8566],
                "Longitude": [139.6917, -74.0060, -0.1278, 2.3522],
            }
            df = pd.DataFrame(data)
            gdf = gpd.GeoDataFrame(
                df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude)
            )
            shapefile_path = Path(temp_dir, "temp_shapefile.shp")
            gdf.to_file(shapefile_path)

            self.map.add_vector(shapefile_path)
            layer = self.map.layers[-1]
            self.assertIsInstance(layer, GeoJSON)

    def test_adding_a_vector_layer_from_geojson_file(self):
        from shapely.geometry import Point

        with tempfile.TemporaryDirectory() as temp_dir:
            gdf = gpd.GeoDataFrame(geometry=[Point(0, 0), Point(1, 1)], crs="EPSG:4326")
            geojson_path = Path(temp_dir, "temp.geojson")
            gdf.to_file(geojson_path, driver="GeoJSON")
            self.map.add_vector(geojson_path)
            layer = self.map.layers[-1]
            self.assertIsInstance(layer, GeoJSON)

    def test_adding_a_vector_layer_from_an_invalid_file(self):
        shapefile_path = Path("invalid_shapefile.shp")
        with self.assertRaises(FileNotFoundError):
            self.map.add_vector(shapefile_path)

    def test_adding_a_vector_layer_from_an_invalid_string(self):
        shapefile_path = "invalid_shapefile.shp"
        with self.assertRaises(ValueError):
            self.map.add_vector(shapefile_path)

    def test_adding_a_vector_layer_with_a_custom_color(self) -> None:
        self.map.add_vector(
            "https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/europe_110.geo.json",
            **{"color": "red"},
        )
        layer = self.map.layers[-1]
        print(layer.style)
        self.assertEqual(layer.style["color"], "red")

    def test_adding_a_vector_layer_with_custom_weight(self) -> None:
        self.map.add_vector(
            "https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/europe_110.geo.json",
            **{"weight": 5},
        )
        layer = self.map.layers[-1]
        self.assertEqual(layer.style["weight"], 5)

    def test_adding_a_vector_layer_with_custom_fillOpacity(self) -> None:
        self.map.add_vector(
            "https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/europe_110.geo.json",
            **{"fillOpacity": 0.5},
        )
        layer = self.map.layers[-1]
        self.assertEqual(layer.style["fillOpacity"], 0.5)

    def test_adding_a_vector_layer_with_invalid_color(self) -> None:
        with self.assertRaises(ValueError):
            self.map.add_vector(
                "https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/europe_110.geo.json",
                **{"color": 123},
            )

    def test_adding_a_vector_layer_with_invalid_weight(self) -> None:
        with self.assertRaises(ValueError):
            self.map.add_vector(
                "https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/europe_110.geo.json",
                **{"weight": "thick"},
            )

    def test_adding_a_vector_layer_with_invalid_fillOpacity(self) -> None:
        with self.assertRaises(ValueError):
            self.map.add_vector(
                "https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/europe_110.geo.json",
                **{"fillOpacity": 2},
            )
