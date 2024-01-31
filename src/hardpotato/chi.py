class ChiInfo:
    """
        Pending:
        * Calculate dE, sr, dt, ttot, mins and max
    """

    def __init__(self, model):
        if model == "chi601e":
            self.name = "CH Instruments 601E (chi601e)"
            self.tech = ['CV', 'IT', 'CA', 'LSV', 'OCP', 'NPV', 'EIS']
            self.options = [
                'Quiet time in s (qt)',
                'Resistance in ohms (resistance)'
            ]
            self.bipot = False
            self.resistance_opt = True

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
        elif model == "chi620e":
            self.name = "CH Instruments 620E (chi620e)"
            self.tech = ['CV', 'IT', 'CA', 'LSV', 'OCP', 'NPV']
            self.options = [
                'Quiet time in s (qt)',
                'Resistance in ohms (resistance)'
            ]
            self.bipot = True
            self.resistance_opt = True

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
            self.freq_min = 0.00001
            self.freq_max = 1000000
        elif model == "chi650e":
            self.name = "CH Instruments 620E (chi620e)"
            self.tech = ['CV', 'IT', 'CA', 'LSV', 'OCP', 'NPV', 'EIS']
            self.options = [
                'Quiet time in s (qt)',
                'Resistance in ohms (resistance)'
            ]
            self.bipot = True
            self.resistance_opt = True

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
            self.freq_min = 0.00001
            self.freq_max = 1000000
        elif model == "chi760e":
            self.name = "CH Instruments 760E (chi760e)"
            self.tech = self.tech = ['CV', 'IT', 'CA', 'LSV', 'OCP', 'NPV', 'EIS']
            self.options = [
                        'Quiet time in s (qt)',
                        'Resistance in ohms (resistance)'
                        ]
            self.bipot = True
            self.resistance_opt = True

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
            self.freq_min = 0.00001
            self.freq_max = 1000000
        elif model == "chi1205b":
            self.name = "CH Instruments 1205B (chi1205b)"
            self.tech = ['CV', 'IT', 'CA', 'LSV', 'OCP']
            self.options = ['Quiet time in s (qt)']
            self.bipot = False
            self.resistance_opt = False

            self.E_min = -2.4
            self.E_max = 2.4
            self.sr_min = 0.000001
            self.sr_max = 10
            # self.dE_min =
            # self.sr_min =
            # self.dt_min =
            # self.dt_max =
            # self.ttot_min =
            # self.ttot_max =
        elif model == "chi1242b":
            self.name = "H Instruments 1242B (chi1242b)"
            self.tech = ['CV', 'IT', 'CA', 'LSV', 'OCP']
            self.options = ['Quiet time in s (qt)']
            self.bipot = True
            self.resistance_opt = False

            self.E_min = -2.4
            self.E_max = 2.4
            self.sr_min = 0.000001
            self.sr_max = 10
            # self.dE_min =
            # self.sr_min =
            # self.dt_min =
            # self.dt_max =
            # self.ttot_min =
            # self.ttot_max =
        else:
            raise Exception(f"CHI model {model} not available in hardpotato.")

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


class ChiCV:
    """
        **kwargs:
            qt # s, quite time
            resistance # ohms, solution resistance
    """

    def __init__(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens,
                 folder, fileName, header, model="", **kwargs):
        self.info = ChiInfo(model)
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        qt = kwargs.get('qt', 2)
        resistance = kwargs.get('resistance', 0)

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
        self.head = f'c\x02\0\0\nfolder: {folder}\nfileoverride\n' \
                    f'header: {header}\n\n'
        self.body = f'tech=cv\nei={Ei}\neh={eh}\nel={el}\npn={pn}\ncl={nSweeps}' \
                    f'\nefon\nef={Efin}\nsi={dE}\nqt={qt}\nv={sr}\nsens={sens}'
        if resistance and self.info.resistance_opt:  # In case IR compensation is required
            self.body2 = self.body + f'\nmir={resistance}\nircompon\nrun\nircompoff\n' \
                                     f'save:{self.fileName}\ntsave:{self.fileName}'
        else:
            self.body2 = self.body + f'\nrun\nsave:{self.fileName}\ntsave:{self.fileName}'
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


