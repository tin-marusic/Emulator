import matplotlib.pyplot as plt
import os
import json
from shapely.geometry import shape
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize

# os.chdir("Plot")
coords = [[[], []], [[], []]]  # for each dimension (E and H) - in the first element we store the coordinates, in the second the sums
files = [["out_eta_E.txt", "out_phi_E.txt", "out_sum_E.txt"], ["out_eta_H.txt", "out_phi_H.txt", "out_sum_H.txt"]]
names = ["E", "H"]

for i in range(2):
    j = 0
    counter = 0
    for file in files[i]:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                coords[i][j].append(float(line.strip("\n")))
        counter += 1
        if counter > 1:
            j += 1

    # create pairs of x, y coordinates
    a = coords[i][0][:len(coords[i][0]) // 2]  # since the first half of the array is eta coord, and the second is phi
    b = coords[i][0][len(coords[i][0]) // 2:]
    c = []
    for j in range(len(a)):
        c.append(a[j])
        c.append(b[j])

    coords[i][0] = [c[k:k + 2] for k in range(0, len(c), 2)]


def plot_bins_from_geojson(geojson_file, output_dir, part=0):  # part - part of the detector, function takes 0 for E or 1 for H
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
    choosen_layer = int(input("Choose ploting layer(1-50): "))
    bins = layer_bins.get(choosen_layer, [])  # draw for the 50th layer

    # Plot bins
    if bins:
        cmap = plt.cm.viridis
        norm = plt.Normalize(vmin=0, vmax=max(coords[part][1]))
        colorbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        colorbar.set_array([])
        fig = plt.figure(figsize=(8, 6))
        eta = 19  # starting coordinate for drawing
        phi = 53
        for idx, bin_geometry in enumerate(bins):
            if [eta, phi] in coords[part][0]:
                if coords[part][0].count([eta, phi]) > 1:
                    print(f"Overlap at coordinates {eta, phi}")
                index = coords[part][0].index([eta, phi])
                plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(coords[part][1][index]))
            else:
                plt.plot(*bin_geometry.exterior.xy, color='black', linewidth=0.5)
            plt.gca().set_aspect('equal', adjustable='datalim')

            # simple algorithm that follows the currently drawn coordinate
            eta -= 1
            if eta < 0:
                phi -= 1
                eta = 19
                if phi < 0:
                    phi = 71

        for i in range(10, 251, 10):  # Start from 10 cm to 250 cm, increment by 10
            plt.plot([-1, 1], [i, i], color='black', linewidth=0.5)
        if part == 0:
            plt.title(f'Sum of output 14 Stage-1 FPG --- E data')
        else:
            plt.title(f'Sum of output 14 Stage-1 FPG --- H data')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.grid(True)

        # Save the plot as a PNG file
        output_file = os.path.join(output_dir, f'sum_output_stage1_{part}.png')
        print(output_file)
        plt.savefig(output_file)
        plt.close()
        add_colorbar("out", max(coords[part][1]))  # add a colorbar to all images in the "out" folder


def add_colorbar(path, color_max):
    # Iteration through images in folder "out"
    for filename in os.listdir(path):
        if filename.endswith(".png") and "_colorbar" not in filename:  # Check the image extension and if it does not already have a colorbar
            # Load image from folder "out"
            img = plt.imread(os.path.join(path, filename))
            fig, ax = plt.subplots(figsize=(15, 10))
            ax.imshow(img)
            ax.axis('off')  # Turn off axis labels
            # Create colorbar on the right side
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.04)
            norm = Normalize(vmin=0, vmax=color_max)  # colorbar range

            cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='viridis'), cax=cax, fraction=0.046, aspect=1)
            cbar.set_label('Sum Values')
            filename_new = filename.replace(".png", "")
            plt.savefig(os.path.join(path, filename_new + '_colorbar.png'), bbox_inches='tight')

            plt.close()
            os.remove(os.path.join(path,filename))

plot_bins_from_geojson("towers_bins_only_vertices.geojson", "out", 0)
plot_bins_from_geojson("towers_bins_only_vertices.geojson", "out", 1)
