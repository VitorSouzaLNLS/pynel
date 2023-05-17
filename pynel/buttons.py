"""Module 'buttons' for the class Object Button"""

from .std_si_data import *
from apsuite.orbcorr import OrbitCorr as _OrbitCorr
import numpy as _np
from copy import deepcopy as _dpcopy
from .misc_functions import calc_vdisp as _calc_vdisp
from .misc_functions import pick_func
from .misc_functions import rmk_correct_orbit

class Button:
    def __init__(self, sect=None, name=None, dtype=None, default_valids='std', famdata='auto', func='testfunc', indices='auto'):
        if indices == 'auto':
            if sect == None and name == None and dtype == None:
                raise ValueError('None of this parameters were passed: Sect, Name, Dtype or Indices')
            else:
                self.__init_by_default(sect=sect, name=name, dtype=dtype, default_valids=default_valids, famdata=famdata, func=func)
        elif isinstance(indices, list):
            if all(isinstance(i, int) for i in indices):
                self.__init_by_indices(indices=indices, dtype=dtype, func=func, default_valids=default_valids)
            else:
                raise ValueError('indices with invalid values')
        elif isinstance(indices, int):
            self.__init_by_indices(indices=[indices], dtype=dtype, func=func, default_valids=default_valids)
        else:
            raise ValueError('Indices passed in wrong format')

    def __init_by_indices(self, indices, dtype, func, default_valids):
        #print('init by indices')
        self.indices = indices
        name = ''
        sect = [-1]
        if len(indices) == 1:
            name = MODEL_BASE[i].fam_name
            pos = SI_SPOS[i]
            for j in range(20):
                if SI_SECT_SPOS[j] <= SI_SPOS[i] < SI_SECT_SPOS[j+1]:
                    if (j+1) not in sect:
                        sect.append(j+1)
        else:
            for i in indices:
                name += '_'+MODEL_BASE[i].fam_name # should agree with the std girders names
                pos = SI_SPOS[i]
                for j in range(20):
                    if SI_SECT_SPOS[j] <= SI_SPOS[i] < SI_SECT_SPOS[j+1]:
                        if (j+1) not in sect:
                            sect.append(j+1)
        if len(sect) > 2:
            print(name, sect, indices)
            raise ValueError('some elements passed are from different sectors')
        self.sect = sect[-1]
        self.bname = name
        self.fantasy_name = name
        self.dtype = dtype
        self.sectype = self.__sector_type()
        if default_valids == 'std':
            self.__validnames = STD_GIRDER_NAMES
            self.__validsects = STD_SECTS
            self.__validtypes = STD_TYPES
        else:
            self.__validnames = default_valids[1]
            self.__validsects = default_valids[0]
            self.__validtypes = default_valids[2]
        self.signature = _np.array([0.0 for _ in range(160)])
        if self.check_isvalid():
            if func == 'vertical_disp':
                temp = self.__calc_vertical_signature_oncorr()
            elif func == 'testfunc':
                temp = self.__calc_test_func()
                #temp = self.__calc_vertical_signature_offcorr()
            else:
                raise KeyError('Invalid signature function. Try "vertical_disp" or "testfunc"')
            if isinstance(temp, list) and len(temp) == 1:
                if len(temp[0]) == 160:
                    self.signature = temp[0]
                else:
                    raise ValueError('Error calculating signature')
            else:
                self.signature = temp

    def __init_by_default(self, sect, name, dtype, default_valids, famdata, func):
        #print('init by default')
        self.bname = name
        self.fantasy_name = name
        self.dtype = dtype
        self.sect = sect
        self.sectype = self.__sector_type()

        if famdata == 'auto':
            fam = SI_FAMDATA
        else:
            fam = famdata

        if default_valids == 'std':
            if self.sectype in ['HA-LB', 'LB-HA']:
                self.__validnames = STD_ELEMS_HALB

            elif self.sectype in ['LP-LB', 'LB-LP']:
                self.__validnames = STD_ELEMS_LBLP
            else:
                self.__validnames = []

            self.__validsects = STD_SECTS
            self.__validtypes = STD_TYPES

        elif isinstance(default_valids, list):
            if len(default_valids) == 3:
                self.__validsects = default_valids[0]
                self.__validnames = default_valids[1]
                self.__validtypes = default_valids[2]
        else:
            raise TypeError('default valid properties not in correct format')

        self.indices = []
        self.signature = _np.zeros(160)
        temp = [0.0 for _ in range(160)]

        if self.check_isvalid():
            self.indices = self.__find_indices(fam)

            if func == 'vertical_disp':
                temp = self.__calc_vertical_signature_oncorr()
            elif func == 'testfunc':
                temp = self.__calc_test_func()
                #temp = self.__calc_vertical_signature_offcorr()
            else:
                raise KeyError('Invalid signature function. Try "vertical_disp" or "testfunc"')
            
        if all(isinstance(l, list) for l in self.indices):
            if len(self.indices) == 1:
                if all(isinstance(i, int) for i in self.indices[0]):
                    self.indices = self.indices[0]
                    self.signature = temp[0]
            elif all(all(isinstance(i, int) for i in self.indices[k]) for k in range(len(self.indices))):
                self.signature = temp
            else:
                raise ValueError('indices has lists, but not lists of ints')

        elif all(isinstance(i, int) for i in self.indices):
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
            if all(isinstance(idx, int) for idx in self.indices):
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
        if (self.bname in self.__validnames) and (self.sect in self.__validsects) and (self.dtype in self.__validtypes):
            return True
        return False

    def show_invalid_parameters(self):
        if (self.bname not in self.__validnames) and (self.sect not in self.__validsects):
            print('(%d, %s, %s) ---> invalid name & sect' %
                  (self.sect, self.bname, self.dtype))
        elif (self.bname not in self.__validnames) and (self.dtype not in self.__validtypes):
            print('(%d, %s, %s) ---> invalid name & type' %
                  (self.sect, self.bname, self.dtype))
        elif (self.dtype not in self.__validtypes) and (self.sect not in self.__validsects):
            print('(%d, %s, %s) ---> invalid type & sect' %
                  (self.sect, self.bname, self.dtype))
        elif (self.bname not in self.__validnames):
            print('(%d, %s, %s) ---> invalid name' %
                  (self.sect, self.bname, self.dtype))
        elif (self.dtype not in self.__validtypes):
            print('(%d, %s, %s) ---> invalid type' %
                  (self.sect, self.bname, self.dtype))
        elif (self.sect not in self.__validsects):
            print('(%d, %s, %s) ---> invalid sect' %
                  (self.sect, self.bname, self.dtype))
        elif (self.bname not in self.__validnames) and (self.sect not in self.__validsects) and (self.dtype not in self.__validtypes):
            print('(%d, %s, %s) ---> invalid name & type & sect' %
                  (self.sect, self.bname, self.dtype))
        else:
            print('(%d, %s, %s) ---> valid button' %
                  (self.sect, self.bname, self.dtype))

    def __find_indices(self, famdata):
        famidx = famdata[self.bname]['index']
        aux = len(famidx)/20
        if self.sectype == 'Not_Sirius_Sector':
            idx = []
        else:
            if aux == 0.5:  # 1 elemento a cada 2 setores
                if self.sectype == 'HA-LB':
                    idx = [famidx[int(0.5 * (self.sect-1))]]
                elif self.sectype == 'LB-HA':
                    idx = [famidx[int((0.5*self.sect) - 1)]]

                elif self.sectype == 'LB-LP':
                    idx = [famidx[int((0.5*self.sect) - 1)]]

                elif self.sectype == 'LP-LB':
                    idx = [famidx[int(0.5 * (self.sect-1))]]

            elif aux == 1.0:  # 1 elemento por setor
                idx = [famidx[self.sect - 1]]
            elif aux == 2.0:  # 2 elementos por setor
                idx = [famidx[2*self.sect - 2], famidx[2*self.sect - 1]]
        return idx

    def __sector_type(self):
        if self.sect in [2, 6, 10, 14, 18]:
            return 'LB-LP'
        elif self.sect in [3, 7, 11, 15, 19]:
            return 'LP-LB'
        elif self.sect in [4, 8, 12, 16, 20]:
            return 'LB-HA'
        elif self.sect in [1, 5, 9, 13, 17]:
            return 'HA-LB'
        else:
            return 'Not_Sirius_Sector'

    def __calc_test_func(self):
        disp = []
        if all(isinstance(i, list) for i in self.indices):
            #print('list of lists')
            for ind in self.indices:
                _disp = _np.array([i for i in range(160)])
                disp.append(_disp.ravel())
        elif all(isinstance(i, int) for i in self.indices):
            #print('list of ints')
            _disp = _np.array([i for i in range(160)])
            disp.append(_disp.ravel())
        else:
            raise ValueError('Indices with format problem')
        return disp
    
    def __calc_vertical_signature_oncorr(self):
        func = pick_func(self.dtype)
        if all(isinstance(i, list) for i in self.indices): # list of list of ints
            indices = self.indices
        elif all(isinstance(i, int) for i in self.indices): # list of ints
            indices = [self.indices]  
        else:
            raise ValueError('Indices with format problem')
        
        # the calculation:
        disp = []
        MODEL_ = create_std_si_model()
        OC = _OrbitCorr(MODEL_, 'SI')
        OC.params.maxnriters = 500
        jmat = OC.get_jacobian_matrix()
        inv_jacob = OC.get_inverse_matrix(jmat)
        for ind in indices:
            func(MODEL_, indices=ind, values=+1e-6) # applying positive delta
            rmk_correct_orbit(OC, inv_jacob)
            disp_p = _calc_vdisp(MODEL_)
            
            func(MODEL_, indices=ind, values=-1e-6) # applying negative delta
            rmk_correct_orbit(OC, inv_jacob)
            disp_n = _calc_vdisp(MODEL_)
            
            disp_ = (disp_p - disp_n)/(2e-6)
            
            disp.append(disp_.ravel())
        del MODEL_, disp_, disp_n, disp_p, OC, inv_jacob
        return disp

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