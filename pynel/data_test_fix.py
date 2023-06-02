"""(COPY TEST) Standart 'PyModels: Sirius' model data collection"""

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

_sect_spos = [(518.3898999999924/20)*i for i in range(21)]
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
    """Return the standart Girders linked-elements names
    -> A girder name could be returned in the form: '_girder_BC_girder' 
    in the imaginary example of a single 'BC' in an hipothetical girder
    """
    return ['_girder_FC1_l082_QFA_l150_SFA0_l135_BPM_girder',
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