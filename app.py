import duckdb
import geopandas as gpd
import pandas as pd
import shapely
from pathlib import Path
from lonboard import Map, ScatterplotLayer
from flask import Flask, render_template

# Créer l'application Flask
app = Flask(__name__)

# Charger le fichier GeoParquet avec DuckDB


# Connexion à DuckDB et installer l'extension spatiale
con = duckdb.connect()
duckdb.install_extension("spatial", connection=con)
duckdb.load_extension("spatial", connection=con)

# Créer la table dans DuckDB
sql = """
CREATE TABLE IF NOT EXISTS  rides AS
SELECT *
FROM 'internet-speeds1.parquet'
"""
con.execute(sql)

# Créer la couche ScatterplotLayer
layer = ScatterplotLayer.from_duckdb(con.table("rides"), con)

# Créer la carte avec le layer
m = Map(layers=[layer])

# Route Flask pour afficher la carte et le bouton
@app.route("/")
def index():
    # Passer le HTML de la carte générée dans le modèle Flask
    map_html = m.to_html()  # Génère directement la carte en HTML
    return render_template("index.html", map_html=map_html)

# Lancer le serveur Flask
if __name__ == "__main__":
    app.run(debug=True)
