# Closest Points
A <a href="https://github.com/qgis/QGIS">QGIS</a>-plugin for extracting the closest points from one layer to another.

## Goal of the project
QGIS does not have a simple function to get the closest points from one layer to another layer, although PyQGIS provides such a function.
There are some workarounds for calculating the nearest points, but they are not very userfriendly.
This plugin provides the missing function with familiar, QGIS-standard interfaces. The functions of the plugin are also available via the processing framework and the toolbox.

## Usage
The plugin is available in the official plugin repository. After downloading and installing, it is located in the vector menu.
The plugin offers mutliple functions, which are described in the following paragraphs.
<img src="screenshots/vector_menu.png" width="100"/>

### Find closest point for each feature
This algorithm iterates over all features of one layer and calculates the closest point for each feature to a second layer.
Only one point per input feature will be calculated.

### Find all closest points for each feature
This algorithm iterates over all features of an input layer and calculates the closest points from this features to each feature of a second layer.
The count of the closest points will be the product of the feature counts of both layers.

### Output
The output will be a point layer and will has four columns:
1. id - a unique id field
2. from_fid - the fid of the feature to calculate the nearest point <b>from</b>
3. to_fid - the fid of the feature to calculate the nearest point <b>to</b>
4. distance - the shortest euclidean distance between the both features referenced by the fields <i>from_id</i> and <i>to_id</i>
<br>
The fields <i>from_id</i> and <i>to_id</i> can be used to create a join to the input layers.

## Remarks
The plugin calculates the euklidean distance, i.e. it is recommended to use metric coordinate systems.