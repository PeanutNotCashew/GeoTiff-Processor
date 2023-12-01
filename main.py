# Imports
import fiona
import numpy.ma as ma
import rasterio
import rasterio.mask

# Init lists and dict
shapes = []
NTAs = []
final = {}

# File paths
ntaFile = 'Data/2010 NTAs/ntas.shp'
tifFile = "Data/temp_deviation.tif"
outputFile = "stats.csv"

# File processing
def processStats():
  # Get NTA shapes/geometries and names
  with fiona.open(ntaFile, 'r') as shapefile:
    for feature in shapefile:
      shapes.append(feature["geometry"])
      NTAs.append(feature.properties["ntacode"])

  # Iterate through shapes to get stats for each NTA
  i = 0
  for feature in shapes:
    current = [feature]
    with rasterio.open(tifFile) as src:
      # Clip
      out_image, out_transform = rasterio.mask.mask(src, current, nodata=10, filled=False, crop=True)
      # Get stats
      average = ma.average(out_image)
      median = ma.median(out_image)
      sum = ma.sum(out_image)

    # Add to dictionary
    final[NTAs[i]] = (average, median, sum)
    i += 1

# Writes "final" dict to output file
def writeToOutput():
	# Writes headers
	with open(outputFile, 'w') as output:
		output.write('"ntacode","mean","median","sum"')

	# Writes individual
	for key in final:
		appendStr = '\n"{}",{},{},{}'.format(key, final[key][0], final[key][1], final[key][2])
		with open(outputFile, 'a') as output:
			output.write(appendStr)

processStats()
writeToOutput()
print("finished")