/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * log10.c
 *
 * Code generation for function 'log10'
 *
 */

/* Include files */
#include "log10.h"
#include "SINR_Channel_Model_5G_data.h"
#include "SINR_Channel_Model_5G_types.h"
#include "eml_int_forloop_overflow_check.h"
#include "rt_nonfinite.h"
#include "mwmathutil.h"

/* Variable Definitions */
static emlrtRSInfo wc_emlrtRSI = { 17, /* lineNo */
  "log10",                             /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/lib/matlab/elfun/log10.m"/* pathName */
};

/* Function Definitions */
void b_log10(const emlrtStack *sp, emxArray_real_T *x)
{
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack st;
  int32_T k;
  int32_T nx;
  boolean_T p;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  p = false;
  nx = x->size[1];
  for (k = 0; k < nx; k++) {
    if (p || (x->data[k] < 0.0)) {
      p = true;
    }
  }

  if (p) {
    emlrtErrorWithMessageIdR2018a(sp, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  st.site = &wc_emlrtRSI;
  nx = x->size[1];
  b_st.site = &gc_emlrtRSI;
  if ((1 <= x->size[1]) && (x->size[1] > 2147483646)) {
    c_st.site = &hc_emlrtRSI;
    check_forloop_overflow_error(&c_st);
  }

  for (k = 0; k < nx; k++) {
    x->data[k] = muDoubleScalarLog10(x->data[k]);
  }
}

/* End of code generation (log10.c) */
