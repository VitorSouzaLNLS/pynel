"""Old complete module of pynel: the all joinned modules base, button, ... etc"""

import pymodels
import pyaccel
import numpy as np
from copy import deepcopy as dpcopy
import matplotlib.pyplot as plt
from apsuite.orbcorr import OrbitCorr

def create_std_si_model():
    model = pymodels.si.create_accelerator()
    model.radiation_on = True
    model.vchamber_on = True
    model.cavity_on = True
    return model

MODEL_BASE = create_std_si_model()
SI_SPOS = pyaccel.lattice.find_spos(MODEL_BASE, indices='closed').ravel()
SI_FAMDATA = pymodels.si.families.get_family_data(MODEL_BASE)
SI_GIRDERS = pymodels.si.families.get_girder_data(MODEL_BASE)
SI_SEXTUPOLES = pymodels.si.families.families_sextupoles()
SI_DIPOLES = pymodels.si.families.families_dipoles()
SI_QUADRUPOLES = pymodels.si.families.families_quadrupoles()
BPMIDX = list(np.array(SI_FAMDATA['BPM']['index']).ravel())
STD_ELEMS_HALB = set([
    'SFA0', 'QFA', 'SDA0', 'QDA', 'B1',
    'SDA1', 'Q1', 'SFA1', 'Q2', 'SDA2', 'B2',
    'SDA3', 'Q3', 'SFA2', 'Q4', 'BC',
    'Q4', 'SFB2', 'Q3', 'SDB3', 'B2',
    'SDB2', 'Q2', 'SFB1', 'Q1', 'SDB1', 'B1',
    'QDB1', 'SDB0', 'QFB', 'SFB0', 'QDB2'])

