/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * power.c
 *
 * Code generation for function 'power'
 *
 */

/* Include files */
#include "power.h"
#include "SINR_Channel_Model_5G_data.h"
#include "SINR_Channel_Model_5G_emxutil.h"
#include "SINR_Channel_Model_5G_types.h"
#include "eml_int_forloop_overflow_check.h"
#include "rt_nonfinite.h"
#include "mwmathutil.h"

/* Variable Definitions */
static emlrtRSInfo sd_emlrtRSI = { 174,/* lineNo */
  "flatIter",                          /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/applyBinaryScalarFunction.m"/* pathName */
};

/* Function Definitions */
void b_power(const emlrtStack *sp, const emxArray_real_T *b, emxArray_real_T *y)
{
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  emlrtStack e_st;
  emlrtStack st;
  int32_T k;
  int32_T nx;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &pb_emlrtRSI;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  e_st.prev = &d_st;
  e_st.tls = d_st.tls;
  b_st.site = &pc_emlrtRSI;
  nx = y->size[0] * y->size[1];
  y->size[0] = 1;
  y->size[1] = b->size[1];
  emxEnsureCapacity_real_T(&b_st, y, nx, &pb_emlrtRTEI);
  c_st.site = &qc_emlrtRSI;
  nx = b->size[1];
  d_st.site = &sd_emlrtRSI;
  if ((1 <= b->size[1]) && (b->size[1] > 2147483646)) {
    e_st.site = &hc_emlrtRSI;
    check_forloop_overflow_error(&e_st);
  }

  for (k = 0; k < nx; k++) {
    y->data[k] = muDoubleScalarPower(10.0, b->data[k]);
  }
}

void power(const emlrtStack *sp, const emxArray_real_T *a, emxArray_real_T *y)
{
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  emlrtStack e_st;
  emlrtStack st;
  real_T d;
  int32_T k;
  int32_T nx;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &pb_emlrtRSI;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  e_st.prev = &d_st;
  e_st.tls = d_st.tls;
  b_st.site = &pc_emlrtRSI;
  nx = y->size[0] * y->size[1];
  y->size[0] = 1;
  y->size[1] = a->size[1];
  emxEnsureCapacity_real_T(&b_st, y, nx, &pb_emlrtRTEI);
  c_st.site = &qc_emlrtRSI;
  nx = a->size[1];
  d_st.site = &rc_emlrtRSI;
  if ((1 <= a->size[1]) && (a->size[1] > 2147483646)) {
    e_st.site = &hc_emlrtRSI;
    check_forloop_overflow_error(&e_st);
  }

  for (k = 0; k < nx; k++) {
    d = a->data[k];
    y->data[k] = d * d;
  }
}

/* End of code generation (power.c) */
