import numpy as np


class Test:
    """
    """

    def __init__(self):
        print('Test from load_data module')


class Read:
    """
    """

    def __init__(self):
        self.data = None
        self.x = np.array([])
        self.y = np.array([])
        self.file_path = self.folder + '/' + self.fileName

    def read(self, text='', model=0):
        self.delimiter = ','
        if model[0:3] == 'chi':
            self.skiprows = self.search(text)
            if self.skiprows:
                self.data = np.loadtxt(self.file_path, delimiter=self.delimiter,
                                       skiprows=self.skiprows)
                self.x = self.data[:, 0]
                self.y = self.data[:, 1:]
            else:
                print('Could not find string \"' + text + '\" to skip rows. Data not loaded.')
        elif model == 'emstatpico':
            self.data = np.loadtxt(self.file_path, delimiter=self.delimiter)
            self.t = self.data[:, 0]
            self.E = self.data[:, 1]
            self.i = self.data[:, 2:]
        else:
            self.data = np.loadtxt(self.file_path, delimiter=self.delimiter,
                                   skiprows=self.skiprows)
            self.E = self.data[:, 0]
            self.i = self.data[:, 1:]

    def search(self, text):
        with open(self.file_path, 'r') as fn:
            count = 0
            for line in fn:
                count += 1
                if text in line:
                    return count
            return 0


class XY(Read):
    """
    """

    def __init__(self, fileName='file', folder='.', skiprows=0, delimiter=',',
                 model=0):
        self.fileName = fileName
        self.folder = folder
        Read.__init__(self)
        self.skiprows = skiprows
        self.delimiter = delimiter
        self.read()


class CV(Read):
    """
    """

    def __init__(self, fileName='file', folder='.', model=0):
        self.fileName = fileName
        self.folder = folder
        text = 'Potential/V,'
        Read.__init__(self)
        self.read(text, model)
        if model[0:3] == 'chi':
            self.E = self.x
            self.i = self.y


class LSV(Read):
    """
    """

    def __init__(self, fileName='file', folder='.', model=0):
        super().__init__()
        cv = CV(fileName, folder, model)  # Same as CV
        self.E = cv.E
        self.i = cv.i


class IT(Read):
    """
    """

    def __init__(self, fileName='file', folder='.', model=0):
        self.fileName = fileName
        self.folder = folder
        text = 'Time/sec,'
        Read.__init__(self)
        self.read(text, model)
        if model[0:3] == 'chi':
            self.t = self.x
            # self.E = self.E
            self.i = self.y


class CA(Read):
    """
    """

    def __init__(self, fileName='file', folder='.', model=0):
        self.fileName = fileName
        self.folder = folder
        text = 'Time/sec,'
        Read.__init__(self)
        self.read(text, model)
        if model[0:3] == 'chi':
            self.t = self.x
            # self.E = self.E
            self.i = self.y


class OCP(Read):
    """
    """

    def __init__(self, fileName='file', folder='.', model=0):
        self.fileName = fileName
        self.folder = folder
        text = 'Time/sec,'
        Read.__init__(self)
        self.read(text, model)
        if model[0:3] == 'chi':
            self.t = self.x
            self.E = self.y


class EIS(Read):
    """
    """

    def __init__(self, fileName='file', folder='.', model=0):
        self.fileName = fileName
        self.folder = folder
        text = 'Freq/Hz'
        Read.__init__(self)
        self.read(text, model)
        if model[0:3] == 'chi':
            self.freq = self.x
            self.z_1 = self.y[:, 0]
            self.z_2 = self.y[:, 1]
            self.z = self.y[:, 2]
            self.phase = self.y[:, 3]
