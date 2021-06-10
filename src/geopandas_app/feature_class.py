import pathlib
from abc import ABC, abstractmethod

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

from src.geopandas_app.config.config import CRS, FEATURE_CLASS_NAMES, CSV_COLUMNS_NAMES

class FeatureClass(ABC):
    """Feature class responsible for containing information about spatial data class.

    Attributes:
        name: name of the layer
        source_file: path of the source file (gdb or csv)
        geo_data_frame: geopandas data frame eg. gpd.GeoDataFrame(columns = FEATURE_CLASS_NAMES)
    """

    def __init__(self, name: str, source_file: pathlib.Path):
        self.name = name
        self.source_file = source_file
        self.geo_data_frame = self.read_from_file()

    def __repr__(self):
        return repr(self.geo_data_frame)

    def __str__(self):
        return str(self.geo_data_frame)

    @property
    def features_count(self):
        """Get pandas data frame feature count."""
        return len(self.geo_data_frame.index)

    @abstractmethod
    def read_from_file(self):
        pass


class CsvFeatureClass(FeatureClass):
    """Feature class for CSV input. Object is Data Frame after read_from_file,
    and Geo Data Frame after convert_data_frame_to_geo_data_frame."""

    def read_from_file(self):
        return pd.read_csv(self.source_file, usecols=CSV_COLUMNS_NAMES, sep=';')

    def filter_out_based_on_coordinates(self, value):
        '''delete rows that do not have global coordinates'''
        df = self.geo_data_frame
        self.geo_data_frame = self.geo_data_frame[(df["LLlat"] != value) &
                                                  (df["LLlon"] != value) &
                                                  (df["LRlat"] != value) &
                                                  (df["LRlon"] != value) &
                                                  (df["ULlat"] != value) &
                                                  (df["ULlon"] != value) &
                                                  (df["URlat"] != value) &
                                                  (df["URlon"] != value)]

    def filter_out_based_on_attributes(self):
        # select rows that have specified values
        df = self.geo_data_frame
        self.geo_data_frame = df.loc[(df["Column1"] == value)]


    def convert_data_frame_to_geo_data_frame(self):
        df = self.geo_data_frame
        df['allcoords'] = df.apply(lambda row: iter(
                                                    [float(row.LLlon),
                                                     float(row.LLlat),
                                                     float(row.LRlon),
                                                     float(row.LRlat),
                                                     float(row.URlon),
                                                     float(row.URlat),
                                                     float(row.ULlon),
                                                     float(row.ULlat)]), axis=1)
        df['geometry'] = df.apply(lambda row: Polygon(zip(row.allcoords, row.allcoords)), axis=1)
        del df['allcoords']
        self.geo_data_frame = gpd.GeoDataFrame(df, crs=CRS, geometry='geometry')

class GdbFeatureClass(FeatureClass):
    """Feature class for GDB input. Object is a Geo Data Frame after read_from_file."""
    def read_from_file(self):
        return gpd.read_file(self.source_file, driver='FileGDB', layer=self.name, bbox=None)

def run_geo_app(gdb_path,csv_path):
    gdb_path = pathlib.Path(gdb_path)
    csv_path = pathlib.Path(csv_path)
    if gdb_path.suffix == '.zip':
        gdb_path = unzip_file(gdb_path)
    if gdb_path.suffix == '.gdb':
        # for feature_class_name in FEATURE_CLASS_NAMES:
        for feature_class_name in FEATURE_CLASS_NAMES[0:1]:
            gdb_feature_class = GdbFeatureClass(feature_class_name, gdb_path)
            csv_feature_class = CsvFeatureClass(feature_class_name, csv_path)
            for value in [0, 9999]:
                csv_feature_class.filter_out_based_on_coordinates(value)
            csv_feature_class.filter_out_based_on_attributes()
            csv_feature_class.convert_data_frame_to_geo_data_frame()
            return f'csv_feature_class: {feature_class_name}, features number: {csv_feature_class.features_count}'

if __name__ == "__main__":
    #read
    from src.geopandas_app.utils.tools import unzip_file
    gdb_path = r""
    csv_path = r""
    gdb_path = pathlib.Path(gdb_path)
    csv_path = pathlib.Path(csv_path)
    if gdb_path.suffix == '.zip':
        gdb_path = unzip_file(gdb_path)
    if gdb_path.suffix == '.gdb':
        # for feature_class_name in FEATURE_CLASS_NAMES:
        for feature_class_name in FEATURE_CLASS_NAMES[0:1]:
            gdb_feature_class = GdbFeatureClass(feature_class_name, gdb_path)
            print(f'gdb_feature_class: {feature_class_name}, features number: {gdb_feature_class.features_count}')
            csv_feature_class = CsvFeatureClass(feature_class_name, csv_path)
            print(f'csv_feature_class: {feature_class_name}, features number: {csv_feature_class.features_count}')
            for value in [0, 9999]:
                csv_feature_class.filter_out_based_on_coordinates(value)
            print(f'csv_feature_class: {feature_class_name}, After coords filter,  features number: {csv_feature_class.features_count}')
            csv_feature_class.filter_out_based_on_attributes()
            print(f'csv_feature_class: {feature_class_name}, After fonts filter,  features number: {csv_feature_class.features_count}')
            print(type(csv_feature_class))
            csv_feature_class.convert_data_frame_to_geo_data_frame()
            print(type(csv_feature_class))