class ChiLSV:
    """
        **kwargs:
            qt # s, quiet time
            resistance # ohms, solution resistance
    """

    def __init__(self, Eini, Efin, sr, dE, sens, folder, fileName, header, model="", **kwargs):
        self.info = ChiInfo(model)
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        qt = kwargs.get('qt', 2)
        resistance = kwargs.get('resistance', 0)

        self.validate(Eini, Efin, sr, dE, sens)

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=lsv\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nv=' + str(sr) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens)
        if resistance and self.info.resistance_opt:  # In case IR compensation is required
            self.body2 = self.body + '\nmir=' + str(resistance) + \
                         '\nircompon\nrun\nircompoff\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        else:
            self.body2 = self.body + '\nrun\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def bipot(self, E, sens):
        if not self.info.bipot:
            raise Exception(self.info.name, " does not have bipot abilities.")
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


class ChiNPV:
    def __init__(self, Eini, Efin, dE, tsample, twidth, tperiod, sens, folder, fileName, header, model="", **kwargs):
        self.info = ChiInfo(model)
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        qt = kwargs.get('qt', 2)

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


class ChiIT:
    """
    """

    def __init__(self, Estep, dt, ttot, sens, folder, fileName, header, model="", **kwargs):
        self.info = ChiInfo(model)
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        qt = kwargs.get('qt', 2)
        resistance = kwargs.get('resistance', 0)

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=i-t\nei=' + str(Estep) + '\nst=' + str(ttot) + \
                    '\nsi=' + str(dt) + '\nqt=' + str(qt) + \
                    '\nsens=' + str(sens)
        if resistance and self.info.resistance_opt:  # In case IR compensation is required
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
        if not self.info.bipot:
            raise Exception(self.info.name, " does not have bipot abilities.")
        # Validate bipot:
        self.info.limits(E, self.info.E_min, self.info.E_max, 'E2', 'V')
        # self.info.limits(sens, self.info.sens_min, self.info.sens_max, 'sens2', 'A/V')
        self.body2 = self.body + \
                     '\ne2=' + str(E) + '\nsens2=' + str(sens) + '\ni2on' + \
                     '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot


class ChiCA:
    """
        **kwargs:
            qt # s, quite time
    """

    def __init__(self, Eini, Ev1, Ev2,  dE, nSweeps, pw, sens,
                 folder, fileName, header, model="", **kwargs):
        self.info = ChiInfo(model)
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        qt = kwargs.get('qt', 2)

        self.validate(Eini, Ev1, Ev2)

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
        self.head = f'c\x02\0\0\nfolder: {folder}\nfileoverride\n' \
                    f'header: {header}\n\n'
        self.body = f'tech=ca\nei={Ei}\neh={eh}\nel={el}\npn={pn}\n' \
                    f'cl={nSweeps}\npw={pw}\nsi={dE}\nqt={qt}\nsens={sens}' \
                    f'\nrun\nsave:{self.fileName}\ntsave:{self.fileName}'
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot

    def validate(self, Eini, Ev1, Ev2):
        self.info.limits(Eini, self.info.E_min, self.info.E_max, 'Eini', 'V')
        self.info.limits(Ev1, self.info.E_min, self.info.E_max, 'Ev1', 'V')
        self.info.limits(Ev2, self.info.E_min, self.info.E_max, 'Ev2', 'V')


class ChiOCP:
    """
        Assumes OCP is between +- 10 V
    """

    def __init__(self, ttot, dt, folder, fileName, header, model="", **kwargs):
        self.info = ChiInfo(model)
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        qt = kwargs.get('qt', 2)
        resistance = kwargs.get('resistance', 0)

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


class ChiEIS:
    """
        Pending:
        * Validate parameters
    """

    def __init__(self, Eini, low_freq, high_freq, amplitude, sens, folder, fileName, header, model="", **kwargs):
        print('EIS technique is still in development. Use with caution.')
        self.info = ChiInfo(model)
        self.fileName = fileName
        self.folder = folder

        qt = kwargs.get('qt', 2)

        self.head = f'C\x02\0\0\nfolder: {folder}\nfileoverride\nheader: {header}\n\n'
        self.body = f'tech=imp\nei={Eini}\nfl={low_freq}\nfh={high_freq}\namp={amplitude}\nsens={sens}\nqt={qt}' \
                    f'\nrun\nsave:{self.fileName}\ntsave:{self.fileName}'
        self.foot = '\nforcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot
