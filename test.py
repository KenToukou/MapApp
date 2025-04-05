import pandas as pd
from geopy.distance import geodesic

from config.cities import cities
from service import CuttingPlaneTSMService, CVRPService, TravelingSalesmanService


def test_geopy_import():
    coord1 = (35.6895, 139.6917)  # 東京
    coord2 = (34.6937, 135.5023)  # 大阪
    distance = geodesic(coord1, coord2).kilometers
    print(f"東京と大阪の距離: {distance:.2f} km")


def examination():
    traveling_salesman_service = TravelingSalesmanService(base_df=cities)
    traveling_salesman_service.create_base_data()
    return traveling_salesman_service.optimize()


def cutting_plane():
    traveling_salesman_service = CuttingPlaneTSMService(base_df=cities)
    traveling_salesman_service.create_base_data()
    traveling_salesman_service.optimize()


def cvr_optimization():
    cities = pd.read_csv("./data/cities.csv")
    traveling_salesman_service = CVRPService(base_df=cities, m=1, Q=800)
    traveling_salesman_service.set_base_data()
    traveling_salesman_service.optimize()


if __name__ == "__main__":
    cvr_optimization()

# 53243.71701156
