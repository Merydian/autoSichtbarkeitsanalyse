class getGemeinden:
    def __init__(self, name, x, y, bufferDist):
        print('innit')
        self.name = name
        self.path = 'C:/Users/T/Documents/GitHub/autoSichtbarkeitsanalyse/' + name + '/'
        self.xy = [x, y]
        self.bufferDist = bufferDist
        self.point = None
        self.bufferOut = self.path + 'vector/buffer.shp'

    def makedir(self):
        print(self.path)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            print("Directory '%s' created" % self.name)

    def clip(self):
        clip = self.path + 'vector/clip.shp'

        result = processing.run("native:clip",
                                {
                                    'INPUT': 'C:/Users/T/Documents/GitHub/autoSichtbarkeitsanalyse/vg5000_ebenen_1231/VG5000_GEM.shp',
                                    'OUTPUT': clip,
                                    'OVERLAY': self.bufferOut})

        layer = QgsVectorLayer(clip, "clip", "ogr")

        list = [feature['GEN'] for feature in layer.getFeatures()]

        print([i.encode('latin-1').decode('utf-8') for i in list])

    def buffer_point(self):


        processing.run("native:buffer",
                       {'DISSOLVE': False,
                        'DISTANCE': self.bufferDist,
                        'END_CAP_STYLE': 0,
                        'INPUT': self.point,
                        'JOIN_STYLE': 0,
                        'MITER_LIMIT': 1,
                        'OUTPUT': self.bufferOut,
                        'SEGMENTS': 100})

    def create_point(self):
        x, y = self.xy

        vl = QgsVectorLayer("Point", "temp", "memory")

        crs = vl.crs()
        crs.createFromId(32632)
        vl.setCrs(crs)

        pr = vl.dataProvider()

        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
        pr.addFeature(f)
        vl.updateExtents()
        QgsProject.instance().addMapLayer(vl)

        self.point = vl.source()

        if not os.path.exists(self.path + '/vector'):
            os.mkdir(self.path + '/vector')
            print("Directory '%s' created" % self.path)

x = getGemeinden('try', 484260, 5584356, 1100)
x.makedir()
x.create_point()
x.buffer_point()
x.clip()