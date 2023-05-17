"""Miscellaneous functions to work with 'Button' and 'Base' objects"""

import pyaccel as _pyaccel
import numpy as _np
from .std_si_data import BPMIDX as _BPMIDX

def apply_deltas(model, base, deltas):
    for i, button in enumerate(base.buttons()):
        func = pick_func(button.dtype)
        func(model, indices=button.indices, values=deltas[i])

def pick_func(dtype):
    if dtype == 'dx':
        func = _pyaccel.lattice.set_error_misalignment_x
    elif dtype == 'dy':
        func = _pyaccel.lattice.set_error_misalignment_y
    elif dtype == 'dr':
        func = _pyaccel.lattice.set_error_rotation_roll
    elif dtype == 'drp':
        func = _pyaccel.lattice.set_error_rotation_pitch
    elif dtype == 'dry':
        func = _pyaccel.lattice.set_error_rotation_yaw
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
    return float((_np.mean(vec*vec))**0.5)

def calc_vdisp(model):
    return (_pyaccel.tracking.find_orbit4(model, indices=_BPMIDX, energy_offset=+1e-6)[2,:] - _pyaccel.tracking.find_orbit4(model, indices=_BPMIDX, energy_offset=-1e-6)[2,:])/(+2e-6)

def rmk_correct_orbit(OrbitCorr_, inverse_jacobian_matrix=None, goal_orbit=None):
    if goal_orbit is None:
        nbpm = len(OrbitCorr_.respm.bpm_idx)
        goal_orbit = _np.zeros(2 * nbpm)

    ismat = inverse_jacobian_matrix

    orb = OrbitCorr_.get_orbit()
    dorb = orb - goal_orbit
    bestfigm = OrbitCorr_.get_figm(dorb)
    if bestfigm < OrbitCorr_.params.tolerance:
        return OrbitCorr_.CORR_STATUS.Sucess

    for _ in range(OrbitCorr_.params.maxnriters):
        dkicks = -1*_np.dot(ismat, dorb)
        kicks = OrbitCorr_._process_kicks(dkicks)
        OrbitCorr_.set_kicks(kicks)
        orb = OrbitCorr_.get_orbit()
        dorb = orb - goal_orbit
        figm = OrbitCorr_.get_figm(dorb)
        diff_figm = _np.abs(bestfigm - figm)
        if figm < bestfigm:
            bestfigm = figm
        if diff_figm < OrbitCorr_.params.tolerance:
            break
    else:
        return OrbitCorr_.CORR_STATUS.Fail
    return OrbitCorr_.CORR_STATUS.Sucess
