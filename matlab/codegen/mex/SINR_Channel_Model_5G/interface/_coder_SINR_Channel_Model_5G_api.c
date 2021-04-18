/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_SINR_Channel_Model_5G_api.c
 *
 * Code generation for function '_coder_SINR_Channel_Model_5G_api'
 *
 */

/* Include files */
#include "_coder_SINR_Channel_Model_5G_api.h"
#include "SINR_Channel_Model_5G.h"
#include "SINR_Channel_Model_5G_data.h"
#include "SINR_Channel_Model_5G_emxutil.h"
#include "SINR_Channel_Model_5G_types.h"
#include "rt_nonfinite.h"

/* Variable Definitions */
static emlrtRTEInfo pd_emlrtRTEI = { 1,/* lineNo */
  1,                                   /* colNo */
  "_coder_SINR_Channel_Model_5G_api",  /* fName */
  ""                                   /* pName */
};

/* Function Declarations */
static real_T b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId);
static const mxArray *b_emlrt_marshallOut(const real_T u);
static void c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *Intf_h_BS,
  const char_T *identifier, emxArray_real_T *y);
static void d_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId, emxArray_real_T *y);
static boolean_T e_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *UMA_notUMI_Model, const char_T *identifier);
static real_T emlrt_marshallIn(const emlrtStack *sp, const mxArray *D2D_dist,
  const char_T *identifier);
static const mxArray *emlrt_marshallOut(const real_T u_data[], const int32_T
  u_size[2]);
static boolean_T f_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u,
  const emlrtMsgIdentifier *parentId);
static real_T g_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src, const
  emlrtMsgIdentifier *msgId);
static void h_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src, const
  emlrtMsgIdentifier *msgId, emxArray_real_T *ret);
static boolean_T i_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId);

/* Function Definitions */
static real_T b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId)
{
  real_T y;
  y = g_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}

static const mxArray *b_emlrt_marshallOut(const real_T u)
{
  const mxArray *m;
  const mxArray *y;
  y = NULL;
  m = emlrtCreateDoubleScalar(u);
  emlrtAssign(&y, m);
  return y;
}

static void c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *Intf_h_BS,
  const char_T *identifier, emxArray_real_T *y)
{
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = (const char_T *)identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  d_emlrt_marshallIn(sp, emlrtAlias(Intf_h_BS), &thisId, y);
  emlrtDestroyArray(&Intf_h_BS);
}

static void d_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId, emxArray_real_T *y)
{
  h_emlrt_marshallIn(sp, emlrtAlias(u), parentId, y);
  emlrtDestroyArray(&u);
}

static boolean_T e_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *UMA_notUMI_Model, const char_T *identifier)
{
  emlrtMsgIdentifier thisId;
  boolean_T y;
  thisId.fIdentifier = (const char_T *)identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = f_emlrt_marshallIn(sp, emlrtAlias(UMA_notUMI_Model), &thisId);
  emlrtDestroyArray(&UMA_notUMI_Model);
  return y;
}

static real_T emlrt_marshallIn(const emlrtStack *sp, const mxArray *D2D_dist,
  const char_T *identifier)
{
  emlrtMsgIdentifier thisId;
  real_T y;
  thisId.fIdentifier = (const char_T *)identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = b_emlrt_marshallIn(sp, emlrtAlias(D2D_dist), &thisId);
  emlrtDestroyArray(&D2D_dist);
  return y;
}

static const mxArray *emlrt_marshallOut(const real_T u_data[], const int32_T
  u_size[2])
{
  static const int32_T iv[2] = { 0, 0 };

  const mxArray *m;
  const mxArray *y;
  y = NULL;
  m = emlrtCreateNumericArray(2, &iv[0], mxDOUBLE_CLASS, mxREAL);
  emlrtMxSetData((mxArray *)m, (void *)&u_data[0]);
  emlrtSetDimensions((mxArray *)m, u_size, 2);
  emlrtAssign(&y, m);
  return y;
}

