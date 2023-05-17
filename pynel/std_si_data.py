"""Standart 'PyModels: Sirius' model data collection"""

import pymodels as _pymodels
import numpy as _np
from pyaccel.lattice import find_spos as _find_spos

def create_std_si_model():
    model = _pymodels.si.create_accelerator()
    model.radiation_on = True
    model.vchamber_on = True
    model.cavity_on = True
    return model

MODEL_BASE = create_std_si_model()
SI_SPOS = _find_spos(MODEL_BASE, indices='closed').ravel()
SI_FAMDATA = _pymodels.si.families.get_family_data(MODEL_BASE)
SI_GIRDERS = _pymodels.si.families.get_girder_data(MODEL_BASE)
SI_SEXTUPOLES = _pymodels.si.families.families_sextupoles()
SI_DIPOLES = _pymodels.si.families.families_dipoles()
SI_QUADRUPOLES = _pymodels.si.families.families_quadrupoles()
BPMIDX = list(_np.array(SI_FAMDATA['BPM']['index']).ravel())
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

