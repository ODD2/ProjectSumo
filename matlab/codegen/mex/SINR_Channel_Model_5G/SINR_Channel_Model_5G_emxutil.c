/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * SINR_Channel_Model_5G_emxutil.c
 *
 * Code generation for function 'SINR_Channel_Model_5G_emxutil'
 *
 */

/* Include files */
#include "SINR_Channel_Model_5G_emxutil.h"
#include "SINR_Channel_Model_5G_types.h"
#include "rt_nonfinite.h"
#include <string.h>

/* Function Definitions */
void emxEnsureCapacity_boolean_T(const emlrtStack *sp, emxArray_boolean_T
  *emxArray, int32_T oldNumel, const emlrtRTEInfo *srcLocation)
{
  int32_T i;
  int32_T newNumel;
  void *newData;
  if (oldNumel < 0) {
    oldNumel = 0;
  }

  newNumel = 1;
  for (i = 0; i < emxArray->numDimensions; i++) {
    newNumel = (int32_T)emlrtSizeMulR2012b((uint32_T)newNumel, (uint32_T)
      emxArray->size[i], srcLocation, sp);
  }

  if (newNumel > emxArray->allocatedSize) {
    i = emxArray->allocatedSize;
    if (i < 16) {
      i = 16;
    }

    while (i < newNumel) {
      if (i > 1073741823) {
        i = MAX_int32_T;
      } else {
        i *= 2;
      }
    }

    newData = emlrtCallocMex((uint32_T)i, sizeof(boolean_T));
    if (newData == NULL) {
      emlrtHeapAllocationErrorR2012b(srcLocation, sp);
    }

    if (emxArray->data != NULL) {
      memcpy(newData, emxArray->data, sizeof(boolean_T) * oldNumel);
      if (emxArray->canFreeData) {
        emlrtFreeMex(emxArray->data);
      }
    }

    emxArray->data = (boolean_T *)newData;
    emxArray->allocatedSize = i;
    emxArray->canFreeData = true;
  }
}

void emxEnsureCapacity_real_T(const emlrtStack *sp, emxArray_real_T *emxArray,
  int32_T oldNumel, const emlrtRTEInfo *srcLocation)
{
  int32_T i;
  int32_T newNumel;
  void *newData;
  if (oldNumel < 0) {
    oldNumel = 0;
  }

  newNumel = 1;
  for (i = 0; i < emxArray->numDimensions; i++) {
    newNumel = (int32_T)emlrtSizeMulR2012b((uint32_T)newNumel, (uint32_T)
      emxArray->size[i], srcLocation, sp);
  }

  if (newNumel > emxArray->allocatedSize) {
    i = emxArray->allocatedSize;
    if (i < 16) {
      i = 16;
    }

    while (i < newNumel) {
      if (i > 1073741823) {
        i = MAX_int32_T;
      } else {
        i *= 2;
      }
    }

    newData = emlrtCallocMex((uint32_T)i, sizeof(real_T));
    if (newData == NULL) {
      emlrtHeapAllocationErrorR2012b(srcLocation, sp);
    }

    if (emxArray->data != NULL) {
      memcpy(newData, emxArray->data, sizeof(real_T) * oldNumel);
      if (emxArray->canFreeData) {
        emlrtFreeMex(emxArray->data);
      }
    }

    emxArray->data = (real_T *)newData;
    emxArray->allocatedSize = i;
    emxArray->canFreeData = true;
  }
}

void emxFree_boolean_T(emxArray_boolean_T **pEmxArray)
{
  if (*pEmxArray != (emxArray_boolean_T *)NULL) {
    if (((*pEmxArray)->data != (boolean_T *)NULL) && (*pEmxArray)->canFreeData)
    {
      emlrtFreeMex((*pEmxArray)->data);
    }

    emlrtFreeMex((*pEmxArray)->size);
    emlrtFreeMex(*pEmxArray);
    *pEmxArray = (emxArray_boolean_T *)NULL;
  }
}

void emxFree_real_T(emxArray_real_T **pEmxArray)
{
  if (*pEmxArray != (emxArray_real_T *)NULL) {
    if (((*pEmxArray)->data != (real_T *)NULL) && (*pEmxArray)->canFreeData) {
      emlrtFreeMex((*pEmxArray)->data);
    }

    emlrtFreeMex((*pEmxArray)->size);
    emlrtFreeMex(*pEmxArray);
    *pEmxArray = (emxArray_real_T *)NULL;
  }
}

void emxInit_boolean_T(const emlrtStack *sp, emxArray_boolean_T **pEmxArray,
  int32_T numDimensions, const emlrtRTEInfo *srcLocation, boolean_T doPush)
{
  emxArray_boolean_T *emxArray;
  int32_T i;
  *pEmxArray = (emxArray_boolean_T *)emlrtMallocMex(sizeof(emxArray_boolean_T));
  if ((void *)*pEmxArray == NULL) {
    emlrtHeapAllocationErrorR2012b(srcLocation, sp);
  }

  if (doPush) {
    emlrtPushHeapReferenceStackR2012b(sp, (void *)pEmxArray, (void *)
      &emxFree_boolean_T);
  }

  emxArray = *pEmxArray;
  emxArray->data = (boolean_T *)NULL;
  emxArray->numDimensions = numDimensions;
  emxArray->size = (int32_T *)emlrtMallocMex(sizeof(int32_T) * numDimensions);
  if ((void *)emxArray->size == NULL) {
    emlrtHeapAllocationErrorR2012b(srcLocation, sp);
  }

  emxArray->allocatedSize = 0;
  emxArray->canFreeData = true;
  for (i = 0; i < numDimensions; i++) {
    emxArray->size[i] = 0;
  }
}

void emxInit_real_T(const emlrtStack *sp, emxArray_real_T **pEmxArray, int32_T
                    numDimensions, const emlrtRTEInfo *srcLocation, boolean_T
                    doPush)
{
  emxArray_real_T *emxArray;
  int32_T i;
  *pEmxArray = (emxArray_real_T *)emlrtMallocMex(sizeof(emxArray_real_T));
  if ((void *)*pEmxArray == NULL) {
    emlrtHeapAllocationErrorR2012b(srcLocation, sp);
  }

  if (doPush) {
    emlrtPushHeapReferenceStackR2012b(sp, (void *)pEmxArray, (void *)
      &emxFree_real_T);
  }

  emxArray = *pEmxArray;
  emxArray->data = (real_T *)NULL;
  emxArray->numDimensions = numDimensions;
  emxArray->size = (int32_T *)emlrtMallocMex(sizeof(int32_T) * numDimensions);
  if ((void *)emxArray->size == NULL) {
    emlrtHeapAllocationErrorR2012b(srcLocation, sp);
  }

  emxArray->allocatedSize = 0;
  emxArray->canFreeData = true;
  for (i = 0; i < numDimensions; i++) {
    emxArray->size[i] = 0;
  }
}

/* End of code generation (SINR_Channel_Model_5G_emxutil.c) */
