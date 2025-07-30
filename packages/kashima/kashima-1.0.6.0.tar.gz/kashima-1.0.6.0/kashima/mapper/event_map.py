import folium
import pandas as pd
import math
import logging
import html
import branca
import matplotlib.pyplot as plt
import os  # ← NEW (needed in load_data)

from .usgs_catalog import load_usgs_csv  # ← replace previous load_usgs import
from .isc_catalog import load_isc

import geopandas as gpd
from geopy.distance import geodesic
from folium import plugins
from folium.plugins import MarkerCluster

from .config import (
    MapConfig,
    EventConfig,
    FaultConfig,
    StationConfig,
    TILE_LAYER_CONFIGS,
)

# ── 1.  imports  ────────────────────────────────────────────────────
from .utils import (
    load_faults,
    load_stations_csv,
    calculate_distances_vectorized,
    great_circle_bbox,  # (already present)
    stream_read_csv_bbox,  # (already present)
)

logger = logging.getLogger(__name__)


class EventMap:
    """
    See original docstring.
    """

    def __init__(
        self,
        map_config: MapConfig,
        event_config: EventConfig,
        events_csv: str,
        legend_csv: str = None,
        x_col: str = None,
        y_col: str = None,
        location_crs: str = "EPSG:4326",
        mandatory_mag_col: str = "mag",
        calculate_distance: bool = True,
        fault_config: FaultConfig = None,
        station_config: StationConfig = None,
        show_distance_in_tooltip: bool = True,
        log_level=logging.INFO,
        url_col: str = "url",
        tooltip_fields=None,
        isc_csv: str | None = None,  # ← NEW PARAM, default None
    ):
        logger.setLevel(log_level)
        self.map_config = map_config
        self.event_config = event_config
        self.fault_config = fault_config
        self.station_config = station_config

        self.events_csv = events_csv
        self.isc_csv = isc_csv  # ← NEW
        self.legend_csv = legend_csv
        self.x_col = x_col
        self.y_col = y_col
        self.location_crs = location_crs
        self.mandatory_mag_col = mandatory_mag_col
        self.calculate_distance = calculate_distance
        self.show_distance_in_tooltip = show_distance_in_tooltip
        self.url_col = url_col

        # NEW: tooltip fields (default: ['place'])
        self.tooltip_fields = (
            tooltip_fields if tooltip_fields is not None else ["place"]
        )

        # Data
        self.events_df = pd.DataFrame()
        self.legend_df = pd.DataFrame()
        self.stations_df = pd.DataFrame()
        self.faults_gdf = None

        # Folium objects
        self.map_object = None
        self.marker_group = None
        self.color_map = None

        # bounding box or bounds, etc.
        self.bounds = None

    def load_data(self):
        """Load catalogues, apply bbox filter, distances, mag filters."""

        # -------------------------------------------------- 1. BBox ---
        bbox = great_circle_bbox(
            self.map_config.longitude,  # lon first
            self.map_config.latitude,
            self.map_config.radius_km
            * (self.event_config.event_radius_multiplier or 1.0),
        )
        min_lon, max_lon, min_lat, max_lat = bbox

        def in_bbox(df):
            """Boolean mask inside bbox (handles dateline)."""
            if min_lon <= max_lon:
                m_lon = df["longitude"].between(min_lon, max_lon, inclusive="both")
            else:  # crosses 180°
                m_lon = (df["longitude"] >= min_lon) | (df["longitude"] <= max_lon)
            m_lat = df["latitude"].between(min_lat, max_lat, inclusive="both")
            return m_lon & m_lat

        # ------------------------------------------- 2.  Read catalogues
        frames = []

        # → USGS (streamed)
        if self.events_csv and os.path.exists(self.events_csv):
            try:
                usgs_df = stream_read_csv_bbox(self.events_csv, bbox=bbox)
                frames.append(usgs_df)
                logger.info("Loaded %d USGS events inside bbox", len(usgs_df))
            except Exception as e:
                logger.error("Could not read USGS CSV '%s': %s", self.events_csv, e)

        # → ISC (may *not* support bbox arg, so read then trim)
        if self.isc_csv and os.path.exists(self.isc_csv):
            try:
                # call defensively: some versions take bbox, some don't
                try:
                    isc_df = load_isc(self.isc_csv, bbox=bbox)
                except TypeError:
                    isc_df = load_isc(self.isc_csv)
                    isc_df = isc_df[in_bbox(isc_df)]
                frames.append(isc_df)
                logger.info("Loaded %d ISC events inside bbox", len(isc_df))
            except Exception as e:
                logger.error("Could not read ISC CSV '%s': %s", self.isc_csv, e)

        if not frames:
            logger.error("No catalogue data could be loaded – aborting.")
            return

        self.events_df = pd.concat(frames, ignore_index=True)

        # --------------------------------------- 3.  Down‑stream logic —
        self._load_legend()
        self._convert_xy_to_latlon_if_needed()

        if self.mandatory_mag_col not in self.events_df.columns:
            logger.error(
                "Mandatory magnitude column '%s' missing.", self.mandatory_mag_col
            )
            return
        self.events_df[self.mandatory_mag_col] = pd.to_numeric(
            self.events_df[self.mandatory_mag_col], errors="coerce"
        ).astype("float32")
        self.events_df.dropna(subset=[self.mandatory_mag_col], inplace=True)

        if self.calculate_distance:
            logger.info("Calculating Repi distances (Haversine) from site.")
            self._compute_distances()
            dist_lim = self.map_config.radius_km * (
                self.event_config.event_radius_multiplier or 1.0
            )
            before = len(self.events_df)
            self.events_df = self.events_df[self.events_df["Repi"] <= dist_lim]
            logger.info(
                "Distance filter removed %d events; %d remain ≤ %.0f km",
                before - len(self.events_df),
                len(self.events_df),
                dist_lim,
            )

        # magnitude filters (unchanged)
        if self.event_config.vmin is not None:
            self.events_df = self.events_df[
                self.events_df[self.mandatory_mag_col] >= self.event_config.vmin
            ]
        if self.event_config.vmax is not None:
            self.events_df = self.events_df[
                self.events_df[self.mandatory_mag_col] <= self.event_config.vmax
            ]

        self._build_colormap()
        if self.fault_config and self.fault_config.include_faults:
            self._load_faults()
        if self.station_config and self.station_config.station_file_path:
            self._load_stations()
        self._compute_combined_bounds()

    def _load_legend(self):
        if not self.legend_csv:
            logger.info("No legend.csv provided. Will show default tooltips only.")
            return
        try:
            self.legend_df = pd.read_csv(self.legend_csv)
            logger.info(
                f"Loaded legend from '{self.legend_csv}'. Fields: {list(self.legend_df['Field'])}"
            )
        except Exception as e:
            logger.warning(
                f"Could not load legend_csv='{self.legend_csv}': {e}. Using empty legend."
            )
            self.legend_df = pd.DataFrame()

    def _convert_xy_to_latlon_if_needed(self):
        has_latlon = ("latitude" in self.events_df.columns) and (
            "longitude" in self.events_df.columns
        )
        has_xy = (self.x_col is not None) and (self.y_col is not None)
        if not has_latlon and has_xy:
            logger.info(
                f"Converting {self.x_col},{self.y_col} from '{self.location_crs}' to EPSG:4326."
            )
            from pyproj import Transformer

            transformer = Transformer.from_crs(
                self.location_crs, "EPSG:4326", always_xy=True
            )
            xs = self.events_df[self.x_col].values
            ys = self.events_df[self.y_col].values
            lon, lat = transformer.transform(xs, ys)
            self.events_df["longitude"] = lon
            self.events_df["latitude"] = lat

        self.events_df.dropna(subset=["latitude", "longitude"], inplace=True)

    def _compute_distances(self):
        calculate_distances_vectorized(
            events_df=self.events_df,
            center_lat=self.map_config.latitude,
            center_lon=self.map_config.longitude,
            lat_col="latitude",
            lon_col="longitude",
            out_col="Repi",
        )

    def _build_colormap(self):
        if self.events_df.empty:
            logger.warning("No events left; skipping color map.")
            return
        vmin = self.event_config.vmin
        vmax = self.event_config.vmax
        mags = self.events_df[self.mandatory_mag_col]
        data_min, data_max = mags.min(), mags.max()

        if vmin is None:
            vmin = math.floor(data_min * 2) / 2.0
        if vmax is None:
            vmax = math.ceil(data_max * 2) / 2.0

        logger.info(
            f"Building color map from {vmin} to {vmax}, reversed={self.event_config.color_reversed}."
        )

        cmap = plt.get_cmap(self.event_config.color_palette)
        if self.event_config.color_reversed:
            cmap = cmap.reversed()

        color_list = [cmap(i / cmap.N) for i in range(cmap.N)]
        self.color_map = branca.colormap.LinearColormap(
            colors=color_list, vmin=vmin, vmax=vmax
        )
        self.color_map.caption = self.event_config.legend_title or "Magnitude"

    def _load_faults(self):
        logger.info(f"Loading faults from {self.fault_config.faults_gem_file_path}...")
        try:
            gdf = load_faults(
                self.fault_config.faults_gem_file_path,
                self.fault_config.coordinate_system,
            )
        except Exception as e:
            logger.error(f"Failed to load faults: {e}")
            return

        if not gdf.is_valid.all():
            logger.warning("Some fault geometries invalid; removing them.")
            gdf = gdf[gdf.is_valid]

        self.faults_gdf = gdf
        logger.info(f"Faults loaded. Found {len(gdf)} features.")

    def _load_stations(self):
        logger.info(f"Loading stations from {self.station_config.station_file_path}...")
        try:
            df = load_stations_csv(
                self.station_config.station_file_path,
                self.station_config.coordinate_system,
            )
        except Exception as e:
            logger.error(f"Failed to load stations: {e}")
            return
        self.stations_df = df
        logger.info(f"Stations loaded. Found {len(self.stations_df)} stations.")

    def _compute_combined_bounds(self):
        lat_c = self.map_config.latitude
        lon_c = self.map_config.longitude
        multiplier = self.event_config.event_radius_multiplier or 1.0
        dist_km = self.map_config.radius_km * multiplier

        d_lat = dist_km / 111.0
        cos_lat = math.cos(math.radians(lat_c))
        if abs(cos_lat) < 1e-6:
            cos_lat = 1e-6
        d_lon = dist_km / (111.0 * cos_lat)

        box_min_lat = lat_c - d_lat
        box_max_lat = lat_c + d_lat
        box_min_lon = lon_c - d_lon
        box_max_lon = lon_c + d_lon

        all_lats = [box_min_lat, box_max_lat]
        all_lons = [box_min_lon, box_max_lon]

        if not self.events_df.empty:
            all_lats.extend(self.events_df["latitude"].values.tolist())
            all_lons.extend(self.events_df["longitude"].values.tolist())
        if not self.stations_df.empty:
            all_lats.extend(self.stations_df["latitude"].values.tolist())
            all_lons.extend(self.stations_df["longitude"].values.tolist())

        min_lat, max_lat = min(all_lats), max(all_lats)
        min_lon, max_lon = min(all_lons), max(all_lons)

        self.bounds = [[min_lat, min_lon], [max_lat, max_lon]]
        logger.info(
            f"Combined bounds: lat=({min_lat}, {max_lat}), lon=({min_lon}, {max_lon})."
        )

    def get_map(self):
        self._initialize_map()
        self.marker_group = folium.FeatureGroup(name="Events")

        self._add_epicentral_distance_layer()
        self._add_event_markers()
        self._add_marker_cluster_layer()
        self._add_heatmap_layer()

        if self.faults_gdf is not None and not self.faults_gdf.empty:
            self._add_faults()
        if not self.stations_df.empty:
            self._add_stations()

        self._add_site_marker()
        self._add_tile_layers()
        self._add_layer_control()
        self._add_fullscreen_button()
        self._add_color_legend()

        # Only auto‑fit if user asked for it
        if self.map_config.auto_fit_bounds:
            self._fit_bounds()

        return self.map_object

    # ── 4.  _initialize_map()  – support lock_pan flag ─────────────────
    def _initialize_map(self):
        cfg = self.map_config
        tile_cfg = TILE_LAYER_CONFIGS[cfg.default_tile_layer]  # <─ NEW
        self.map_object = folium.Map(
            location=[cfg.latitude, cfg.longitude],
            zoom_start=cfg.base_zoom_level,
            min_zoom=cfg.min_zoom_level,
            max_zoom=cfg.max_zoom_level,
            tiles=tile_cfg["tiles"],  # <─ was .url
            attr=tile_cfg["attr"],  # <─ was .attribution
            control_scale=True,
            dragging=not getattr(cfg, "lock_pan", False),  # NEW
            max_bounds=getattr(cfg, "lock_pan", False),  # NEW
        )

    def _add_event_markers(self):
        """
        Add one CircleMarker per event with a short tooltip
        and a rich HTML popup.  Back‑ticks and HTML are escaped to avoid
        breaking the generated JavaScript.
        """
        import html  # local import to avoid global if not needed

        if self.events_df.empty:
            logger.warning("No events to plot.")
            return

        def _esc_js(s: str) -> str:
            """
            Escape back‑ticks, backslashes and newlines so the string
            can sit safely inside a JavaScript template literal.
            """
            return s.replace("\\", "\\\\").replace("`", "\\`").replace("\n", "\\n")

        self.marker_group = folium.FeatureGroup(
            name="Events",
            show=self.event_config.show_events_default,
        )

        legend_map = (
            {
                str(row["Field"]).strip(): str(row["Legend"]).strip()
                for _, row in self.legend_df.iterrows()
            }
            if not self.legend_df.empty
            else {}
        )

        for _, row in self.events_df.iterrows():
            # ----------------------------------------------------------------
            # 1) colour by magnitude
            # ----------------------------------------------------------------
            mag = row[self.mandatory_mag_col]
            colour = self.color_map(mag) if self.color_map else "blue"

            # ----------------------------------------------------------------
            # 2) tooltip (user‑selected fields)
            # ----------------------------------------------------------------
            tooltip_parts = [
                _esc_js(str(row.get(f, "")).strip())
                for f in self.tooltip_fields
                if pd.notnull(row.get(f, "")) and str(row.get(f, "")).strip()
            ]
            tooltip_text = " | ".join(tooltip_parts) if tooltip_parts else None

            # ----------------------------------------------------------------
            # 3) popup HTML
            # ----------------------------------------------------------------
            def add_line(label, value):
                return f"<b>{html.escape(label)}</b> {html.escape(value)}"

            lines = [
                add_line(
                    legend_map.get(self.mandatory_mag_col, "Magnitude:"), f"{mag:g}"
                ),
                add_line(
                    legend_map.get("latitude", "Latitude:"), f"{row['latitude']:.5f}"
                ),
                add_line(
                    legend_map.get("longitude", "Longitude:"), f"{row['longitude']:.5f}"
                ),
            ]

            if self.show_distance_in_tooltip and "Repi" in row:
                lines.append(add_line("Distance:", f"{row['Repi']:.1f} km"))

            # any other legend fields
            for field, label in legend_map.items():
                if field in (self.mandatory_mag_col, "latitude", "longitude"):
                    continue
                if field in row and pd.notnull(row[field]):
                    val = str(row[field]).strip()
                    if val.startswith(("http://", "https://")):
                        val = f'<a href="{html.escape(val)}" target="_blank">link</a>'
                    lines.append(add_line(label, val))

            popup_html = "<br>".join(lines)
            popup_obj = folium.Popup(popup_html, max_width=300)

            # ----------------------------------------------------------------
            # 4) add marker
            # ----------------------------------------------------------------
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=4,
                color=colour,
                fill=True,
                fill_opacity=0.7,
                tooltip=tooltip_text,
                popup=popup_obj,
            ).add_to(self.marker_group)

        self.marker_group.add_to(self.map_object)

    def _add_marker_cluster_layer(self):
        if self.events_df.empty:
            logger.warning("No events to cluster.")
            return

        clus = MarkerCluster(
            name="Marker Cluster",
            show=self.event_config.show_cluster_default,
        )
        for _, row in self.events_df.iterrows():
            tip = f"Mag: {row[self.mandatory_mag_col]:.2f}"
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                tooltip=tip,
            ).add_to(clus)

        clus.add_to(self.map_object)

    def _add_heatmap_layer(self):
        if self.events_df.empty:
            logger.warning("No events for heatmap.")
            return

        data = [
            (r["latitude"], r["longitude"], r[self.mandatory_mag_col])
            for _, r in self.events_df.iterrows()
        ]
        fg = folium.FeatureGroup(
            name="Heatmap",
            show=self.event_config.show_heatmap_default,
        )
        heat = plugins.HeatMap(
            data,
            min_opacity=self.event_config.heatmap_min_opacity,
            max_zoom=self.map_config.max_zoom_level,
            radius=self.event_config.heatmap_radius,
            blur=self.event_config.heatmap_blur,
        )
        fg.add_child(heat)
        fg.add_to(self.map_object)

    def _add_site_marker(self):
        popup_html = f"""
        <b>Site Project:</b> {self.map_config.project_name}<br>
        <b>Client:</b> {self.map_config.client}
        """
        folium.Marker(
            location=[self.map_config.latitude, self.map_config.longitude],
            icon=folium.Icon(color="red", icon="star", prefix="fa"),
            tooltip=self.map_config.project_name,
            popup=folium.Popup(popup_html, max_width=300),
        ).add_to(self.map_object)

    def _add_tile_layers(self):
        for layer_name, cfg in TILE_LAYER_CONFIGS.items():
            if layer_name != self.map_config.default_tile_layer:
                folium.TileLayer(
                    tiles=cfg["tiles"],
                    name=layer_name,
                    attr=cfg["attr"],
                    control=True,
                    max_zoom=self.map_config.max_zoom_level,
                    min_zoom=self.map_config.min_zoom_level,
                ).add_to(self.map_object)

        default_cfg = TILE_LAYER_CONFIGS[self.map_config.default_tile_layer]
        folium.TileLayer(
            tiles=default_cfg["tiles"],
            name=self.map_config.default_tile_layer,
            attr=default_cfg["attr"],
            control=True,
            max_zoom=self.map_config.max_zoom_level,
            min_zoom=self.map_config.min_zoom_level,
        ).add_to(self.map_object)

    def _add_layer_control(self):
        folium.LayerControl().add_to(self.map_object)

    def _add_fullscreen_button(self):
        plugins.Fullscreen(
            position="topleft",
            title="Full Screen",
            title_cancel="Exit Full Screen",
            force_separate_button=True,
        ).add_to(self.map_object)

    def _add_color_legend(self):
        if self.color_map is not None:
            self.color_map.position = self.event_config.legend_position.lower()
            self.color_map.add_to(self.map_object)
            logger.info("Color legend added to the map.")
        else:
            logger.info("No color map to add.")

    def _add_faults(self):
        logger.info("Adding fault lines to the map...")
        if self.faults_gdf is None or self.faults_gdf.empty:
            logger.warning("No fault lines to display.")
            return

        style_func = lambda x: {
            "color": self.fault_config.regional_faults_color,
            "weight": self.fault_config.regional_faults_weight,
            "opacity": 1.0,
        }
        fault_lyr = folium.GeoJson(
            data=self.faults_gdf, style_function=style_func, name="Faults", show=True
        )
        fault_lyr.add_to(self.map_object)
        logger.info("Fault lines layer added.")

    def _add_stations(self):
        logger.info("Adding stations to the map...")
        if self.stations_df.empty:
            logger.warning("No station data to display.")
            return

        stn_grp = folium.FeatureGroup(
            name=self.station_config.layer_title if self.station_config else "Stations",
            show=True,
        )
        icon_map = {
            1: {"color": "blue", "icon": "arrow-up", "prefix": "fa"},
            2: {"color": "green", "icon": "arrows-h", "prefix": "fa"},
            3: {"color": "red", "icon": "cube", "prefix": "fa"},
        }

        for _, row in self.stations_df.iterrows():
            lat_ = row["latitude"]
            lon_ = row["longitude"]
            axes_ = int(row.get("axes", 0))

            icon_conf = icon_map.get(
                axes_, {"color": "gray", "icon": "info-sign", "prefix": "fa"}
            )
            tip = (
                f"Station ID: {row.get('ID','?')}<br>"
                f"Type: {row.get('type','N/A')}<br>"
                f"Axes: {axes_}"
            )
            folium.Marker(
                location=[lat_, lon_],
                icon=folium.Icon(
                    color=icon_conf["color"],
                    icon=icon_conf["icon"],
                    prefix=icon_conf["prefix"],
                ),
                tooltip=tip,
            ).add_to(stn_grp)

        stn_grp.add_to(self.map_object)
        logger.info("Stations layer added.")

    def _fit_bounds(self):
        if not self.bounds:
            logger.warning("No bounding box available. Skipping fit_bounds.")
            return

        logger.info("Fitting map to combined bounds (site + events).")
        self.map_object.fit_bounds(self.bounds, padding=(10, 10))

    def _add_epicentral_distance_layer(self):
        circles = self.map_config.epicentral_circles
        if circles < self.map_config.MIN_EPICENTRAL_CIRCLES:
            circles = self.map_config.MIN_EPICENTRAL_CIRCLES
        if circles > self.map_config.MAX_EPICENTRAL_CIRCLES:
            circles = self.map_config.MAX_EPICENTRAL_CIRCLES
        if circles <= 0:
            return

        fg = folium.FeatureGroup(
            name=self.map_config.epicentral_circles_title,
            show=self.event_config.show_epicentral_circles_default,
        )

        interval_km = self.map_config.radius_km / circles
        for i in reversed(range(1, circles + 1)):
            dist_km = i * interval_km
            folium.Circle(
                location=[self.map_config.latitude, self.map_config.longitude],
                radius=dist_km * 1000,
                color="blue",
                weight=1,
                opacity=0.5,
                fill=True,
                fill_opacity=0.0,
                tooltip=f"{dist_km:.0f} km",
            ).add_to(fg)

        fg.add_to(self.map_object)
