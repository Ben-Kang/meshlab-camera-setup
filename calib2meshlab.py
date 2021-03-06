import sys

if len(sys.argv) != 5:
  print "Wrong number of input parameter!"
  print "Usage: " + sys.argv[0] + " <meshFileName> <calibrationFileName> <imageListFileName> <outputSceneFileName.mlp>"
  exit()

# Reading input arguments
meshName = sys.argv[1]
inName = sys.argv[2]
imageList = sys.argv[3]
outName = sys.argv[4]


outFile = open(outName, "w")
inFile = open(inName, "r")
imageListFile = open(imageList, "r")

# First line indicates number of cameras and image resolutions
line = inFile.readline().split()
numCam = int(line[0])

# Now we read the image list file with the name of every image
imageNames = []
for imageline in imageListFile:
  imageline = imageline.rstrip("\n")
  imageNames.append(imageline)

#
allMatrices = []


# We read the camera content for each line
for i in range(1, numCam+1):
  camMatrices = []
  line = inFile.readline().split()
  intrinsic = line[0:9]
  extrinsic = line[9:18]
  position = line[18:21]
  imWidth = int(line[21])
  imHeight = int(line[22])
  camMatrices.append(intrinsic)
  camMatrices.append(extrinsic)
  camMatrices.append(position)
  camMatrices.append(imWidth)
  camMatrices.append(imHeight)
  allMatrices.append(camMatrices)



# Meshlab header file
outFile.write("<!DOCTYPE MeshLabDocument>\n")
outFile.write("<MeshLabProject>\n")
outFile.write(" <MeshGroup>\n")
outFile.write("  <MLMesh label=\"%s\" filename=\"%s\">\n" % (meshName, meshName))
outFile.write("   <MLMatrix44>\n")
outFile.write("1 0 0 0 \n")
outFile.write("0 1 0 0 \n")
outFile.write("0 0 1 0 \n")
outFile.write("0 0 0 1 \n")
outFile.write("</MLMatrix44>\n")
outFile.write("  </MLMesh>\n")
outFile.write(" </MeshGroup>\n")

# Raster group starts
outFile.write(" <RasterGroup>\n")

for i in range(0, numCam):
  outFile.write("  <MLRaster label=\"cam %d\">\n" % (i+1))
  pos = allMatrices[i][2]
  intr = allMatrices[i][0]
  extr = allMatrices[i][1]
  wid = allMatrices[i][3]
  hei = allMatrices[i][4]
  imName = imageNames[i]

  # Position of the camera is inversed
  outFile.write("   <VCGCamera TranslationVector=\"%.16e %.16e %.16e\"" % (-float(pos[0]), -float(pos[1]), -float(pos[2])))
  outFile.write(" LensDistortion=\"0 0\" ViewportPx=\"%d %d\" PixelSizeMm=\"1 1\"" % (wid, hei))
  centerX = float(intr[2])
  centerY = float(hei) - float(intr[5])
  focal = float(intr[0])
  outFile.write(" CenterPx=\"%d %d\" FocalMm=\"%.16e\"" % (int(centerX), int(centerY), focal))
  # The rotation matrix is all inversed except for the first vector
  outFile.write(" RotationMatrix=\"%.16e %.16e %.16e 0 %.16e %.16e %.16e 0 %.16e %.16e %.16e 0 0 0 0 1\"/>\n" % (float(extr[0]), float(extr[1]), float(extr[2]), -float(extr[3]), -float(extr[4]), -float(extr[5]), -float(extr[6]), -float(extr[7]), -float(extr[8])))
  outFile.write("   <Plane semantic=\"\" fileName=\"%s\"/>\n" % (imName))
  outFile.write("  </MLRaster>\n\n")


outFile.write(" </RasterGroup>\n")
outFile.write("</MeshLabProject>\n")


outFile.close()
inFile.close()
imageListFile.close()
