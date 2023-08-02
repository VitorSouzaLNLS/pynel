"""Module 'buttons' for the class Object Button"""

from .std_si_data import MODEL_BASE, SI_SPOS, SI_SECT_SPOS, STD_SECTS, STD_TYPES, STD_ELEMS_HALB, STD_ELEMS_LBLP, STD_ORBCORR_INV_JACOB_MAT, SI_FAMDATA, STD_GIRDER_NAMES
from apsuite.orbcorr import OrbitCorr as _OrbitCorr
import numpy as _np
from copy import deepcopy as _dpcopy
from .misc_functions import calc_vdisp as _calc_vdisp
from .misc_functions import pick_func
from .misc_functions import rmk_correct_orbit
from pyaccel.optics import calc_twiss as _calc_twiss


_MODEL_BASE       = MODEL_BASE()
_SI_SPOS          = SI_SPOS()
_SI_SECT_SPOS     = SI_SECT_SPOS()
_STD_GIRDER_NAMES = STD_GIRDER_NAMES()
_STD_SECTS        = STD_SECTS()       
_STD_TYPES        = STD_TYPES()       
_STD_ELEMS_HALB   = STD_ELEMS_HALB() 
_STD_ELEMS_LBLP   = STD_ELEMS_LBLP() 
_OC_MODEL = MODEL_BASE() # new pymodels si model
_OC = _OrbitCorr(_OC_MODEL, 'SI')
_OC.params.maxnriters = 500
_IJMAT            = STD_ORBCORR_INV_JACOB_MAT()
# _IJMAT          = _OC.get_inverse_matrix(_OC.get_jacobian_matrix())
_STD_SECT_TYPES = ['HighBetaA -> LowBetaB', 
                    'LowBetaB -> LowBetaP', 
                    'LowBetaP -> LowBetaB', 
                    'LowBetaB -> HighBetaA']
_SI_FAMDATA = SI_FAMDATA()