STD_ELEMS_LBLP = set([
    'QDB2', 'SFB0', 'QFB', 'SDB0', 'QDB1', 'B1',
    'SDB1', 'Q1', 'SFB1', 'Q2', 'SDB2', 'B2',
    'SDB3', 'Q3', 'SFB2', 'Q4', 'BC',
    'Q4', 'SFP2', 'Q3', 'SDP3', 'B2',
    'SDP2', 'Q2', 'SFP1', 'Q1', 'SDP1', 'B1',
    'QDP1', 'SDP0', 'QFP', 'SFP0', 'QDP2'
])
STD_TYPES = set(['dr', 'dx', 'dy'])
STD_SECTS = [i for i in range(1, 21)]
STD_ELEMS = SI_DIPOLES+SI_QUADRUPOLES+SI_SEXTUPOLES
STD_GIRDER_NAMES = ['_girder_FC1_l082_QFA_l150_SFA0_l135_BPM_girder',
 '_girder_SDP2_l170_Q2_l230_SFP1_l125_BPM_l135_Q1_l170_SDP1_l237_TuneShkrV_girder',
 '_girder_SDB2_l170_Q2_l230_SFB1_l125_BPM_l135_Q1_l170_SDB1_l237_DCCT_girder',
 '_girder_SDP2_l170_Q2_l230_SFP1_l125_BPM_l135_Q1_l170_SDP1_l237_DCCT_girder',
 '_girder_SDP0_l150_QDP1_l134_calc_mom_accep_B1_B1_B1_B1_B1_EDGE_B1_B1_SRC_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_mb1_calc_mom_accep_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_EDGE_B1_B1_B1_B1_calc_mom_accep_girder',
 '_girder_SDB2_l170_Q2_l230_SFB1_l125_BPM_l135_Q1_l170_SDB1_GBPM_girder',
 '_girder_calc_mom_accep_B1_B1_B1_B1_B1_EDGE_B1_B1_SRC_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_mb1_calc_mom_accep_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_EDGE_B1_B1_B1_B1_calc_mom_accep_l134_QDB1_l150_SDB0_girder',
 '_girder_SDA3_l170_Q3_l230_SFA2_l260_Q4_l200_CV_girder',
 '_girder_QFB_l150_SFB0_l049_FC1_l052_QDB2_l140_BPM_girder',
 '_girder_BPM_l140_QDP2_l052_FC1_l049_SFP0_l150_QFP_girder',
 '_girder_SDB0_l150_QDB1_l134_calc_mom_accep_B1_B1_B1_B1_B1_EDGE_B1_B1_SRC_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_mb1_calc_mom_accep_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_EDGE_B1_B1_B1_B1_calc_mom_accep_girder',
 '_girder_l112_Q4_l133_BPM_l127_SFB2_l056_FC1_l090_Q3_l170_SDB3_girder',
 '_girder_SDP1_l170_Q1_l135_BPM_l125_SFP1_l230_Q2_l170_SDP2_girder',
 '_girder_SDA1_l170_Q1_l135_BPM_l125_SFA1_l230_Q2_l170_SDA2_girder',
 '_girder_l112_Q4_l133_BPM_l127_SFP2_l056_FC1_l090_Q3_l170_SDP3_girder',
 '_girder_QFP_l150_SFP0_l049_FC1_l052_QDP2_l140_BPM_girder',
 '_girder_FC2_l119_BPM_l075_BC_BC_BC_BC_EDGE_BC_BC_BC_calc_mom_accep_BC_BC_calc_mom_accep_BC_BC_BC_BC_BC_BC_BC_BC_BC_mc_calc_mom_accep_BC_BC_BC_BC_BC_BC_BC_BC_BC_calc_mom_accep_BC_BC_calc_mom_accep_BC_BC_BC_BC_EDGE_BC_BC_BC_girder',
 '_girder_SDP2_l170_Q2_l230_SFP1_l125_BPM_l135_Q1_l170_SDP1_girder',
 '_girder_SDP3_l170_Q3_l230_SFP2_l260_Q4_l200_CV_girder',
 '_girder_SDB1_l170_Q1_l135_BPM_l125_SFB1_l230_Q2_l170_SDB2_girder',
 '_girder_SDA0_l150_QDA_l134_calc_mom_accep_B1_B1_B1_B1_B1_EDGE_B1_B1_SRC_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_mb1_calc_mom_accep_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_EDGE_B1_B1_B1_B1_calc_mom_accep_girder',
 '_girder_SDA2_l170_Q2_l230_SFA1_l125_BPM_l135_Q1_l170_SDA1_girder',
 '_girder_SDB3_l170_Q3_l230_SFB2_l260_Q4_l200_CV_girder',
 '_girder_SDB2_l170_Q2_l230_SFB1_l125_BPM_l135_Q1_l170_SDB1_l135_PingV_girder',
 '_girder_SDA2_l170_Q2_l230_SFA1_l125_BPM_l135_Q1_l170_SDA1_l237_BbBKckrV_girder',
 '_girder_BPM_l011_calc_mom_accep_B2_B2_B2_B2_B2_B2_EDGE_B2_B2_B2_B2_B2_B2_B2_calc_mom_accep_B2_B2_B2_B2_B2_B2_mb2_calc_mom_accep_B2_B2_B2_B2_B2_B2_calc_mom_accep_B2_B2_B2_B2_B2_B2_B2_B2_EDGE_B2_B2_B2_B2_B2_calc_mom_accep_girder',
 '_girder_SDB2_l170_Q2_l230_SFB1_l125_BPM_l135_Q1_l170_SDB1_l237_TunePkupV_girder',
 '_girder_BPM_l140_QDB2_l052_FC1_l049_SFB0_l150_QFB_girder',
 '_girder_calc_mom_accep_B1_B1_B1_B1_B1_EDGE_B1_B1_SRC_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_mb1_calc_mom_accep_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_EDGE_B1_B1_B1_B1_calc_mom_accep_l134_QDP1_l150_SDP0_girder',
 '_girder_SDB2_l170_Q2_l230_SFB1_l125_BPM_l135_Q1_l170_SDB1_girder',
 '_girder_calc_mom_accep_B1_B1_B1_B1_B1_EDGE_B1_B1_SRC_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_mb1_calc_mom_accep_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_B1_EDGE_B1_B1_B1_B1_calc_mom_accep_l134_QDA_l150_SDA0_girder',
 '_girder_BPM_l135_SFA0_l150_QFA_l082_FC1_girder',
 '_girder_l112_Q4_l133_BPM_l127_SFA2_l056_FC1_l090_Q3_l170_SDA3_girder']