static boolean_T f_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u,
  const emlrtMsgIdentifier *parentId)
{
  boolean_T y;
  y = i_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}

static real_T g_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src, const
  emlrtMsgIdentifier *msgId)
{
  static const int32_T dims = 0;
  real_T ret;
  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 0U, &dims);
  ret = *(real_T *)emlrtMxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

static void h_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src, const
  emlrtMsgIdentifier *msgId, emxArray_real_T *ret)
{
  static const int32_T dims[2] = { 1, -1 };

  int32_T iv[2];
  int32_T i;
  const boolean_T bv[2] = { false, true };

  emlrtCheckVsBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims, &bv[0],
    iv);
  ret->allocatedSize = iv[0] * iv[1];
  i = ret->size[0] * ret->size[1];
  ret->size[0] = iv[0];
  ret->size[1] = iv[1];
  emxEnsureCapacity_real_T(sp, ret, i, (emlrtRTEInfo *)NULL);
  ret->data = (real_T *)emlrtMxGetData(src);
  ret->canFreeData = false;
  emlrtDestroyArray(&src);
}

static boolean_T i_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId)
{
  static const int32_T dims = 0;
  boolean_T ret;
  emlrtCheckBuiltInR2012b(sp, msgId, src, "logical", false, 0U, &dims);
  ret = *emlrtMxGetLogicals(src);
  emlrtDestroyArray(&src);
  return ret;
}

