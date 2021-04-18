/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * SINR_Channel_Model_5G_initialize.c
 *
 * Code generation for function 'SINR_Channel_Model_5G_initialize'
 *
 */

/* Include files */
#include "SINR_Channel_Model_5G_initialize.h"
#include "SINR_Channel_Model_5G_data.h"
#include "_coder_SINR_Channel_Model_5G_mex.h"
#include "rt_nonfinite.h"

/* Function Definitions */
void SINR_Channel_Model_5G_initialize(void)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  mex_InitInfAndNan();
  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  emlrtLicenseCheckR2012b(&st, "statistics_toolbox", 2);
  emlrtFirstTimeR2012b(emlrtRootTLSGlobal);
}

/* End of code generation (SINR_Channel_Model_5G_initialize.c) */
