/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_SINR_Channel_Model_5G_mex.c
 *
 * Code generation for function '_coder_SINR_Channel_Model_5G_mex'
 *
 */

/* Include files */
#include "_coder_SINR_Channel_Model_5G_mex.h"
#include "SINR_Channel_Model_5G_data.h"
#include "SINR_Channel_Model_5G_initialize.h"
#include "SINR_Channel_Model_5G_terminate.h"
#include "_coder_SINR_Channel_Model_5G_api.h"
#include "rt_nonfinite.h"

/* Function Definitions */
void SINR_Channel_Model_5G_mexFunction(int32_T nlhs, mxArray *plhs[9], int32_T
  nrhs, const mxArray *prhs[17])
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  const mxArray *outputs[9];
  int32_T b_nlhs;
  st.tls = emlrtRootTLSGlobal;

  /* Check for proper number of arguments. */
  if (nrhs != 17) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:WrongNumberOfInputs", 5, 12, 17, 4,
                        21, "SINR_Channel_Model_5G");
  }

  if (nlhs > 9) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:TooManyOutputArguments", 3, 4, 21,
                        "SINR_Channel_Model_5G");
  }

  /* Call the function. */
  SINR_Channel_Model_5G_api(prhs, nlhs, outputs);

  /* Copy over outputs to the caller. */
  if (nlhs < 1) {
    b_nlhs = 1;
  } else {
    b_nlhs = nlhs;
  }

  emlrtReturnArrays(b_nlhs, plhs, outputs);
}

void mexFunction(int32_T nlhs, mxArray *plhs[], int32_T nrhs, const mxArray
                 *prhs[])
{
  mexAtExit(&SINR_Channel_Model_5G_atexit);

  /* Module initialization. */
  SINR_Channel_Model_5G_initialize();

  /* Dispatch the entry-point. */
  SINR_Channel_Model_5G_mexFunction(nlhs, plhs, nrhs, prhs);

  /* Module termination. */
  SINR_Channel_Model_5G_terminate();
}

emlrtCTX mexFunctionCreateRootTLS(void)
{
  emlrtCreateRootTLS(&emlrtRootTLSGlobal, &emlrtContextGlobal, NULL, 1);
  return emlrtRootTLSGlobal;
}

/* End of code generation (_coder_SINR_Channel_Model_5G_mex.c) */
