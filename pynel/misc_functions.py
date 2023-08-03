"""Miscellaneous functions to work with 'Button' and 'Base' objects"""

import pyaccel as _pyaccel
import numpy as _np
from .std_si_data import BPMIDX as _BPMIDX_

_BPMIDX = _BPMIDX_()

def apply_deltas(model, base, deltas):
    for i, button in enumerate(base.buttons()):
        # func = pick_func(button.dtype)
        # func(model, indices=button.indices, values=deltas[i])
        pick_func(button.dtype)(model, indices=button.indices, values=deltas[i])

def revoke_deltas(model, base):
    for i, button in enumerate(base.buttons()):
        pick_func(button.dtype)(model, indices=button.indices, values=0.0)

# def pick_func(dtype):
#     if dtype == 'dx':
#         func = _pyaccel.lattice.set_error_misalignment_x
#     elif dtype == 'dy':
#         func = _pyaccel.lattice.set_error_misalignment_y
#     elif dtype == 'dr':
#         func = _pyaccel.lattice.set_error_rotation_roll
#     elif dtype == 'drp':
#         func = _pyaccel.lattice.set_error_rotation_pitch
#     elif dtype == 'dry':
#         func = _pyaccel.lattice.set_error_rotation_yaw
#     # elif dtype == 'dksl':
#     #     func = add_error_ksl
#     else:
#         raise TypeError('invalid dtype!')
#     return func

_FUNCS = {
        'dx': _pyaccel.lattice.set_error_misalignment_x,
        'dy': _pyaccel.lattice.set_error_misalignment_y,
        'dr': _pyaccel.lattice.set_error_rotation_roll,
        'drp': _pyaccel.lattice.set_error_rotation_pitch,
        'dry': _pyaccel.lattice.set_error_rotation_yaw
        }

def pick_func(dtype):
    return _FUNCS[dtype]

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

def calc_vdisp(model, indices='bpm'):
    if indices not in ['bpm','closed','open']:
        raise ValueError('Invalid indices parameter: should be "bpm" or "open" or "closed"!')
    if indices == 'bpm':
        indices = _BPMIDX
    orbp = _pyaccel.tracking.find_orbit4(model, indices=indices, energy_offset=+1e-6) 
    orbn = _pyaccel.tracking.find_orbit4(model, indices=indices, energy_offset=-1e-6)
    return (orbp[2,:] - orbn[2,:])/(2e-6)

def calc_hdisp(model, indices='bpm'):
    if indices not in ['bpm','closed','open']:
        raise ValueError('Invalid indices parameter: should be "bpm" or "open" or "closed"!')
    if indices == 'bpm':
        indices = _BPMIDX
    orbp = _pyaccel.tracking.find_orbit4(model, indices=indices, energy_offset=+1e-6) 
    orbn = _pyaccel.tracking.find_orbit4(model, indices=indices, energy_offset=-1e-6)
    return (orbp[0,:] - orbn[0,:])/(2e-6)

def calc_disp(model, indices='bpm'):
    if indices not in ['bpm','closed','open']:
        raise ValueError('Invalid indices parameter: should be "bpm" or "open" or "closed"!')
    if indices == 'bpm':
        indices = _BPMIDX
    orbp = _pyaccel.tracking.find_orbit4(model, indices=indices, energy_offset=+1e-6) 
    orbn = _pyaccel.tracking.find_orbit4(model, indices=indices, energy_offset=-1e-6)
    return _np.hstack([(orbp[0,:] - orbn[0,:])/(2e-6), (orbp[2,:] - orbn[2,:])/(2e-6)])

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

def calc_pinv(matrix, svals="auto", cut=1e-3):
    u, smat, vh = _np.linalg.svd(matrix, full_matrices=False)
    if svals == "auto":
        ismat = []
        c = 1
        for s in smat:
            if _np.log10(s / smat[0]) > _np.log10(cut):
                ismat.append(1 / s)
                c += 1
            else:
                ismat.append(0)
    elif isinstance(svals, int):
        ismat = 1 / smat
        ismat[svals:] *= 0.0
        c = svals
    elif svals == "all":
        ismat = 1 / smat
        c = len(smat)
    else:
        raise ValueError('svals should be "auto" or an integer')
    imat = vh.T @ _np.diag(ismat) @ u.T
    return imat, u, smat, vh, c

__all__ = ('calc_pinv', 'calc_rms', 'calc_disp', 'calc_vdisp', 'calc_hdisp', 'rmk_correct_orbit', 'apply_deltas', 'revoke_deltas')
