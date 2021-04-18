/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * find.c
 *
 * Code generation for function 'find'
 *
 */

/* Include files */
#include "find.h"
#include "rt_nonfinite.h"

/* Function Definitions */
void eml_find(const boolean_T x[16], int32_T i_data[], int32_T i_size[2])
{
  int32_T idx;
  int32_T ii;
  boolean_T exitg1;
  idx = 0;
  i_size[0] = 1;
  i_size[1] = 1;
  ii = 16;
  exitg1 = false;
  while ((!exitg1) && (ii > 0)) {
    if (x[ii - 1]) {
      idx = 1;
      i_data[0] = ii;
      exitg1 = true;
    } else {
      ii--;
    }
  }

  if (idx == 0) {
    i_size[0] = 1;
    i_size[1] = 0;
  }
}

/* End of code generation (find.c) */
