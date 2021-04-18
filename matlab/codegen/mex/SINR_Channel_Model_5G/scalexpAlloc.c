/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * scalexpAlloc.c
 *
 * Code generation for function 'scalexpAlloc'
 *
 */

/* Include files */
#include "scalexpAlloc.h"
#include "SINR_Channel_Model_5G_types.h"
#include "rt_nonfinite.h"

/* Function Definitions */
boolean_T dimagree(const emxArray_real_T *z, const emxArray_real_T *varargin_1,
                   const emxArray_real_T *varargin_2)
{
  int32_T k;
  boolean_T b_p;
  boolean_T exitg1;
  boolean_T p;
  p = true;
  b_p = true;
  k = 0;
  exitg1 = false;
  while ((!exitg1) && (k < 2)) {
    if (z->size[k] != varargin_1->size[k]) {
      b_p = false;
      exitg1 = true;
    } else {
      k++;
    }
  }

  if (b_p) {
    b_p = true;
    k = 0;
    exitg1 = false;
    while ((!exitg1) && (k < 2)) {
      if (z->size[k] != varargin_2->size[k]) {
        b_p = false;
        exitg1 = true;
      } else {
        k++;
      }
    }

    if (!b_p) {
      p = false;
    }
  } else {
    p = false;
  }

  return p;
}

/* End of code generation (scalexpAlloc.c) */
