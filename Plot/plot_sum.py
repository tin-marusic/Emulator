import matplotlib.pyplot as plt
import os
import json
from shapely.geometry import shape
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize

#os.chdir("Plot")
coord = [[[],[]],[[],[]]] #za svaku dimeziju(E i H) - u prvi element spremamo koordinate,u drugi sume
files = [["out_eta_E.txt","out_phi_E.txt","out_sum_E.txt"],["out_eta_H.txt","out_phi_H.txt","out_sum_H.txt",]]
imena = ["E","H"]

for i in range(2):
    j = 0
    brojac = 0
    for file in files[i]:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                coord[i][j].append(float(line.strip("\n")))
        brojac += 1
        if brojac > 1:
            j += 1 

    #slazemo parove x,y koordinata
                
    a = coord[i][0][:len(coord[i][0])//2] #buduci da je prva polovica niza eta koord, a druga phi
    b = coord[i][0][len(coord[i][0])//2:]
    c = []
    for j in range(len(a)): 
        c.append(a[j])
        c.append(b[j])
        
    coord[i][0] = [c[k:k+2] for k in range(0, len(c), 2)] 


def plot_bins_from_geojson(geojson_file, output_dir,part = 0): #part - dio detektora, funkcija prima 0 za E ili 1 za H 
        # Read GeoJSON file
        with open(geojson_file, 'r') as f:
            data = json.load(f)
        
        # Dictionary to store bins grouped by layer
        layer_bins = {}
        
        # Iterate over each feature in the GeoJSON file
        for feature in data['features']:
            layer = feature['properties']['Layer']
            geometry = shape(feature['geometry'])  # Convert GeoJSON geometry to Shapely geometry
            
            # Add the geometry to the corresponding layer
            if layer not in layer_bins:
                layer_bins[layer] = [geometry]
            else:
                layer_bins[layer].append(geometry)
        
        bins = layer_bins.get(50, []) #crtamo za 50ti layer
        
        # Plot bins
        if bins:
                cmap = plt.cm.viridis
                norm = plt.Normalize(vmin=0, vmax=max(coord[part][1]))
                colorbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
                colorbar.set_array([])
                fig = plt.figure(figsize=(8, 6))
                i = 1
                eta = 19
                phi = 53
                for idx, bin_geometry in enumerate(bins):
                    if [eta,phi] in coord[part][0]:
                        indeks = coord[part][0].index([eta,phi])
                        plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(coord[part][1][indeks]))
                    else:
                        plt.plot(*bin_geometry.exterior.xy, color='black', linewidth=0.5)
                    plt.gca().set_aspect('equal', adjustable='datalim')

                    #jednostavni algoritam koji prati koordinatu koju se trenutno crta
                    i += 1
                    eta -= 1
                    if eta < 0:
                        phi -= 1
                        eta = 19
                        if phi < 0:
                            phi = 71

                for i in range(10, 251, 10):  # Start from 10 cm to 250 cm, increment by 10
                    plt.plot([-1, 1], [i, i], color='black', linewidth=0.5) 
                if part == 0:
                    plt.title(f'Suma outputa 14 Stage-1 FPG --- E data')
                else:
                    plt.title(f'Suma outputa 14 Stage-1 FPG --- H data')
                plt.xlabel('X Position')
                plt.ylabel('Y Position')
                plt.grid(True)
                
                # Save the plot as a PNG file
                output_file = os.path.join(output_dir, f'sum_output_stage1_{part}.png')
                print(output_file)
                plt.savefig(output_file)
                plt.close() 
                add_colorbar("out",max(coord[part][1])) #dodajemo colorbar na sve slike koje se nalaze u mapi out

def add_colorbar(path,color_max):

    # Iteracija kroz slike u mapi A
    for filename in os.listdir(path):
        if filename.endswith(".png") and "_colorbar" not in filename: #Provjera ekstenzije slike te da vec nema colorbar
            # Učitavanje slike iz mape A
            img = plt.imread(os.path.join(path, filename))

            # Stvaranje subplota
            fig, ax = plt.subplots(figsize=(15, 10))

            # Prikaz slike na lijevoj strani
            ax.imshow(img)
            ax.axis('off')  # Isključivanje oznaka osi

            # Stvaranje colorbara na desnoj strani
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.04 )  # Promijenite veličinu colorbara ovdje

            # Postavljanje normiranja za colorbar
            norm = Normalize(vmin=0, vmax=color_max)  # Pretpostavljamo da su vrijednosti piksela u rasponu od 0 do 255

            # Dodavanje colorbara
            cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='viridis'), cax=cax,fraction=0.046, aspect=1)
            cbar.set_label('Vrijednosti sume')

            # Spremanje subplota u mapu B
            filename = filename.replace(".png", "")
            plt.savefig(os.path.join(path, filename + '_colorbar.png'), bbox_inches='tight')
            
            # Zatvaranje subplota
            plt.close() 
            
plot_bins_from_geojson("towers_bins_only_vertices.geojson","out",0)
plot_bins_from_geojson("towers_bins_only_vertices.geojson","out",1)