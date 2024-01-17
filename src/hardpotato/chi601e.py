from hardpotato.bases_classes import *


class Test:
    """
    """
    def __init__(self):
        print('Test from chi601e translator')


class Info(BaseInfo):
    def __init__(self):
        super().__init__()
        self.name = "CH Instruments 601E (chi601e)"
        self.tech = ['CV', 'CA', 'LSV', 'OCP', 'NPV', 'EIS']
        self.options = [
                        'Quiet time in s (qt)', 
                        'Resistance in ohms (resistance)'
                        ]

        self.E_min = -10
        self.E_max = 10
        self.sr_min = 0.000001
        self.sr_max = 10000
        # self.dE_min =
        # self.sr_min =
        # self.dt_min =
        # self.dt_max =
        # self.ttot_min =
        # self.ttot_max =
        # self.freq_min = 0.00001
        # self.freq_max = 1000000


class CV(BaseCV):
    """
        **kwargs:
            qt # s, quite time
            resistance # ohms, solution resistance
    """
    def __init__(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens, 
                 folder, fileName, header, **kwargs):
        super().__init__(Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens, folder, fileName, header, **kwargs)
        self.info = Info()


class LSV(BaseLSV):
    """
        **kwargs:
            qt # s, quiet time
            resistance # ohms, solution resistance
    """
    def __init__(self, Eini, Efin, sr, dE, sens, folder, fileName, header, **kwargs):
        super().__init__(Eini, Efin, sr, dE, sens, folder, fileName, header, **kwargs)
        self.info = Info()

    def bipot(self, E, sens):
        raise Exception(self.info.name, " does not have bipot abilities.")


class NPV(BaseNPV):
    def __init__(self, Eini, Efin, dE, tsample, twidth, tperiod, sens, folder, fileName, header, **kwargs):
        super().__init__(Eini, Efin, dE, tsample, twidth, tperiod, sens, folder, fileName, header, **kwargs)
        self.info = Info()


class CA(BaseCA):
    """
    """
    def __init__(self, Estep, dt, ttot, sens, folder, fileName, header, **kwargs):
        super().__init__(Estep, dt, ttot, sens, folder, fileName, header, **kwargs)
        self.info = Info()

    def bipot(self, E, sens):
        raise Exception(self.info.name, " does not have bipot abilities.")


class OCP(BaseOCP):
    """
        Assumes OCP is between +- 10 V
    """

    def __init__(self, ttot, dt, folder, fileName, header, **kwargs):
        super().__init__(ttot, dt, folder, fileName, header, **kwargs)
        self.info = Info()
