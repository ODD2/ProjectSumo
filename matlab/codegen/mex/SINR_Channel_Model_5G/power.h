/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * power.h
 *
 * Code generation for function 'power'
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
void b_power(const emlrtStack *sp, const emxArray_real_T *b, emxArray_real_T *y);
void power(const emlrtStack *sp, const emxArray_real_T *a, emxArray_real_T *y);

/* End of code generation (power.h) */
