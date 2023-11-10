"""Miscellaneous functions to work with 'Button' and 'Base' objects"""

import pyaccel as _pyaccel
import numpy as _np
from .std_si_data import BPMIDX as _BPMIDX_

_BPMIDX = _BPMIDX_()

_SET_FUNCS = {
        'dx':  _pyaccel.lattice.set_error_misalignment_x ,
        'dy':  _pyaccel.lattice.set_error_misalignment_y ,
        'dr':  _pyaccel.lattice.set_error_rotation_roll ,
        'drp': _pyaccel.lattice.set_error_rotation_pitch ,
        'dry': _pyaccel.lattice.set_error_rotation_yaw
        }

_GET_FUNCS = {
        'dx':  _pyaccel.lattice.get_error_misalignment_x ,
        'dy':  _pyaccel.lattice.get_error_misalignment_y ,
        'dr':  _pyaccel.lattice.get_error_rotation_roll ,
        'drp': _pyaccel.lattice.get_error_rotation_pitch ,
        'dry': _pyaccel.lattice.get_error_rotation_yaw
        }

_ADD_FUNCS = {
        'dx':  _pyaccel.lattice.add_error_misalignment_x ,
        'dy':  _pyaccel.lattice.add_error_misalignment_y ,
        'dr':  _pyaccel.lattice.add_error_rotation_roll ,
        'drp': _pyaccel.lattice.add_error_rotation_pitch ,
        'dry': _pyaccel.lattice.add_error_rotation_yaw
        }


def get_error(model, button):
    return _GET_FUNCS[button.dtype](model, indices=[button.indices[0]])

def get_errors(model, base):
    errors = []
    for button in base.buttons:
        errors.append(get_error(model, button))
    return _np.array(errors)



def set_error(model, button, error):
    if isinstance(error, (_np.int_, _np.float_, float, int)):
        _SET_FUNCS[button.dtype](model, indices=button.indices, values=error)
    elif len(error) == len(button.indices):
        _SET_FUNCS[button.dtype](model, indices=button.indices, values=error)
    else:
        raise ValueError('problem with deltas')
    
def set_errors(model, base, errors):
    if len(errors) != len(base):
        raise ValueError('"errors" size is incompatible with "base" size')
    for i, button in enumerate(base.buttons):
        set_error(model, button, errors[i])    
         
def add_delta_error(model, button, delta):
    if isinstance(delta, (_np.int_, _np.float_, float, int)):
        _ADD_FUNCS[button.dtype](model, indices=button.indices, values=delta)
    elif len(delta) == len(button.indices):
        _ADD_FUNCS[button.dtype](model, indices=button.indices, values=delta)
    else:
        raise ValueError('problem with delta')

def add_delta_errors(model, base, deltas):
    if len(deltas) != len(base):
        raise ValueError('"deltas" size is incompatible with "base" size')
    for i, button in enumerate(base.buttons):
        add_delta_error(model, button, deltas[i])    

def remove_delta_errors(model, base, deltas):
    for i, button in enumerate(base.buttons):
        _ADD_FUNCS[button.dtype](model, indices=button.indices, values=-deltas[i])

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
    return float(_np.std(vec))

def calc_vdisp(model, indices='bpm'):
    disp = calc_disp(model=model, indices=indices)
    return disp[int(len(disp)/2):]

def calc_hdisp(model, indices='bpm'):
    disp = calc_disp(model=model, indices=indices)
    return disp[:int(len(disp)/2)]

def calc_disp(model, indices='bpm'):
    if indices not in ['bpm','closed','open']:
        raise ValueError('Invalid indices parameter: should be "bpm" or "open" or "closed"!')
    if indices == 'bpm':
        indices = _BPMIDX
    orbp = _pyaccel.tracking.find_orbit4(model, indices=indices, energy_offset=+1e-6) 
    orbn = _pyaccel.tracking.find_orbit4(model, indices=indices, energy_offset=-1e-6)
    return _np.hstack([(orbp[0,:] - orbn[0,:])/(2e-6), (orbp[2,:] - orbn[2,:])/(2e-6)])

def rmk_correct_orbit(OrbitCorr_obj, jacobian_matrix, goal_orbit=None):
    """Orbit correction routine
        --> returns: 
        0 = Succes
        1 = Orb RMS Warning
        2 = Convergence Fail
        3 = Saturation Fail
    """
    if goal_orbit is None:
        nbpm = len(OrbitCorr_obj.respm.bpm_idx)
        goal_orbit = _np.zeros(2 * nbpm, dtype=float)

    jmat = jacobian_matrix
    if jmat is None:
        jmat = OrbitCorr_obj.get_jacobian_matrix()

    ismat = OrbitCorr_obj.get_inverse_matrix(jmat)

    orb = OrbitCorr_obj.get_orbit()
    dorb = orb - goal_orbit
    bestfigm = OrbitCorr_obj.get_figm(dorb)
    maxit = 0
    for _ in range(OrbitCorr_obj.params.maxnriters):
        dkicks = -1*_np.dot(ismat, dorb)
        kicks, saturation_flag = OrbitCorr_obj._process_kicks(dkicks)
        if saturation_flag:
            return OrbitCorr_obj.CORR_STATUS.SaturationFail, maxit
        OrbitCorr_obj.set_kicks(kicks)
        maxit += 1
        orb = OrbitCorr_obj.get_orbit()
        dorb = orb - goal_orbit
        figm = OrbitCorr_obj.get_figm(dorb)
        diff_figm = _np.abs(bestfigm - figm)
        if figm < bestfigm:
            bestfigm = figm
        if diff_figm < OrbitCorr_obj.params.convergencetol:
            if bestfigm <= OrbitCorr_obj.params.orbrmswarnthres:
                return OrbitCorr_obj.CORR_STATUS.Sucess, maxit
            else:
                return OrbitCorr_obj.CORR_STATUS.OrbRMSWarning, maxit
        if OrbitCorr_obj.params.updatejacobian:
            jmat = OrbitCorr_obj.get_jacobian_matrix()
            ismat = OrbitCorr_obj.get_inverse_matrix(jmat)
    return OrbitCorr_obj.CORR_STATUS.ConvergenceFail, maxit

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

__all__ = ('calc_pinv', 'calc_rms', 'calc_disp', 'calc_vdisp', 'calc_hdisp', 'set_error', 'set_errors', 'add_delta_error', 'add_delta_errors', 'remove_delta_errors', 'get_error', 'get_errors')
