"""'Iterations' module to run dispersion fitting and analisys"""

import numpy as _np
from apsuite.orbcorr import OrbitCorr as _OrbitCorr
from .misc_functions import apply_deltas as _apply_deltas
from .misc_functions import calc_vdisp as _calc_vdisp
from .misc_functions import rmk_correct_orbit as _rmk_correct_orbit 
from .misc_functions import calc_rms as _calc_rms
from .misc_functions import revoke_deltas as _revoke_deltas
from .std_si_data import STD_ORBCORR_INV_JACOB_MAT as _inv_jacob

_IJMAT = _inv_jacob()

def s_iter(model, disp_meta, base, n_iter, svals="auto", cut=1e-3, Orbcorr="auto"):
    imat, _, smat, _, c = calc_pinv(base.resp_mat(), svals, cut)
    print("N_svals =", c)
    deltas = _np.zeros(len(base.buttons()))
    disp = _np.zeros(160)
    if Orbcorr == "auto":
        oc = _OrbitCorr(model, acc="SI")
        oc_jacob_mat = oc.get_jacobian_matrix()
        oc_inv_jacob_mat = oc.get_inverse_matrix(jacobian_matrix=oc_jacob_mat)
        oc.params.maxnriters = 100
    elif isinstance(Orbcorr, tuple) and isinstance(Orbcorr[0], _OrbitCorr):
        oc = Orbcorr[0]
        oc_inv_jacob_mat = Orbcorr[1]
    else:
        raise ValueError(
            "Orbcorr in wrong format: should be a tuple of (_OrbitCorr obj, inverse_jacobian_matrix)"
        )
    for i in range(n_iter):
        disp = _calc_vdisp(model)
        diff = disp_meta - disp
        delta = imat @ diff
        deltas += delta
        _apply_deltas(model=model, base=base, deltas=deltas)
        _rmk_correct_orbit(oc, inverse_jacobian_matrix=oc_inv_jacob_mat)
    disp = _calc_vdisp(model)
    print(f"RMS residue = {_calc_rms(disp-disp_meta):f}")
    print(f"Corr. coef. = {_np.corrcoef(disp, disp_meta)[1,0]*100:.3f}%")
    _revoke_deltas(model, base)
    _rmk_correct_orbit(oc, inverse_jacobian_matrix=oc_inv_jacob_mat)
    return disp, deltas, smat, c


def f_iter_Y(
    model, disp_meta, base, n_iter, svals="auto", cut=1e-3, Orbcorr="auto"
):
    imat, _, smat, _, c = calc_pinv(base.resp_mat(), svals, cut)
    # print("N_svals =", c)
    deltas = _np.zeros(len(base.buttons()))
    disp = _np.zeros(160)
    for i in range(n_iter):
        for j, b in enumerate(base.buttons()):
            disp += deltas[j] * b.signature
        diff = disp_meta - disp
        delta = imat @ diff
        deltas += delta
    _apply_deltas(model, base, -deltas)
    if Orbcorr == "auto":
        oc = _OrbitCorr(model, acc="SI")
        oc_jacob_mat = oc.get_jacobian_matrix()
        oc_inv_jacob_mat = oc.get_inverse_matrix(jacobian_matrix=oc_jacob_mat)
        oc.params.maxnriters = 100
    elif isinstance(Orbcorr, tuple) and isinstance(Orbcorr[0], _OrbitCorr):
        oc = Orbcorr[0]
        oc_inv_jacob_mat = Orbcorr[1]
    else:
        raise ValueError("Orbcorr in wrong format: should be a tuple of (_OrbitCorr obj, inverse_jacobian_matrix)")
    _rmk_correct_orbit(oc, oc_inv_jacob_mat)
    disp = _calc_vdisp(model)
    # print(f"RMS residue = {_calc_rms(disp-disp_meta):f}")
    # print(f"Corr. coef. = {_np.corrcoef(disp, disp_meta)[1,0]*100:.3f}%")
    return disp, deltas, smat, c


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


def sf_iter_Y(
    disp_meta, base, n_iter, svals="auto", cut=1e-3
):
    imat, *_ = calc_pinv(base.resp_mat(), svals, cut)
    deltas = _np.zeros(len(base.buttons()))
    disp = _np.zeros(160)

    for i in range(n_iter):
        for j, b in enumerate(base.buttons()):
            disp += deltas[j] * b.signature
        diff = disp_meta - disp
        delta = imat @ diff
        deltas += delta

    for j, b in enumerate(base.buttons()):
        disp += deltas[j] * b.signature
    return disp, deltas

def dev_iter(model, disp_meta, base, n_iter, inv_jacob_mat='std', True_Apply=True, svals="auto", cut=1e-3):
    imat, _, smat, _, c = calc_pinv(base.resp_mat(), svals, cut)
    print("N_svals =", c)
    deltas = _np.zeros(len(base.buttons()))
    disp = _np.zeros(160)
    OrbcorrObj = _OrbitCorr(model, 'SI')
    if isinstance(inv_jacob_mat, str):
        if inv_jacob_mat == 'std':
            inv_jacob_mat = _IJMAT
        elif inv_jacob_mat == 'auto':
            _jacob_mat = OrbcorrObj.get_jacobian_matrix()
            inv_jacob_mat = OrbcorrObj.get_inverse_matrix(_jacob_mat)
        else:
            raise ValueError('inv_jacob_mat should be "std", "auto", or a "numpy.ndarray" with shape: (320, 281)')
    elif isinstance(inv_jacob_mat, (_np.ndarray)):
        pass
    else:
        raise ValueError('inv_jacob_mat should be "std", "auto", or a "numpy.ndarray" with shape: (320, 281)')
    for i in range(n_iter):
        disp = _calc_vdisp(model); 
        diff = disp_meta - disp;
        delta = imat @ diff; 
        deltas += delta
        _apply_deltas(model=model, base=base, deltas=deltas);
        _rmk_correct_orbit(OrbcorrObj, inverse_jacobian_matrix=inv_jacob_mat); 
    disp = _calc_vdisp(model)
    print(f"RMS residue = {_calc_rms(disp-disp_meta):f}")
    print(f"Corr. coef. = {_np.corrcoef(disp, disp_meta)[1,0]*100:.3f}%")
    if not True_Apply:
        _revoke_deltas(model, base)
        _rmk_correct_orbit(OrbcorrObj, inverse_jacobian_matrix=inv_jacob_mat); 
    return disp, deltas, smat, c