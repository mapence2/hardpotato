class BaseInfo:
    """
        Pending:
        * Calculate dE, sr, dt, ttot, mins and max
    """

    def __init__(self):
        self.name = ""
        self.tech = []
        self.options = []

        self.E_min = None
        self.E_max = None
        self.sr_min = None
        self.sr_max = None
        self.dE_min = None
        self.sr_min = None
        self.dt_min = None
        self.dt_max = None
        self.ttot_min = None
        self.ttot_max = None
        self.freq_min = None
        self.freq_max = None

    @staticmethod
    def limits(val, low, high, label, units):
        if val < low or val > high:
            raise Exception(label + ' should be between ' + str(low) + ' ' + \
                            units + ' and ' + str(high) + ' ' + units + \
                            '. Received ' + str(val) + ' ' + units)

    def specifications(self):
        print('Model: ', self.name)
        print('Techniques available:', self.tech)
        print('Options available:', self.options)


class BaseCV:
    """
        **kwargs:
            qt # s, quite time
            resistance # ohms, solution resistance
    """

    def __init__(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens,
                 folder, fileName, header, **kwargs):
        self.info = BaseInfo()
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0

        self.validate(Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens)

        # correcting parameters:
        Ei = Eini
        if Ev1 > Ev2:
            eh = Ev1
            el = Ev2
            pn = 'p'
        else:
            eh = Ev2
            el = Ev1
            pn = 'n'
        nSweeps = nSweeps + 1  # final e from chi is enabled by default

        # building macro:
        self.head = 'c\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=cv\nei=' + str(Ei) + '\neh=' + str(eh) + '\nel=' + \
                    str(el) + '\npn=' + pn + '\ncl=' + str(nSweeps) + \
                    '\nefon\nef=' + str(Efin) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nv=' + str(sr) + '\nsens=' + str(sens)
        if resistance:  # In case IR compensation is required
            self.body2 = self.body + '\nmir=' + str(resistance) + \
                         '\nircompon\nrun\nircompoff\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        else:
            self.body2 = self.body + '\nrun\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def validate(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens):
        self.info.limits(Eini, self.info.E_min, self.info.E_max, 'Eini', 'V')
        self.info.limits(Ev1, self.info.E_min, self.info.E_max, 'Ev1', 'V')
        self.info.limits(Ev2, self.info.E_min, self.info.E_max, 'Ev2', 'V')
        self.info.limits(Efin, self.info.E_min, self.info.E_max, 'Efin', 'V')
        self.info.limits(sr, self.info.sr_min, self.info.sr_max, 'sr', 'V/s')
        # self.info.limits(dE, self.info.dE_min, self.info.dE_max, 'dE', 'V')
        # self.info.limits(sens, self.info.sens_min, self.info.sens_max, 'sens', 'A/V')


class BaseLSV:
    """
        **kwargs:
            qt # s, quiet time
            resistance # ohms, solution resistance
    """

    def __init__(self, Eini, Efin, sr, dE, sens, folder, fileName, header, **kwargs):
        self.info = BaseInfo()
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0

        self.validate(Eini, Efin, sr, dE, sens)

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=lsv\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nv=' + str(sr) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens)
        if resistance:  # In case IR compensation is required
            self.body2 = self.body + '\nmir=' + str(resistance) + \
                         '\nircompon\nrun\nircompoff\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        else:
            self.body2 = self.body + '\nrun\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def bipot(self, E, sens):
        # Validate bipot:
        self.info.limits(E, self.info.E_min, self.info.E_max, 'E2', 'V')
        # self.info.limits(sens, self.info.sens_min, self.info.sens_max, 'sens', 'A/V')

        self.body2 = self.body + \
                     '\ne2=' + str(E) + '\nsens2=' + str(sens) + '\ni2on' + \
                     '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def validate(self, Eini, Efin, sr, dE, sens):
        self.info.limits(Eini, self.info.E_min, self.info.E_max, 'Eini', 'V')
        self.info.limits(Efin, self.info.E_min, self.info.E_max, 'Efin', 'V')
        self.info.limits(sr, self.info.sr_min, self.info.sr_max, 'sr', 'V/s')
        # self.info.limits(dE, self.info.dE_min, self.info.dE_max, 'dE', 'V')
        # self.info.limits(sens, self.info.sens_min, self.info.sens_max, 'sens', 'A/V')