void SINR_Channel_Model_5G_api(const mxArray * const prhs[17], int32_T nlhs,
  const mxArray *plhs[9])
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  emxArray_real_T *Intf_dist;
  emxArray_real_T *Intf_h_BS;
  emxArray_real_T *Intf_h_MS;
  emxArray_real_T *Intf_pwr_dBm;
  real_T (*CQI_out_data)[1];
  real_T CP;
  real_T D2D_dist;
  real_T DS_Desired;
  real_T DS_intf_dBm;
  real_T INTF_dBm;
  real_T Max_SINR_rx_dB_10;
  real_T Min_INTF_dBm;
  real_T Min_SINR_rx_dB_10;
  real_T Min_Spare_dBm;
  real_T PL_dB;
  real_T bandwidth;
  real_T fc;
  real_T h_BS;
  real_T h_MS;
  real_T min_tx_p_dBm;
  real_T min_tx_pwr_dBm;
  real_T tx_delta_dBm;
  real_T tx_p_dBm;
  int32_T CQI_out_size[2];
  boolean_T NOMA_Dir;
  boolean_T SINR_model;
  boolean_T UMA_notUMI_Model;
  st.tls = emlrtRootTLSGlobal;
  CQI_out_data = (real_T (*)[1])mxMalloc(sizeof(real_T [1]));
  emlrtHeapReferenceStackEnterFcnR2012b(&st);
  emxInit_real_T(&st, &Intf_h_BS, 2, &pd_emlrtRTEI, true);
  emxInit_real_T(&st, &Intf_h_MS, 2, &pd_emlrtRTEI, true);
  emxInit_real_T(&st, &Intf_dist, 2, &pd_emlrtRTEI, true);
  emxInit_real_T(&st, &Intf_pwr_dBm, 2, &pd_emlrtRTEI, true);

  /* Marshall function inputs */
  D2D_dist = emlrt_marshallIn(&st, emlrtAliasP(prhs[0]), "D2D_dist");
  h_BS = emlrt_marshallIn(&st, emlrtAliasP(prhs[1]), "h_BS");
  h_MS = emlrt_marshallIn(&st, emlrtAliasP(prhs[2]), "h_MS");
  fc = emlrt_marshallIn(&st, emlrtAliasP(prhs[3]), "fc");
  tx_p_dBm = emlrt_marshallIn(&st, emlrtAliasP(prhs[4]), "tx_p_dBm");
  bandwidth = emlrt_marshallIn(&st, emlrtAliasP(prhs[5]), "bandwidth");
  Intf_h_BS->canFreeData = false;
  c_emlrt_marshallIn(&st, emlrtAlias(prhs[6]), "Intf_h_BS", Intf_h_BS);
  Intf_h_MS->canFreeData = false;
  c_emlrt_marshallIn(&st, emlrtAlias(prhs[7]), "Intf_h_MS", Intf_h_MS);
  Intf_dist->canFreeData = false;
  c_emlrt_marshallIn(&st, emlrtAlias(prhs[8]), "Intf_dist", Intf_dist);
  Intf_pwr_dBm->canFreeData = false;
  c_emlrt_marshallIn(&st, emlrtAlias(prhs[9]), "Intf_pwr_dBm", Intf_pwr_dBm);
  DS_Desired = emlrt_marshallIn(&st, emlrtAliasP(prhs[10]), "DS_Desired");
  CP = emlrt_marshallIn(&st, emlrtAliasP(prhs[11]), "CP");
  UMA_notUMI_Model = e_emlrt_marshallIn(&st, emlrtAliasP(prhs[12]),
    "UMA_notUMI_Model");
  tx_delta_dBm = emlrt_marshallIn(&st, emlrtAliasP(prhs[13]), "tx_delta_dBm");
  min_tx_pwr_dBm = emlrt_marshallIn(&st, emlrtAliasP(prhs[14]), "min_tx_pwr_dBm");
  SINR_model = e_emlrt_marshallIn(&st, emlrtAliasP(prhs[15]), "SINR_model");
  NOMA_Dir = e_emlrt_marshallIn(&st, emlrtAliasP(prhs[16]), "NOMA_Dir");

  /* Invoke the target function */
  SINR_Channel_Model_5G(&st, D2D_dist, h_BS, h_MS, fc, tx_p_dBm, bandwidth,
                        Intf_h_BS, Intf_h_MS, Intf_dist, Intf_pwr_dBm,
                        DS_Desired, CP, UMA_notUMI_Model, tx_delta_dBm,
                        min_tx_pwr_dBm, SINR_model, NOMA_Dir, *CQI_out_data,
                        CQI_out_size, &Max_SINR_rx_dB_10, &min_tx_p_dBm, &PL_dB,
                        &INTF_dBm, &DS_intf_dBm, &Min_SINR_rx_dB_10,
                        &Min_INTF_dBm, &Min_Spare_dBm);

  /* Marshall function outputs */
  plhs[0] = emlrt_marshallOut(*CQI_out_data, CQI_out_size);
  emxFree_real_T(&Intf_pwr_dBm);
  emxFree_real_T(&Intf_dist);
  emxFree_real_T(&Intf_h_MS);
  emxFree_real_T(&Intf_h_BS);
  if (nlhs > 1) {
    plhs[1] = b_emlrt_marshallOut(Max_SINR_rx_dB_10);
  }

  if (nlhs > 2) {
    plhs[2] = b_emlrt_marshallOut(min_tx_p_dBm);
  }

  if (nlhs > 3) {
    plhs[3] = b_emlrt_marshallOut(PL_dB);
  }

  if (nlhs > 4) {
    plhs[4] = b_emlrt_marshallOut(INTF_dBm);
  }

  if (nlhs > 5) {
    plhs[5] = b_emlrt_marshallOut(DS_intf_dBm);
  }

  if (nlhs > 6) {
    plhs[6] = b_emlrt_marshallOut(Min_SINR_rx_dB_10);
  }

  if (nlhs > 7) {
    plhs[7] = b_emlrt_marshallOut(Min_INTF_dBm);
  }

  if (nlhs > 8) {
    plhs[8] = b_emlrt_marshallOut(Min_Spare_dBm);
  }

  emlrtHeapReferenceStackLeaveFcnR2012b(&st);
}

/* End of code generation (_coder_SINR_Channel_Model_5G_api.c) */
