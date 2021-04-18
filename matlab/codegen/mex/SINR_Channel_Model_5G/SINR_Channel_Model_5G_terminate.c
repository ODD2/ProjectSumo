/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * SINR_Channel_Model_5G_terminate.c
 *
 * Code generation for function 'SINR_Channel_Model_5G_terminate'
 *
 */

/* Include files */
#include "SINR_Channel_Model_5G_terminate.h"
#include "SINR_Channel_Model_5G_data.h"
#include "_coder_SINR_Channel_Model_5G_mex.h"
#include "rt_nonfinite.h"

/* Function Definitions */
void SINR_Channel_Model_5G_atexit(void)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtEnterRtStackR2012b(&st);
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
  emlrtExitTimeCleanup(&emlrtContextGlobal);
}

void SINR_Channel_Model_5G_terminate(void)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  st.tls = emlrtRootTLSGlobal;
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/* End of code generation (SINR_Channel_Model_5G_terminate.c) */
