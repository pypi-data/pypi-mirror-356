#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""

from spacekernel.datamodel cimport COE_t


cdef double _2pi

# ========== ========== ========== ========== Conversion between SMA, MNM and ORP
cdef inline double c_orp_from_sma(const double sma, double GM) nogil

cdef inline double c_sma_from_orp(const double orp, double GM) nogil

cdef inline double c_mnm_from_sma(const double sma, double GM) nogil

cdef inline double c_sma_from_mnm(const double mnm, double GM) nogil

# ========== ========== ========== ========== Conversion between anomalies
cdef double c_eca_from_mea(const double mea, const double ecc) nogil

cdef inline double c_mea_from_eca(const double eca, const double ecc) nogil

cdef inline double c_eca_from_tra(const double tra, const double ecc) nogil

cdef inline double c_tra_from_eca(const double eca, const double ecc) nogil

cdef inline double c_tra_from_mea(const double mea, const double ecc) nogil

cdef inline double c_mea_from_tra(const double tra, const double ecc) nogil

# ========== ========== ========== ========== conversion using Apogee and Perigee
cdef inline double c_pge_from_sma_ecc(const double sma, const double ecc, const double Re) nogil

cdef inline double c_apg_from_sma_ecc(const double sma, const double ecc, const double Re) nogil

cdef inline double c_sma_from_pge_apg(const double pge, const double apg, const double Re) nogil

cdef inline double c_sma_from_ecc_pge(const double ecc, const double pge, const double Re) nogil

cdef inline double c_sma_from_ecc_apg(const double ecc, const double apg, const double Re) nogil

cdef inline double c_ecc_from_pge_apg(const double pge, const double apg, const double Re) nogil

cdef inline double c_ecc_from_sma_pge(const double sma, const double pge, const double Re) nogil

cdef inline double c_ecc_from_sma_apg(const double sma, const double apg, const double Re) nogil

# ========== ========== ========== ==========  COE -> SV
cdef void c_coe_from_sv(const double[3] r,
                        const double[3] v,
                        const double GM,
                        COE_t* coe) nogil

cdef void c_sv_from_coe(const COE_t coe,
                        const double GM,
                        double[3] r,
                        double[3] v) nogil