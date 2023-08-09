"""Standart "PyModels Sirius model" data collection"""

import pymodels as _pymodels
import numpy as _np
from pyaccel.lattice import find_spos as _find_spos
import os as _os
from apsuite.orbcorr import OrbitCorr as _OrbitCorr
from copy import deepcopy

# file_path = _os.path.join(_os.path.dirname(__file__), 'pynel_inv_jacob_mat.txt')
_model = _pymodels.si.create_accelerator()
_model.radiation_on = True
_model.vchamber_on = True
_model.cavity_on = True

def MODEL_BASE():
    """Generate a standart (BASE) SIRIUS model with radiation, cavity and vchambers ON."""
    return deepcopy(_model)

_spos = _find_spos(_model, indices='closed')
def SI_SPOS():
    """Get the default SIRIUS longitudinal coordinates of the lattice elements"""
    return deepcopy(_spos)

_girders = _pymodels.si.families.get_girder_data(_model)
def SI_GIRDERS():
    """Get the default SIRIUS girders indices data"""
    return deepcopy(_girders)

def SI_SEXTUPOLES():
    """Get the default SIRIUS sextupoles names"""
    return ['SDA0','SDA1','SDA2','SDA3','SFA0','SFA1','SFA2',
            'SDB0','SDB1','SDB2','SDB3','SFB0','SFB1','SFB2',
            'SDP0','SDP1','SDP2','SDP3','SFP0','SFP1','SFP2']

def SI_DIPOLES():
    """Get the default SIRIUS dipoles names"""
    return ['B1', 'B2', 'BC']

def SI_QUADRUPOLES():
    """Get the default SIRIUS quadrupoles names"""
    return ['QFA','QDA',
            'QFB','QDB1','QDB2',
            'QFP','QDP1','QDP2',
            'Q1','Q2','Q3','Q4']

_famdata = _pymodels.si.families.get_family_data(_model)
_bpmidx = list(_np.array(_famdata['BPM']['index']).ravel())
def BPMIDX():
    """Get the default SIRIUS BPM's indices"""
    return deepcopy(_bpmidx)

def STD_ELEMS_HALB():
    """Get the default SIRIUS names of the elements in the 'HA-LB' or 'LB-HA' sectors"""
    return ['SFA0', 'QFA', 'SDA0', 'QDA', 'B1',
            'SDA1', 'Q1', 'SFA1', 'Q2', 'SDA2','B2',
            'SDA3', 'Q3', 'SFA2', 'Q4', 
            'BC',
            'Q4', 'SFB2', 'Q3', 'SDB3', 
            'B2','SDB2', 'Q2', 'SFB1', 'Q1', 'SDB1', 
            'B1','QDB1', 'SDB0', 'QFB', 'SFB0', 'QDB2']

def STD_ELEMS_LBLP():
    """Get the default SIRIUS names of the elements in the 'LB-LP' or 'LP-LB' sectors"""
    return ['QDB2', 'SFB0', 'QFB', 'SDB0', 'QDB1', 'B1',
            'SDB1', 'Q1', 'SFB1', 'Q2', 'SDB2', 'B2',
            'SDB3', 'Q3', 'SFB2', 'Q4',
            'BC',
            'Q4', 'SFP2', 'Q3', 'SDP3', 
            'B2','SDP2', 'Q2', 'SFP1', 'Q1', 'SDP1', 
            'B1','QDP1', 'SDP0', 'QFP', 'SFP0', 'QDP2']

def STD_TYPES():
    """Returns the default modification types: 
    'dr'  : Rotation roll misalignment (theta)
    'dx'  : Tranverse-horizontal misalignment (X)
    'dy'  : Tranverse-vertical misalignment (Y)
    'drp' : Rotation pitch misalignment 
    'dry' : Rotation yaw misalignment
    """
    #'dksl': Skew Gradient Strength
    return [ 'dx', 'dy', 'dr', 'drp', 'dry'] #, 'dksl'])

_all_sects = [i for i in range(1, 21)]
def STD_SECTS():
    """Returns the default sectors of SIRIUS ring (sectors from 1 to 20)"""
    return deepcopy(_all_sects)


def STD_ELEMS():
    """Get the default SIRIUS names of dipoles, quadrupoles and sextupoles in the ring"""
    return ['B1','B2','BC',
            'QFA','QDA',
            'QFB','QDB1','QDB2',
            'QFP','QDP1','QDP2',
            'Q1','Q2','Q3','Q4',
            'SDA0','SDA1','SDA2','SDA3','SFA0','SFA1','SFA2',
            'SDB0','SDB1','SDB2','SDB3','SFB0','SFB1','SFB2',
            'SDP0','SDP1','SDP2','SDP3','SFP0','SFP1','SFP2']

_sect_spos = [(_spos[-1]/20)*i for i in range(21)]
def SI_SECT_SPOS():
    """Get the longitudinal coordinates at the start of each sector"""
    return deepcopy(_sect_spos)

def SI_FAMDATA():
    """Get the default SIRIUS families data"""
    return deepcopy(_famdata)

def NothingHere():
    """You will find nothing here..."""
    print('Nothing Here!')

_jacob_mat = _np.loadtxt(_os.path.join(_os.path.dirname(__file__), 'pynel_inv_jacob_mat.txt')) # pre-saved jacobian for MODEL_BASE
#_jacob_mat = _OrbitCorr(_model, 'SI').get_jacobian_matrix()
def STD_ORBCORR_INV_JACOB_MAT():
    """Return the inverse matrix of the Orbit Correction Jacobian of the standart pymodels SIRIUS model"""
    return deepcopy(_jacob_mat)


def STD_GIRDER_NAMES():
    """ *** DISCONTINUED ***
    Return the standart Girders linked-elements names
    -> A girder name could be returned in the form: '_girder_BC_girder' 
    in the imaginary example of a single 'BC' in an hipothetical girder
    """
    return []

from mathphys.functions import load_pickle as _load_pickle
_path_full_buttons = _os.path.join(_os.path.dirname(__file__), "full_buttons_03-08-23.pickle")
_FULL_VERTC_BUTTONS = _load_pickle(_path_full_buttons)
def COMPLETE_BUTTONS_VERTICAL_DISPERSION():
    return deepcopy(_FULL_VERTC_BUTTONS)

