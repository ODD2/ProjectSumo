/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * ifWhileCond.c
 *
 * Code generation for function 'ifWhileCond'
 *
 */

/* Include files */
#include "ifWhileCond.h"
#include "SINR_Channel_Model_5G_data.h"
#include "SINR_Channel_Model_5G_types.h"
#include "eml_int_forloop_overflow_check.h"
#include "rt_nonfinite.h"

/* Variable Definitions */
static emlrtRSInfo mc_emlrtRSI = { 18, /* lineNo */
  "ifWhileCond",                       /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/ifWhileCond.m"/* pathName */
};

static emlrtRSInfo nc_emlrtRSI = { 31, /* lineNo */
  "checkNoNaNs",                       /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/ifWhileCond.m"/* pathName */
};

/* Function Definitions */
boolean_T ifWhileCond(const emlrtStack *sp, const emxArray_boolean_T *x)
{
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack st;
  int32_T k;
  boolean_T exitg1;
  boolean_T y;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  y = (x->size[1] != 0);
  if (y) {
    st.site = &mc_emlrtRSI;
    b_st.site = &nc_emlrtRSI;
    if ((1 <= x->size[1]) && (x->size[1] > 2147483646)) {
      c_st.site = &hc_emlrtRSI;
      check_forloop_overflow_error(&c_st);
    }

    k = 0;
    exitg1 = false;
    while ((!exitg1) && (k <= x->size[1] - 1)) {
      if (!x->data[k]) {
        y = false;
        exitg1 = true;
      } else {
        k++;
      }
    }
  }

  return y;
}

/* End of code generation (ifWhileCond.c) */
