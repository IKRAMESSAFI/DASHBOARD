import streamlit as st
def app():
    import os
    from PIL import Image
    import geopandas as gpd
    import base64
    import imageio
    import folium
    import numpy as np
    import rasterio
    import matplotlib.cm as cm
    from branca.colormap import LinearColormap
    from streamlit_folium import folium_static, st_folium
    import time
    import requests
    from io import BytesIO

    # Function to read the GeoTIFF file with rasterio
    def download_file(url):
        response = requests.get(url)
        return BytesIO(response.content)

    def read_geotiff(url1):
        response1 = requests.get(url1)
        with rasterio.open(BytesIO(response1.content)) as dataset:
            return dataset.read(1)  # Assuming a single band GeoTIFF

    def display_loading_message():
        """Display a loading message while data is being loaded."""
        with st.spinner("Chargement des données en cours ... veuillez patienter un peu..."):
            # Simulate a loading delay
            time.sleep(20)

    # Fonction pour convertir une image en base64
    def image_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    # Charger les données depuis le fichier GeoParquet
    file_url = "https://ikramessafi.github.io/DATAPARQUET/DONNEE_MAROC.parquet"
    file_path = download_file(file_url)
    gdf = gpd.read_parquet(file_path)

    # Dictionnaire des fichiers GeoTIFF correspondant à chaque attribut
    raster_paths = {
        'Indice_Q': {
            '0': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Indice_Q_0.tif',
            '1': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Indice_Q_1.tif',
            '2': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Indice_Q_2.tif',
            '3': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Indice_Q_3.tif',
            '4': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Indice_Q_4.tif',
            '5': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Indice_Q_5.tif',
            '6': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Indice_Q_6.tif',
        },
        'Taux_occ_': {
            '0': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_occ_0.tif',
            '1': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_occ_1.tif',
            '2': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_occ_2.tif',
            '3': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_occ_3.tif',
            '4': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_occ_4.tif',
            '5': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_occ_5.tif',
            '6': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_occ_6.tif',
        },
        'Taux_plu_': {
            '0': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_plu_0.tif',
            '1': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_plu_1.tif',
            '2': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_plu_2.tif',
            '3': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_plu_3.tif',
            '4': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_plu_4.tif',
            '5': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_plu_5.tif',
            '6': 'https://kaoutar-elmouh.github.io/ikramraster/RASTERSS/Taux_plu_6.tif',
        },
    }

    # Sidebar pour la sélection de l'attribut
    selected_attribute = st.sidebar.selectbox("Sélectionnez l'attribut à visualiser", ['Indice_Q', 'Taux_occ_', 'Taux_plu_'])

    # Créer un graphique temporel avec Altair
    st.title(f" Timelapses permettant  de naviguer entre les différents jours de l'attribut {selected_attribute}")

    # Utiliser leafmap pour créer le timelapse
    # Utiliser leafmap pour créer le timelapse
    output_dir = "output_directory"
    # Check and create the directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output Directory: {output_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")

    output_gif_path = os.path.join(output_dir, f'output_timelapse_{selected_attribute}.gif')

    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output Directory: {output_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")

    output_gif_path = os.path.join(output_dir, f'output_timelapse_{selected_attribute}.gif')

    try:
        images = list(raster_paths[selected_attribute].values())

        # Create a list to store rasterio.DatasetReader objects
        raster_datasets = []

        for image_path in images:
            raster_data = read_geotiff(image_path)
            raster_datasets.append(raster_data)

        # Create a list to store PIL Image objects
        pil_images = []

        for raster_data in raster_datasets:
            pil_image = Image.fromarray(raster_data)
            new_size = (800, 960)
            resized_img = pil_image.resize(new_size, resample=Image.LANCZOS)
            pil_images.append(resized_img)

        # Save each resized frame as a static image
        for i, pil_image in enumerate(pil_images):
            frame_path = os.path.join(output_dir, f"frame_{i}.png")
            pil_image.save(frame_path)

        # Create GIF from resized static images
        gif_path = os.path.join(output_dir, f'output_timelapse_{selected_attribute}.gif')
        with imageio.get_writer(gif_path, mode='I', duration=1000, loop=0, palettesize=256) as writer:
            for frame_path in [f"frame_{i}.png" for i in range(len(pil_images))]:
                img = imageio.imread(os.path.join(output_dir, frame_path))
                resized_img = Image.fromarray(img).resize((800, 960), resample=Image.LANCZOS)
                writer.append_data(resized_img)


    except Exception as e:
        st.error(f"Erreur lors de la création du timelapse : {e}")
        st.stop()

    # Obtenir les limites (bounds) à partir des données GeoParquet
    bounds = [
        [gdf.bounds.miny.min(), gdf.bounds.minx.min()],
        [gdf.bounds.maxy.max(), gdf.bounds.maxx.max()]
    ]

    # Créer la carte Folium
    m = folium.Map(location=[31.5, -7], zoom_start=5, width=800, height=960)

    # Ajouter le calque GIF à la carte
    gif_layer = folium.raster_layers.ImageOverlay(
        gif_path,
        bounds=bounds,
        opacity=0.7,
        name='GIF Layer'
    ).add_to(m)

    # Ajouter le contrôle de calque à la carte
    folium.LayerControl().add_to(m)

    # Define vmin, vmax, and class_limits based on the selected attribute for URL1
    if selected_attribute == 'Indice_Q':
        vmin = 0
        vmax = 100
    elif selected_attribute == "Taux_occ_":
        vmin = 0
        vmax = 20
    else:
        vmin = 0
        vmax = 50

    class_limits = np.linspace(vmin, vmax, num=6)

    # Create a colormap with 6 equal intervals
    colormap = LinearColormap(
        colors=[cm.cividis(x) for x in np.linspace(0, 1, num=6)],
        index=np.linspace(vmin, vmax, num=6),
        vmin=vmin,
        vmax=vmax
    )
    m.add_child(colormap)

    # Afficher la carte
    folium_static(m, width=1200, height=700)