class BaseNPV():
    def __init__(self, Eini, Efin, dE, tsample, twidth, tperiod, sens, folder, fileName, header, **kwargs):
        self.info = BaseInfo()
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2

        print('NPV technique still in development. Use with caution.')

        self.validate(Eini, Efin, dE, tsample, twidth, tperiod, sens)

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=NPV\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nincre=' + str(dE) + '\npw=' + str(tsample) + \
                    '\nsw=' + str(twidth) + '\nprod=' + str(tperiod) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens)
        self.body = self.body + \
                    '\nrun\nsave:' + fileName + '\ntsave:' + fileName
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot

    def validate(self, Eini, Efin, dE, tsample, twidth, tperiod, sens):
        self.info.limits(Eini, self.info.E_min, self.info.E_max, 'Eini', 'V')
        self.info.limits(Efin, self.info.E_min, self.info.E_max, 'Efin', 'V')
        # self.info.limits(tsample, self.info.tsample)
        # self.info.limits(dE, self.info.dE_min, self.info.dE_max, 'dE', 'V')
        # self.info.limits(sens, self.info.sens_min, self.info.sens_max, 'sens', 'A/V')


class BaseCA:
    """
    """

    def __init__(self, Estep, dt, ttot, sens, folder, fileName, header, **kwargs):
        self.info = BaseInfo()
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=i-t\nei=' + str(Estep) + '\nst=' + str(ttot) + \
                    '\nsi=' + str(dt) + '\nqt=' + str(qt) + \
                    '\nsens=' + str(sens)
        if resistance:  # In case IR compensation is required
            self.body2 = self.body + '\nmir=' + str(resistance) + \
                         '\nircompon\nrun\nircompoff\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        else:
            self.body2 = self.body + '\nrun\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

        self.validate(Estep, dt, ttot, sens)

    def validate(self, Estep, dt, ttot, sens):
        self.info.limits(Estep, self.info.E_min, self.info.E_max, 'Estep', 'V')
        # self.info.limits(dt, self.info.dt_min, self.info.dt_max, 'dt', 's')
        # self.info.limits(ttot, self.info.ttot_min, self.info.ttot_max, 'ttot', 's')
        # self.info.limits(sens, self.info.sens_min, self.info.sens_max, 'sens', 'A/V')

    def bipot(self, E, sens):
        # Validate bipot:
        self.info.limits(E, self.info.E_min, self.info.E_max, 'E2', 'V')
        # self.info.limits(sens, self.info.sens_min, self.info.sens_max, 'sens2', 'A/V')
        self.body2 = self.body + \
                     '\ne2=' + str(E) + '\nsens2=' + str(sens) + '\ni2on' + \
                     '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot


class BaseOCP:
    """
        Assumes OCP is between +- 10 V
    """

    def __init__(self, ttot, dt, folder, fileName, header, **kwargs):
        self.info = BaseInfo()
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=ocpt\nst=' + str(ttot) + '\neh=10' + \
                    '\nel=-10' + '\nsi=' + str(dt) + '\nqt=' + str(qt) + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName
        self.foot = '\nforcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot

        self.validate(ttot, dt)

    def validate(self, ttot, dt):
        pass
        # self.info.limits(dt, self.info.dt_min, self.info.dt_max, 'dt', 's')
        # self.info.limits(ttot, self.info.ttot_min, self.info.ttot_max, 'ttot', 's')


class BaseEIS:
    """
        Pending:
        * Validate parameters
    """

    def __init__(self, Eini, low_freq, high_freq, amplitude, sens, folder, fileName, header, **kwargs):
        print('EIS technique is still in development. Use with caution.')
        self.info = BaseInfo()
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=imp\nei=' + str(Eini) + '\nfl=' + str(low_freq) + \
                    '\nfh=' + str(high_freq) + '\namp=' + str(amplitude) + \
                    '\nsens=' + str(sens) + '\nqt=' + str(qt) + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName
        self.foot = '\nforcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot
