import folium
import pandas as pd
from folium.plugins import MarkerCluster


def create_map(cities_df: pd.DataFrame, best_edges: list | None = None):
    # folium Map の作成
    jp_map = folium.Map(
        location=[37.0902, 138.2529],  # 任意の中心地点（日本付近）
        zoom_start=3,
        tiles="OpenStreetMap",
        attr="Map tiles by Stamen Design",
    )
    marker_cluster = MarkerCluster().add_to(jp_map)

    # 都市のマーカーを配置
    for idx, row in cities_df.iterrows():
        folium.Marker(
            location=[row["緯度"], row["経度"]],
            popup=f"{row['都市名']} (Order: {row.get('visit_order', 'N/A')})",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(marker_cluster)

    if best_edges:
        # best_edges の各 (start, end) ペアに対して線を引く
        for start, end in best_edges:
            i_start = start - 1
            i_end = end - 1

            lat1, lon1 = cities_df.loc[i_start, ["緯度", "経度"]]
            lat2, lon2 = cities_df.loc[i_end, ["緯度", "経度"]]

            # それぞれの edge を個別の PolyLine として描画
            folium.PolyLine(
                locations=[[lat1, lon1], [lat2, lon2]],
                color="blue",
                weight=2.5,
                opacity=1,
            ).add_to(jp_map)

    return jp_map