class Button:
    """Button object for storing a magnet (bname), it's sector (sect), it's indices 
       and it's vertical dispersion signature due to an misaligment (dtype)"""
    def __init__(self, sect=None, dtype=None, name=None, default_valids='std', famdata='auto', func='testfunc', indices='auto'):
        if default_valids == 'std':
            default_valids = ['std', 'std', 'std']
        elif default_valids == 'off':
            default_valids = ['off', 'off', 'off']
        elif isinstance(default_valids, (tuple, list)):
            if len(default_valids) == 3:
                if any((d not in ['off', 'std']) for d in default_valids):
                    raise ValueError('the "default_valids should contain only "std" of "off" strings"')
            else:
                raise ValueError('"default_valids" parameter should be a list of 3 strings: "off" and/or "std"')
        else:
            raise ValueError('"default_valids" parameter should be "off", "std" or a list/tuple')
        if indices == 'auto':
            if sect == None and name == None and dtype == None:
                raise ValueError('None of this parameters were passed: Sect, Name, Dtype or Indices')
            else:
                self.__init_by_default(sect=sect, dtype=dtype, name=name, default_valids=default_valids, famdata=famdata, func=func)
        elif isinstance(indices, list):
            if all(isinstance(i, (int, _np.integer)) for i in indices):
                self.__init_by_indices(indices=indices, dtype=dtype, func=func, default_valids=default_valids)
            else:
                raise ValueError('indices with invalid values')
        elif isinstance(indices, (int, _np.integer)):
            self.__init_by_indices(indices=[indices], dtype=dtype, func=func, default_valids=default_valids)
        else:
            raise ValueError('Indices passed in wrong format')

    def __init_by_indices(self, indices, dtype, func, default_valids):
        #print('init by indices')
        self.indices = indices
        name = ''
        sect = [-1]
        model_base = _MODEL_BASE
        si_spos = _SI_SPOS
        si_sect_spos = _SI_SECT_SPOS
        if len(indices) == 1:
            i = indices[0]
            name = model_base[i].fam_name
            #pos = si_spos[i]
            for j in range(20):
                if si_sect_spos[j] <= si_spos[i] < si_sect_spos[j+1]:
                    if (j+1) not in sect:
                        sect.append(j+1)
        else:
            for i in indices:
                name += '_'+model_base[i].fam_name # should agree with the std girders names
                #pos = si_spos[i]
                for j in range(20):
                    if si_sect_spos[j] <= si_spos[i] < si_sect_spos[j+1]:
                        if (j+1) not in sect:
                            sect.append(j+1)
        if len(sect) > 2:
            #print(name, sect, indices)
            raise ValueError('some elements passed are from different sectors')
        self.sect = sect[-1]
        self.bname = name
        self.fantasy_name = name
        self.dtype = dtype
        self.sectype = self.__sector_type()
        if default_valids[0] == 'off':
            self.__validsects = 'off'
        elif default_valids[0] == 'std':
            self.__validsects = _STD_SECTS 

        if default_valids[1] == 'off':
            self.__validtypes = 'off'
        elif default_valids[1] == 'std':
            self.__validtypes = _STD_TYPES

        if default_valids[2] == 'off':
            self.__validnames = 'off'
        elif default_valids[2] == 'std':
            self.__validnames = _STD_GIRDER_NAMES

        self.signature = _np.array([0.0 for _ in range(160)])
        if self.check_isvalid():
            if func == 'vertical_disp':
                temp = self.__calc_vertical_dispersion_signature()
            elif func == 'testfunc':
                temp = self.__calc_test_func_signature()
            elif func == 'twiss':
                temp = self.__calc_twiss_signatures()
            else:
                raise KeyError('Invalid signature function. Try "vertical_disp", "testfunc" or "twiss"')
            if isinstance(temp, list) and len(temp) == 1:
                if len(temp[0]) == 160:
                    self.signature = temp[0]
                else:
                    raise ValueError('Error calculating signature')
            else:
                self.signature = temp

    def __init_by_default(self, sect, dtype, name, default_valids, famdata, func):
        #print('init by default')
        self.bname = name
        self.fantasy_name = name
        self.dtype = dtype
        self.sect = sect
        self.sectype = self.__sector_type()

        if famdata == 'auto':
            fam = _SI_FAMDATA
        else:
            fam = famdata

        if default_valids[0] == 'std':
            self.__validsects = _STD_SECTS
        if default_valids[0] == 'off':
            self.__validsects = 'off'

        if default_valids[1] == 'std':
            self.__validtypes = _STD_TYPES
        if default_valids[1] == 'off':
            self.__validtypes = 'off'

        if default_valids[2] == 'std':
            if self.sectype in ['HighBetaA -> LowBetaB', 'LowBetaB -> HighBetaA']:
                self.__validnames = _STD_ELEMS_HALB
            elif self.sectype in ['LowBetaP -> LowBetaB', 'LowBetaB -> LowBetaP']:
                self.__validnames = _STD_ELEMS_LBLP
            else:
                self.__validnames = []
        if default_valids[2] == 'off':
            self.__validnames = 'off'

        self.indices = []
        self.signature = _np.zeros(160)
        temp = [0.0 for _ in range(160)]

        if self.check_isvalid():
            self.indices = self.__find_indices(fam)

            if func == 'vertical_disp':
                temp = self.__calc_vertical_dispersion_signature()
            elif func == 'testfunc':
                temp = self.__calc_test_func_signature()
            elif func == 'twiss':
                temp = self.__calc_twiss_signatures()
            else:
                raise KeyError('Invalid signature function. Try "vertical_disp", "testfunc" or "twiss"')
            
        if all(isinstance(l, list) for l in self.indices):
            if len(self.indices) == 1:
                if all(isinstance(i, (int, _np.integer)) for i in self.indices[0]):
                    self.indices = self.indices[0]
                    self.signature = temp[0]
            elif all(all(isinstance(i, (int, _np.integer)) for i in self.indices[k]) for k in range(len(self.indices))):
                self.signature = temp
            else:
                raise ValueError('indices has lists, but not lists of ints')

        elif all(isinstance(i, (int, _np.integer)) for i in self.indices):
            if len(temp) == 1:
                if len(temp[0]) == 160:
                    self.signature = temp[0]
                else:
                    raise ValueError('error with signature')
                
            elif len(temp) == 160:
                self.signature = temp
            else:
                raise ValueError('error with signature')
        else:
            raise ValueError('indices error')

    def check_isflat(self):
        if self.indices == []:
            return True
        elif isinstance(self.indices, list):
            if all(isinstance(idx, (int, _np.integer)) for idx in self.indices):
                return True
            elif all(isinstance(idx, list) for idx in self.indices):
                return False
        else:
            raise ValueError('flat error: problem with indices')

    def __str__(self) -> str:
        return '('+str(self.sect)+','+str(self.dtype)+','+str(self.fantasy_name)+')'

    def __repr__(self) -> str:
        return '('+str(self.sect)+','+str(self.dtype)+','+str(self.fantasy_name)+')'

    def __eq__(self, other):
        if isinstance(other, Button):
            return self.bname == other.bname and self.dtype == other.dtype and self.sect == other.sect and self.indices == other.indices and self.fantasy_name == other.fantasy_name
        return False

    def check_isvalid(self):
        validify = [False, False, False]
        if self.__validsects == 'off':
            validify[0] = True
        elif (self.sect in self.__validsects):
            validify[0] = True
        if self.__validtypes == 'off':
            validify[1] = True
        elif (self.dtype in self.__validtypes):
            validify[1] = True
        if self.__validnames == 'off':
            validify[2] = True
        elif (self.bname in self.__validnames):
            validify[2] = True
        return all(validify)
    
    def __check_isvalid_for_printing(self):
        validify = [False, False, False]
        if self.__validsects == 'off':
            validify[0] = True
        elif (self.sect in self.__validsects):
            validify[0] = True
        if self.__validtypes == 'off':
            validify[1] = True
        elif (self.dtype in self.__validtypes):
            validify[1] = True
        if self.__validnames == 'off':
            validify[2] = True
        elif (self.bname in self.__validnames):
            validify[2] = True
        return validify
        

    def show_invalid_parameters(self):
        valids = self.__check_isvalid_for_printing()
        invalid = []
        strings = ['sector', 'dtype', 'name']
        for i, v in enumerate(valids):
            if not v:
                invalid.append(strings[i])
        if len(invalid) == 0:
            print('(%d, %s, %s) ---> valid button' % (self.sect,self.dtype, self.bname))
        if len(invalid) == 1:
            print('(%d, %s, %s) ---> invalid %s' % (self.sect, self.dtype, self.bname,  invalid[0]))
        if len(invalid) == 2:
            print('(%d, %s, %s) ---> invalid %s & %s' % (self.sect, self.dtype, self.bname, invalid[0], invalid[1]))
        if len(invalid) == 3:
            print('(%d, %s, %s) ---> completely invalid' % (self.sect, self.dtype, self.bname))

    def __find_indices(self, famdata):
        famidx = famdata[self.bname]['index']
        aux = len(famidx)/20
        if self.sectype == 'Not_Sirius_Sector':
            idx = []
        else:
            if aux == 0.5:  # 1 elemento a cada 2 setores
                if self.sectype == _STD_SECT_TYPES[0]:      #'HighBetaA -> LowBetaB':
                    idx = [famidx[int(0.5 * (self.sect-1))]]
                elif self.sectype == _STD_SECT_TYPES[3]:    #'LowBetaB -> HighBetaA':
                    idx = [famidx[int((0.5*self.sect) - 1)]]

                elif self.sectype == _STD_SECT_TYPES[1]:    #'LowBetaB -> LowBetaP':
                    idx = [famidx[int((0.5*self.sect) - 1)]]

                elif self.sectype == _STD_SECT_TYPES[2]:    #'LowBetaP -> LowBetaB':
                    idx = [famidx[int(0.5 * (self.sect-1))]]

            elif aux == 1.0:  # 1 elemento por setor
                idx = [famidx[self.sect - 1]]
            elif aux == 2.0:  # 2 elementos por setor
                idx = [famidx[2*self.sect - 2], famidx[2*self.sect - 1]]
        return idx

    def __sector_type(self):
        if self.sect in [2, 6, 10, 14, 18]:
            return _STD_SECT_TYPES[1]
        elif self.sect in [3, 7, 11, 15, 19]:
            return _STD_SECT_TYPES[2]
        elif self.sect in [4, 8, 12, 16, 20]:
            return _STD_SECT_TYPES[3]
        elif self.sect in [1, 5, 9, 13, 17]:
            return _STD_SECT_TYPES[0]
        else:
            return 'Not_Sirius_Sector'

    def __calc_test_func_signature(self):
        disp = []
        if all(isinstance(i, list) for i in self.indices):
            #print('list of lists')
            for ind in self.indices:
                _disp = _np.array([i for i in range(160)])
                disp.append(_disp.ravel())
        elif all(isinstance(i, (int, _np.integer)) for i in self.indices):
            #print('list of ints')
            _disp = _np.array([i for i in range(160)])
            disp.append(_disp.ravel())
        else:
            raise ValueError('Indices with format problem')
        return disp
    
    def __calc_vertical_dispersion_signature(self):
        func = pick_func(self.dtype)
        if all(isinstance(i, list) for i in self.indices): # list of list of ints
            indices = self.indices
        elif all(isinstance(i, (int, _np.integer)) for i in self.indices): # list of ints
            indices = [self.indices]  
        else:
            raise ValueError('Indices with format problem')
        
        # the calculation:
        disp = []
        # MODEL_ = MODEL_BASE() # new pymodels si model
        # OC_ = _OrbitCorr(MODEL_, 'SI')
        #_IJMAT_  = OC_.get_inverse_matrix(OC_.get_jacobian_matrix())
        for ind in indices:
            func(_OC_MODEL, indices=ind, values=+1e-6) # applying (SETTING) positive delta
            rmk_correct_orbit(_OC, _IJMAT)
            disp_p = _calc_vdisp(_OC_MODEL)
            
            func(_OC_MODEL, indices=ind, values=-1e-6) # applying (SETTING) negative delta
            rmk_correct_orbit(_OC, _IJMAT)
            disp_n = _calc_vdisp(_OC_MODEL)
            
            disp_ = (disp_p - disp_n)/(2e-6)
            
            disp.append(disp_.ravel())

            func(_OC_MODEL, indices=ind, values=0.0)
        del disp_, disp_n, disp_p #, OC_, MODEL_
        return disp
    
    def __calc_twiss_signatures(self):
        func = pick_func(self.dtype)
        if all(isinstance(i, list) for i in self.indices): # list of list of ints
            indices = self.indices
        elif all(isinstance(i, (int, _np.integer)) for i in self.indices): # list of ints
            indices = [self.indices]  
        else:
            raise ValueError('Indices with format problem')
        twiss = []
        # the calculation:
        for ind in indices:
            func(_OC_MODEL, indices=ind, values=+1e-6) # applying (SETTING) positive delta
            rmk_correct_orbit(_OC, _IJMAT)
            twiss_p = _calc_twiss(_OC_MODEL)[0]
            
            func(_OC_MODEL, indices=ind, values=-1e-6) # applying (SETTING) negative delta
            rmk_correct_orbit(_OC, _IJMAT)
            twiss_n = _calc_twiss(_OC_MODEL)[0]
            
            twiss.append({  'betax': ((twiss_p.betax  - twiss_n.betax )/(2e-6)).ravel(),
                            'mux':   ((twiss_p.mux    - twiss_n.mux   )/(2e-6)).ravel(),
                            'alphax':((twiss_p.alphax - twiss_n.alphax)/(2e-6)).ravel(),
                            'betay': ((twiss_p.betay  - twiss_n.betay )/(2e-6)).ravel(),
                            'alphay':((twiss_p.alphay - twiss_n.alphay)/(2e-6)).ravel(),
                            'muy':   ((twiss_p.muy    - twiss_n.muy   )/(2e-6)).ravel(),                      
                            'etax':  ((twiss_p.etax   - twiss_n.etax  )/(2e-6)).ravel(),
                            'etapx': ((twiss_p.etapx  - twiss_n.etapx )/(2e-6)).ravel(),
                            'etay':  ((twiss_p.etay   - twiss_n.etay  )/(2e-6)).ravel(),
                            'etapy': ((twiss_p.etapy  - twiss_n.etapy )/(2e-6)).ravel(),
                            'rx':    ((twiss_p.rx     - twiss_n.rx    )/(2e-6)).ravel(), 
                            'px':    ((twiss_p.px     - twiss_n.px    )/(2e-6)).ravel(), 
                            'ry':    ((twiss_p.ry     - twiss_n.ry    )/(2e-6)).ravel(), 
                            'py':    ((twiss_p.py     - twiss_n.py    )/(2e-6)).ravel(), 
                            'de':    ((twiss_p.de     - twiss_n.de    )/(2e-6)).ravel(), 
                            'dl':    ((twiss_p.dl     - twiss_n.dl    )/(2e-6)).ravel()})

            func(_OC_MODEL, indices=ind, values=0.0)
        del twiss_p, twiss_n
        return twiss

    def flatten(self):
        if not isinstance(self.indices, list):
            raise ValueError('indices error')
        elif self.indices != []:
            if isinstance(self.indices[0], list):
                # Split the button into multiple buttons
                buttons = []
                for i in range(len(self.indices)):
                    sub_button = _dpcopy(self)
                    sub_button.indices = self.indices[i]
                    sub_button.signature = self.signature[i]
                    sub_button.fantasy_name = self.fantasy_name+'_'+str(i+1)
                    buttons.append(sub_button)
                return buttons
            else:
                # Return the button as a single-item list
                return [self]
        else:
            return [self] # flat button, but propably is invalid