SI_SECT_SPOS = [i*MODEL_BASE.length/20 for i in range(0,21)]
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
        self.signature = np.array([0.0 for _ in range(160)])
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
        self.signature = np.zeros(160)
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
                _disp = np.array([i for i in range(160)])
                disp.append(_disp.ravel())
        elif all(isinstance(i, int) for i in self.indices):
            #print('list of ints')
            _disp = np.array([i for i in range(160)])
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
        OC = OrbitCorr(MODEL_, 'SI')
        OC.params.maxnriters = 500
        jmat = OC.get_jacobian_matrix()
        inv_jacob = OC.get_inverse_matrix(jmat)
        for ind in indices:
            func(MODEL_, indices=ind, values=+1e-6) # applying positive delta
            rmk_correct_orbit(OC, inv_jacob)
            disp_p = calc_vdisp(MODEL_)
            
            func(MODEL_, indices=ind, values=-1e-6) # applying negative delta
            rmk_correct_orbit(OC, inv_jacob)
            disp_n = calc_vdisp(MODEL_)
            
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
                    sub_button = dpcopy(self)
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

class Base:
    def __init__(self, sects='all', elements='all', dtypes='all', auto_refine=True, exclude=None, reset_valids=False, func='vertical_disp', famdata='auto', buttons=None, girders=None):
        if buttons == None and girders == None:
            self.__init_by_default(sects, elements, dtypes, exclude, reset_valids, func, famdata)

        elif buttons != None and sects == 'all' and dtypes == 'all' and elements == 'all' and girders == None:
            if isinstance(buttons, list) and all(isinstance(i, Button) for i in buttons):
                self.__init_by_buttons(buttons=buttons)
            elif isinstance(buttons, Button):
                self.__init_by_buttons(buttons=[buttons])
            else:
                raise ValueError('parameter "buttons" passed with wrong format')
        
        elif girders != None and sects == 'all' and elements == 'all' and buttons == None:
            if isinstance(girders, list):
                if all(isinstance(i, int) for i in girders):
                    #print('list of ints')
                    if girders in SI_GIRDERS:
                        self.__init_by_girders(girders=[girders], dtypes=dtypes, func=func, famdata=famdata)
                elif all(isinstance(i, list) for i in girders):
                    if all(girder in SI_GIRDERS for girder in girders):
                        #print('list of list of ints')
                        self.__init_by_girders(girders=girders, dtypes=dtypes, func=func, famdata=famdata)
            else:
                raise ValueError('parameter "girders" with problem, check if the girders are correct')
        else:
            raise ValueError('conflict when passing "buttons" or "girders"')

        self._SECT_TYPES = self.__find_sector_types()
        self.__is_flat = self.__check_isflat()
        self.__is_updated = False

        if auto_refine:
            self.refine_base(update_buttons=True, flatten=True, return_removed=False, show_invalids=False)

        self.__matrix = self.__make_matrix()
        return
    
    def __init_by_girders(self, girders, dtypes, func, famdata):
        #print('starting by girders')
        __stdfunc = func
        _SECTS =[]
        _ELEMS =[]

        if dtypes == 'all':
            _TYPES = STD_TYPES
        else:
            if isinstance(dtypes, list):
                _TYPES = dtypes
            elif isinstance(dtypes, str):
                _TYPES = [dtypes]
            else:
                raise TypeError('dtypes parameter not in correct format')

        buttons = []
        for dtype in _TYPES:
            for girder_indices in girders:
                buttons.append(Button(dtype=dtype, indices=girder_indices, func=__stdfunc, famdata=famdata))

        for button in buttons:
            if button.sect not in _SECTS: 
                _SECTS.append(button.sect) 

            if button.bname not in _ELEMS: 
                _ELEMS.append(button.bname)

        self._SECTS, self._ELEMS, self._TYPES, self.__buttons_list = _SECTS, _ELEMS, _TYPES, buttons

    def __init_by_buttons(self, buttons):
        #print('starting by buttons')
        __stdfunc = 'None'
        _SECTS =[]
        _ELEMS =[]
        _TYPES =[]

        for button in buttons:
            if button.sect not in _SECTS: 
                _SECTS.append(button.sect) 

            if button.bname not in _ELEMS: 
                _ELEMS.append(button.bname) 

            if button.dtype not in _TYPES: 
                _TYPES.append(button.dtype)

        self._SECTS, self._ELEMS, self._TYPES, self.__buttons_list = _SECTS, _ELEMS, _TYPES, buttons

    def __check_isflat(self):
        for b in self.__buttons_list:
            if isinstance(b.indices, list) and b.indices == []:
                return True
            elif isinstance(b.indices, list) and b.indices != []:
                if isinstance(b.indices[0], list):
                    return False
                elif all(isinstance(idx, int) for idx in b.indices):
                    return True
                else:
                    raise ValueError('list of indices with problem')
        return False

    def __init_by_default(self, sects, elements, dtypes, exclude, reset_valids, func, famdata):
        #print('starting by default')
        if famdata == 'auto':
            famdat = SI_FAMDATA
        else:
            famdat = famdata
        if sects == 'all':
            _SECTS = STD_SECTS
        else:
            if isinstance(sects, list):
                _SECTS = sects
            elif isinstance(sects, int):
                _SECTS = [sects]
            else:
                raise TypeError('sects parameter not in correct format')
        if elements == 'all':
            _ELEMS = STD_ELEMS
        else:
            if isinstance(elements, list):
                _ELEMS = elements
            elif isinstance(elements, str):
                _ELEMS = [elements]
            else:
                raise TypeError('elements parameter not in correct format')

        if dtypes == 'all':
            _TYPES = STD_TYPES
        else:
            if isinstance(dtypes, list):
                _TYPES = dtypes
            elif isinstance(dtypes, str):
                _TYPES = [dtypes]
            else:
                raise TypeError('dtypes parameter not in correct format')

        if reset_valids:
            __default_valids = [self._SECTS, self._ELEMS, self._TYPES]
        else:
            __default_valids = 'std'

        self._SECTS, self._ELEMS, self._TYPES, = _SECTS, _ELEMS, _TYPES
        self.__buttons_list = self.__generate_buttons(exclude, famdata=famdat, stdfunc=func, default_valids=__default_valids)

    def __find_sector_types(self):
        sectypes = []
        for sect in self._SECTS:
            if sect in [2, 6, 10, 14, 18]:
                sectypes.append((sect, 'LB-LP'))
            elif sect in [3, 7, 11, 15, 19]:
                sectypes.append((sect, 'LP-LB'))
            elif sect in [4, 8, 12, 16, 20]:
                sectypes.append((sect, 'LB-HA'))
            elif sect in [1, 5, 9, 13, 17]:
                sectypes.append((sect, 'HA-LB'))
            else:
                sectypes.append((sect, 'Not_Sirius_Sector'))
        return dict(sectypes)

    def __generate_buttons(self, exclude=None, famdata=SI_FAMDATA, stdfunc='vertical_disp', default_valids='std'):
        
        to_exclude = []
        if exclude == None:
            exclude = set()
        elif isinstance(exclude, (str, int)):
            exclude = set([exclude])
        elif isinstance(exclude, (list, tuple)):
            exclude = set(exclude)
        else:
            raise TypeError("Exclude parameters not in format!")

        for e in exclude:
            if isinstance(e, (str, int)):
                to_exclude.extend(self.__exclude_buttons(e))
            elif isinstance(e, (tuple, list)):
                to_exclude.extend(self.__exclude_buttons(*e))
            else:
                raise TypeError("Exclude parameters not in format!")
        
        if to_exclude == []:
            to_exclude = [Button(sect=-1, name='FalseButton', dtype='dF')]
        exparams=[]
        for exbutton in to_exclude:
            exparams.append((exbutton.sect, exbutton.dtype, exbutton.bname))

        all_buttons = []
        for dtype in self._TYPES:
            for sect in self._SECTS:
                for elem in self._ELEMS:
                    if (sect, dtype, elem) not in exparams:
                        all_buttons.append(
                            Button(name=elem, dtype=dtype, sect=sect, default_valids=default_valids, famdata=famdata, func=stdfunc))
        #print(all_buttons)
        return all_buttons

    def __exclude_buttons(self, par1, par2=None, par3=None):
        if par2 == None and par3 == None:
            if isinstance(par1, int):
                exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                             for sect in self._SECTS
                             for dtype in self._TYPES
                             for elem in self._ELEMS
                             if sect == par1]
            elif isinstance(par1, str):
                if par1[0] == 'd':
                    exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                                 for sect in self._SECTS
                                 for dtype in self._TYPES
                                 for elem in self._ELEMS
                                 if dtype == par1]
                else:
                    exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                                 for sect in self._SECTS
                                 for dtype in self._TYPES
                                 for elem in self._ELEMS
                                 if elem == par1]
        elif par3 == None:
            if isinstance(par1, int):  # par1 = sect
                if par2.startswith('d'):  # par1 = sect, par2 = dtype #### (sect, dtype)
                    exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                                 for sect in self._SECTS
                                 for dtype in self._TYPES
                                 for elem in self._ELEMS
                                 if (dtype == par2 and sect == par1)]
                # par1 = sect, par2 = elem                     #### (sect, elem)
                else:
                    exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                                 for sect in self._SECTS
                                 for dtype in self._TYPES
                                 for elem in self._ELEMS
                                 if (elem == par2 and sect == par1)]
            elif isinstance(par2, int):  # par2 = sect
                if par1.startswith('d'):  # par1 = dtype, par2 = sect #### (dtype, sect)
                    exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                                 for sect in self._SECTS
                                 for dtype in self._TYPES
                                 for elem in self._ELEMS
                                 if (dtype == par1 and sect == par2)]
                # par1 = elem, par2 = sect                     #### (elem, sect)
                else:
                    exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                                 for sect in self._SECTS
                                 for dtype in self._TYPES
                                 for elem in self._ELEMS
                                 if (elem == par1 and sect == par2)]
            else:  # par1, par2 = elem or dtype:
                if par1.startswith('d'):  # par1 = dtype, par2 = elem #### (dtype, elem)
                    exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                                 for sect in self._SECTS
                                 for dtype in self._TYPES
                                 for elem in self._ELEMS
                                 if (dtype == par1 and elem == par2)]
                # par1 = elem, par2 = dtype                   #### (elem, dtype)
                else:
                    exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )
                                 for sect in self._SECTS
                                 for dtype in self._TYPES
                                 for elem in self._ELEMS
                                 if (elem == par1 and dtype == par2)]
        else:
            for el in (par1, par2, par3):
                if isinstance(el, int):
                    sect = el
                if isinstance(el, str) and el[0] == 'd':
                    dtype = el
                if isinstance(el, str) and el[0] != 'd':
                    elem = el
            exbuttons = [Button(name=elem, dtype=dtype, sect=sect, func='testfunc' )]
        return exbuttons

    def refine_base(self, update_buttons=True, flatten=True, return_removed=False, show_invalids=False):  
        if flatten:
            flat = []
            for b in self.__buttons_list:
                for new_b in b.flatten():
                    flat.append(new_b)
            self.__buttons_list = flat
            self.__is_flat = self.__check_isflat()

        to_remove = []
        for b in self.__buttons_list:
            if not b.check_isvalid():
                to_remove.append(b)

        if update_buttons:
            
            self._SECTS = []
            self._ELEMS = []
            self._TYPES = []
            old_buttons = dpcopy(self.__buttons_list)

            self.__buttons_list = []
            for button in old_buttons:
                if button not in to_remove: 
                    self.__buttons_list.append(button)
                    if button.sect not in self._SECTS: 
                        self._SECTS.append(button.sect) 
                    if button.bname not in self._ELEMS: 
                        self._ELEMS.append(button.bname) 
                    if button.dtype not in self._TYPES: 
                        self._TYPES.append(button.dtype) 

            self.__is_updated = True

        if show_invalids:
            for b in to_remove:
                b.show_invalid_parameters()

        if return_removed:
            return to_remove
        
        self.__matrix = self.__make_matrix()

    def __make_matrix(self):
        if len(self.__buttons_list) <= 0:
            print('Zero buttons, matrix not generated')

        elif self.__is_flat and self.__is_updated:
            M = np.zeros((160, len(self.__buttons_list)))
            for i, b in enumerate(self.__buttons_list):
                M[:, i] = np.array(b.signature).ravel()
            return M
        elif self.__is_flat == True and self.__is_updated == False:
            print('Base flat, but not updated please refine (update)')
            return 0
        elif self.__is_flat == False and self.__is_updated == True:
            print('Base not flat, please refine (flatten)')
            return 0
        else:
            print('Please refine Base (update & flatten)')
            return 0

    def buttons(self):
        return self.__buttons_list

    def sectors(self):
        return self._SECTS

    def magnets(self):
        return self._ELEMS

    def dtypes(self):
        return self._TYPES

    def sector_types(self):
        return self._SECT_TYPES

    def resp_mat(self):
        return self.__matrix

    def is_flat(self):
        return self.__check_isflat()

    def is_updated(self):
        return self.__is_updated

