/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * SINR_Channel_Model_5G.h
 *
 * Code generation for function 'SINR_Channel_Model_5G'
 *
 */

#pragma once

/* Include files */
#include "SINR_Channel_Model_5G_types.h"
#include "rtwtypes.h"
#include "emlrt.h"
#include "mex.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Function Declarations */
void SINR_Channel_Model_5G(const emlrtStack *sp, real_T D2D_dist, real_T h_BS,
  real_T h_MS, real_T fc, real_T tx_p_dBm, real_T bandwidth, const
  emxArray_real_T *Intf_h_BS, const emxArray_real_T *Intf_h_MS, const
  emxArray_real_T *Intf_dist, const emxArray_real_T *Intf_pwr_dBm, real_T
  DS_Desired, real_T CP, boolean_T UMA_notUMI_Model, real_T tx_delta_dBm, real_T
  min_tx_pwr_dBm, boolean_T SINR_model, boolean_T NOMA_Dir, real_T CQI_out_data[],
  int32_T CQI_out_size[2], real_T *Max_SINR_rx_dB_10, real_T *min_tx_p_dBm,
  real_T *PL_dB, real_T *INTF_dBm, real_T *DS_intf_dBm, real_T
  *Min_SINR_rx_dB_10, real_T *Min_INTF_dBm, real_T *Min_Spare_dBm);

/* End of code generation (SINR_Channel_Model_5G.h) */
