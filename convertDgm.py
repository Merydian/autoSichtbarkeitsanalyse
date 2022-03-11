
class convert:
    def __init__(self, name, dir):
        self.name = name
        self.crs = 32632
        self.dir = dir 
        self.dgmPath = self.dir + name + '/dgm/'
        self.domPath = self.dir + name + '/dom/'

        self.Convert_to_tif(self.dgmPath)
        self.merge(self.dgmPath)
        self.clip_raster(self.dgmPath)

        self.Convert_to_tif(self.domPath)
        self.merge(self.domPath)
        self.clip_raster(self.domPath)

    def Convert_to_tif(self, path):
        files = []
        for file in os.listdir(path):
            if file.endswith(".xyz"):
                name = path + file
                files.append(os.path.join(name))
        print(files)

        for file in files:
            # load layer
            name = file.split('/')[7]

            iface.addRasterLayer(file, name, "gdal")
            rlayer = QgsProject.instance().mapLayersByName(name)[0]

            crs = QgsCoordinateReferenceSystem()
            crs.createFromId(self.crs)
            rlayer.setCrs(crs)

            # export layer
            tif = file.replace('xyz', 'tif')

            file_writer = QgsRasterFileWriter(tif)
            pipe = QgsRasterPipe()
            provider = rlayer.dataProvider()

            print(provider.crs())

            if not pipe.set(provider.clone()):
                print("Cannot set pipe provider")
                continue

            file_writer.writeRaster(
                pipe,
                provider.xSize(),
                provider.ySize(),
                provider.extent(),
                crs)

            qinst = QgsProject.instance()
            qinst.removeMapLayer(qinst.mapLayersByName(name)[0].id())

    def merge(self, path):
        outPath = path + "merge.tiff"

        files = []
        for file in os.listdir(path):
            if file.endswith(".tif"):
                name = path + file
                files.append(os.path.join(name))
        print(files)

        result = processing.run("gdal:merge",
                                {'DATA_TYPE': 5,
                                 'EXTRA': '',
                                 'INPUT': files,
                                 'NODATA_INPUT': None,
                                 'NODATA_OUTPUT': None,
                                 'OPTIONS': '',
                                 'OUTPUT': outPath,
                                 'PCT': False,
                                 'SEPARATE': False})

    def clip_raster(self, path):
        outPath = path + "merge.tiff"

        rclipOut = path + '/rclip.tif'
        processing.run("gdal:cliprasterbymasklayer",
                       {'ALPHA_BAND': False,
                        'CROP_TO_CUTLINE': True,
                        'DATA_TYPE': 0,
                        'EXTRA': '',
                        'INPUT': outPath,
                        'KEEP_RESOLUTION': False,
                        'MASK': self.dir + self.name + '/vector/buffer.shp',
                        'MULTITHREADING': False,
                        'NODATA': None,
                        'OPTIONS': '',
                        'OUTPUT': rclipOut,
                        'SET_RESOLUTION': False,
                        'SOURCE_CRS': None,
                        'TARGET_CRS': None,
                        'X_RESOLUTION': None,
                        'Y_RESOLUTION': None})


x = convert('Caro', 'C:/Users/T/Documents/GitHub/autoSichtbarkeitsanalyse/')

