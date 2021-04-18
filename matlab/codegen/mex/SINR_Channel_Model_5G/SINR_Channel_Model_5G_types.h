/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * SINR_Channel_Model_5G_types.h
 *
 * Code generation for function 'SINR_Channel_Model_5G'
 *
 */

#pragma once

/* Include files */
#include "rtwtypes.h"
#include "emlrt.h"

/* Type Definitions */
#ifndef struct_emxArray_real_T
#define struct_emxArray_real_T

struct emxArray_real_T
{
  real_T *data;
  int32_T *size;
  int32_T allocatedSize;
  int32_T numDimensions;
  boolean_T canFreeData;
};

#endif                                 /*struct_emxArray_real_T*/

#ifndef typedef_emxArray_real_T
#define typedef_emxArray_real_T

typedef struct emxArray_real_T emxArray_real_T;

#endif                                 /*typedef_emxArray_real_T*/

#ifndef struct_emxArray_boolean_T
#define struct_emxArray_boolean_T

struct emxArray_boolean_T
{
  boolean_T *data;
  int32_T *size;
  int32_T allocatedSize;
  int32_T numDimensions;
  boolean_T canFreeData;
};

#endif                                 /*struct_emxArray_boolean_T*/

#ifndef typedef_emxArray_boolean_T
#define typedef_emxArray_boolean_T

typedef struct emxArray_boolean_T emxArray_boolean_T;

#endif                                 /*typedef_emxArray_boolean_T*/

/* End of code generation (SINR_Channel_Model_5G_types.h) */