def apply_deltas(model, base, deltas):
    for i, button in enumerate(base.buttons()):
        func = pick_func(button.dtype)
        func(model, indices=button.indices, values=deltas[i])

def pick_func(dtype):
    if dtype == 'dx':
        func = pyaccel.lattice.set_error_misalignment_x
    elif dtype == 'dy':
        func = pyaccel.lattice.set_error_misalignment_y
    elif dtype == 'dr':
        func = pyaccel.lattice.set_error_rotation_roll
    elif dtype == 'drp':
        func = pyaccel.lattice.set_error_rotation_pitch
    elif dtype == 'dry':
        func = pyaccel.lattice.set_error_rotation_yaw
    elif dtype == 'dksl':
        func = add_error_ksl
    else:
        raise TypeError('invalid dtype!')
    return func

def add_error_ksl(lattice, indices, values):
    if isinstance(values, list):
        pass
    elif isinstance(values, (int, float)):
        values = [values]
    else:
        raise ValueError('values in wrong format')
    for i, ind in enumerate(indices):
        lattice[ind].KsL += values[i]

def calc_rms(vec):
    return float((np.mean(vec*vec))**0.5)

def rmk_correct_orbit(OrbitCorr_, inverse_jacobian_matrix=None, goal_orbit=None):
    """Orbit correction.

    Calculates the pseudo-inverse of orbit correction matrix via SVD
    and minimizes the residue vector [CODx@BPM, CODy@BPM].
    """
    if goal_orbit is None:
        nbpm = len(OrbitCorr_.respm.bpm_idx)
        goal_orbit = np.zeros(2 * nbpm)

    ismat = inverse_jacobian_matrix

    orb = OrbitCorr_.get_orbit()
    dorb = orb - goal_orbit
    bestfigm = OrbitCorr_.get_figm(dorb)
    if bestfigm < OrbitCorr_.params.tolerance:
        return OrbitCorr_.CORR_STATUS.Sucess

    for _ in range(OrbitCorr_.params.maxnriters):
        dkicks = -1*np.dot(ismat, dorb)
        kicks = OrbitCorr_._process_kicks(dkicks)
        OrbitCorr_.set_kicks(kicks)
        orb = OrbitCorr_.get_orbit()
        dorb = orb - goal_orbit
        figm = OrbitCorr_.get_figm(dorb)
        diff_figm = np.abs(bestfigm - figm)
        if figm < bestfigm:
            bestfigm = figm
        if diff_figm < OrbitCorr_.params.tolerance:
            break
    else:
        return OrbitCorr_.CORR_STATUS.Fail
    return OrbitCorr_.CORR_STATUS.Sucess

def calc_vdisp(model):
    return (pyaccel.tracking.find_orbit4(model, indices=BPMIDX, energy_offset=+1e-6)[2,:] - pyaccel.tracking.find_orbit4(model, indices=BPMIDX, energy_offset=-1e-6)[2,:])/(+2e-6)

# def test():
#     print('Hello World!')
#     return 0

# just a test 17/05/2023 at 15h55