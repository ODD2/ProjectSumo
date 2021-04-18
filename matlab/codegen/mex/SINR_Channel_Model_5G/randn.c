/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * randn.c
 *
 * Code generation for function 'randn'
 *
 */

/* Include files */
#include "randn.h"
#include "SINR_Channel_Model_5G_emxutil.h"
#include "SINR_Channel_Model_5G_types.h"
#include "rt_nonfinite.h"

/* Variable Definitions */
static emlrtRTEInfo sc_emlrtRTEI = { 110,/* lineNo */
  24,                                  /* colNo */
  "randn",                             /* fName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/lib/matlab/randfun/randn.m"/* pName */
};

/* Function Definitions */
void b_randn(const emlrtStack *sp, const real_T varargin_1[2], emxArray_real_T
             *r)
{
  int32_T i;
  i = r->size[0] * r->size[1];
  r->size[0] = 1;
  r->size[1] = (int32_T)varargin_1[1];
  emxEnsureCapacity_real_T(sp, r, i, &sc_emlrtRTEI);
  if ((int32_T)varargin_1[1] != 0) {
    emlrtRandn(&r->data[0], (int32_T)varargin_1[1]);
  }
}

real_T randn(void)
{
  real_T r;
  emlrtRandn(&r, 1);
  return r;
}

/* End of code generation (randn.c) */
