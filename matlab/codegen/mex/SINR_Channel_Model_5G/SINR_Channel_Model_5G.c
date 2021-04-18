/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * SINR_Channel_Model_5G.c
 *
 * Code generation for function 'SINR_Channel_Model_5G'
 *
 */

/* Include files */
#include "SINR_Channel_Model_5G.h"
#include "SINR_Channel_Model_5G_data.h"
#include "SINR_Channel_Model_5G_emxutil.h"
#include "SINR_Channel_Model_5G_types.h"
#include "eml_int_forloop_overflow_check.h"
#include "exp.h"
#include "find.h"
#include "ifWhileCond.h"
#include "log10.h"
#include "power.h"
#include "rand.h"
#include "randn.h"
#include "rt_nonfinite.h"
#include "scalexpAlloc.h"
#include "sqrt.h"
#include "sum.h"
#include "mwmathutil.h"

/* Variable Definitions */
static emlrtRSInfo emlrtRSI = { 101,   /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo b_emlrtRSI = { 102, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo c_emlrtRSI = { 103, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo d_emlrtRSI = { 107, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo e_emlrtRSI = { 109, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo f_emlrtRSI = { 110, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo g_emlrtRSI = { 117, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo h_emlrtRSI = { 118, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo i_emlrtRSI = { 119, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo j_emlrtRSI = { 121, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo k_emlrtRSI = { 123, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo l_emlrtRSI = { 124, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo m_emlrtRSI = { 125, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo n_emlrtRSI = { 156, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo o_emlrtRSI = { 159, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo p_emlrtRSI = { 161, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo q_emlrtRSI = { 162, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo r_emlrtRSI = { 163, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo s_emlrtRSI = { 168, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo t_emlrtRSI = { 171, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo u_emlrtRSI = { 172, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo v_emlrtRSI = { 175, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo w_emlrtRSI = { 178, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo x_emlrtRSI = { 181, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo y_emlrtRSI = { 184, /* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo ab_emlrtRSI = { 187,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo bb_emlrtRSI = { 198,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo cb_emlrtRSI = { 223,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo db_emlrtRSI = { 228,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo eb_emlrtRSI = { 232,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo fb_emlrtRSI = { 235,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo gb_emlrtRSI = { 240,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo hb_emlrtRSI = { 250,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo ib_emlrtRSI = { 251,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo jb_emlrtRSI = { 255,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo kb_emlrtRSI = { 258,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo lb_emlrtRSI = { 262,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo mb_emlrtRSI = { 265,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo nb_emlrtRSI = { 271,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo ob_emlrtRSI = { 274,/* lineNo */
  "SINR_Channel_Model_5G",             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo rb_emlrtRSI = { 387,/* lineNo */
  "PrLOS",                             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo sb_emlrtRSI = { 390,/* lineNo */
  "PrLOS",                             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo tb_emlrtRSI = { 304,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo ub_emlrtRSI = { 310,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo vb_emlrtRSI = { 312,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo wb_emlrtRSI = { 314,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo xb_emlrtRSI = { 315,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo yb_emlrtRSI = { 325,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo ac_emlrtRSI = { 326,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo bc_emlrtRSI = { 329,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo cc_emlrtRSI = { 11, /* lineNo */
  "normrnd",                           /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/stats/eml/normrnd.m"/* pathName */
};

static emlrtRSInfo dc_emlrtRSI = { 1,  /* lineNo */
  "rnd",                               /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/rnd.p"/* pathName */
};

static emlrtRSInfo ec_emlrtRSI = { 1,  /* lineNo */
  "normrnd",                           /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/private/normrnd.p"/* pathName */
};

static emlrtRSInfo ic_emlrtRSI = { 381,/* lineNo */
  "PrLOS",                             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo jc_emlrtRSI = { 389,/* lineNo */
  "PrLOS",                             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo kc_emlrtRSI = { 393,/* lineNo */
  "PrLOS",                             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo lc_emlrtRSI = { 396,/* lineNo */
  "PrLOS",                             /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo sc_emlrtRSI = { 317,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo tc_emlrtRSI = { 323,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo uc_emlrtRSI = { 327,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo vc_emlrtRSI = { 330,/* lineNo */
  "UMA_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo xc_emlrtRSI = { 14, /* lineNo */
  "max",                               /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/lib/matlab/datafun/max.m"/* pathName */
};

static emlrtRSInfo yc_emlrtRSI = { 29, /* lineNo */
  "minOrMax",                          /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/minOrMax.m"/* pathName */
};

static emlrtRSInfo ad_emlrtRSI = { 58, /* lineNo */
  "maximum2",                          /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/minOrMax.m"/* pathName */
};

static emlrtRSInfo bd_emlrtRSI = { 64, /* lineNo */
  "binaryMinOrMax",                    /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/binaryMinOrMax.m"/* pathName */
};

static emlrtRSInfo cd_emlrtRSI = { 46, /* lineNo */
  "applyBinaryScalarFunction",         /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/applyBinaryScalarFunction.m"/* pathName */
};

static emlrtRSInfo dd_emlrtRSI = { 202,/* lineNo */
  "flatIter",                          /* fcnName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/applyBinaryScalarFunction.m"/* pathName */
};

static emlrtRSInfo ed_emlrtRSI = { 342,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo fd_emlrtRSI = { 348,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo gd_emlrtRSI = { 350,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo hd_emlrtRSI = { 352,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo id_emlrtRSI = { 353,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo jd_emlrtRSI = { 363,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo kd_emlrtRSI = { 364,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo ld_emlrtRSI = { 367,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo md_emlrtRSI = { 355,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo nd_emlrtRSI = { 361,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo od_emlrtRSI = { 365,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo pd_emlrtRSI = { 368,/* lineNo */
  "UMI_Model",                         /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo qd_emlrtRSI = { 295,/* lineNo */
  "Calc_DS_Inteference",               /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtRSInfo rd_emlrtRSI = { 298,/* lineNo */
  "Calc_DS_Inteference",               /* fcnName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pathName */
};

static emlrtECInfo emlrtECI = { 2,     /* nDims */
  295,                                 /* lineNo */
  34,                                  /* colNo */
  "Calc_DS_Inteference",               /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo b_emlrtECI = { 2,   /* nDims */
  294,                                 /* lineNo */
  26,                                  /* colNo */
  "Calc_DS_Inteference",               /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo c_emlrtECI = { 2,   /* nDims */
  265,                                 /* lineNo */
  8,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo emlrtRTEI = { 227, /* lineNo */
  20,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo d_emlrtECI = { 2,   /* nDims */
  161,                                 /* lineNo */
  18,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo e_emlrtECI = { 2,   /* nDims */
  121,                                 /* lineNo */
  26,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo f_emlrtECI = { 2,   /* nDims */
  121,                                 /* lineNo */
  42,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo g_emlrtECI = { 2,   /* nDims */
  107,                                 /* lineNo */
  26,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo h_emlrtECI = { 2,   /* nDims */
  107,                                 /* lineNo */
  49,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo i_emlrtECI = { 2,   /* nDims */
  107,                                 /* lineNo */
  75,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo j_emlrtECI = { 2,   /* nDims */
  107,                                 /* lineNo */
  50,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo k_emlrtECI = { 2,   /* nDims */
  396,                                 /* lineNo */
  27,                                  /* colNo */
  "PrLOS",                             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo l_emlrtECI = { 2,   /* nDims */
  396,                                 /* lineNo */
  48,                                  /* colNo */
  "PrLOS",                             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo m_emlrtECI = { 2,   /* nDims */
  389,                                 /* lineNo */
  26,                                  /* colNo */
  "PrLOS",                             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo n_emlrtECI = { 2,   /* nDims */
  390,                                 /* lineNo */
  32,                                  /* colNo */
  "PrLOS",                             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo o_emlrtECI = { 2,   /* nDims */
  389,                                 /* lineNo */
  27,                                  /* colNo */
  "PrLOS",                             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo p_emlrtECI = { 2,   /* nDims */
  389,                                 /* lineNo */
  48,                                  /* colNo */
  "PrLOS",                             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo d_emlrtRTEI = { 19,/* lineNo */
  23,                                  /* colNo */
  "scalexpAlloc",                      /* fName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/scalexpAlloc.m"/* pName */
};

static emlrtECInfo q_emlrtECI = { 2,   /* nDims */
  326,                                 /* lineNo */
  23,                                  /* colNo */
  "UMA_Model",                         /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo r_emlrtECI = { 2,   /* nDims */
  312,                                 /* lineNo */
  26,                                  /* colNo */
  "UMA_Model",                         /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo s_emlrtECI = { 2,   /* nDims */
  312,                                 /* lineNo */
  92,                                  /* colNo */
  "UMA_Model",                         /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo t_emlrtECI = { 2,   /* nDims */
  310,                                 /* lineNo */
  24,                                  /* colNo */
  "UMA_Model",                         /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo u_emlrtECI = { 2,   /* nDims */
  364,                                 /* lineNo */
  23,                                  /* colNo */
  "UMI_Model",                         /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo v_emlrtECI = { 2,   /* nDims */
  350,                                 /* lineNo */
  26,                                  /* colNo */
  "UMI_Model",                         /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo w_emlrtECI = { 2,   /* nDims */
  350,                                 /* lineNo */
  93,                                  /* colNo */
  "UMI_Model",                         /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtECInfo x_emlrtECI = { 2,   /* nDims */
  348,                                 /* lineNo */
  24,                                  /* colNo */
  "UMI_Model",                         /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo g_emlrtRTEI = { 121,/* lineNo */
  42,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo h_emlrtRTEI = { 121,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo i_emlrtRTEI = { 125,/* lineNo */
  8,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo j_emlrtRTEI = { 126,/* lineNo */
  9,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo k_emlrtRTEI = { 288,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo l_emlrtRTEI = { 161,/* lineNo */
  23,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo m_emlrtRTEI = { 295,/* lineNo */
  60,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo n_emlrtRTEI = { 161,/* lineNo */
  48,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo o_emlrtRTEI = { 295,/* lineNo */
  13,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo p_emlrtRTEI = { 107,/* lineNo */
  26,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo q_emlrtRTEI = { 161,/* lineNo */
  1,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo r_emlrtRTEI = { 107,/* lineNo */
  50,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo s_emlrtRTEI = { 162,/* lineNo */
  4,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo t_emlrtRTEI = { 107,/* lineNo */
  49,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo u_emlrtRTEI = { 165,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo v_emlrtRTEI = { 163,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo w_emlrtRTEI = { 107,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo x_emlrtRTEI = { 181,/* lineNo */
  4,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo y_emlrtRTEI = { 184,/* lineNo */
  29,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ab_emlrtRTEI = { 255,/* lineNo */
  8,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo bb_emlrtRTEI = { 258,/* lineNo */
  33,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo cb_emlrtRTEI = { 109,/* lineNo */
  6,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo db_emlrtRTEI = { 110,/* lineNo */
  6,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo eb_emlrtRTEI = { 393,/* lineNo */
  12,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo fb_emlrtRTEI = { 381,/* lineNo */
  12,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo gb_emlrtRTEI = { 396,/* lineNo */
  48,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo hb_emlrtRTEI = { 394,/* lineNo */
  13,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ib_emlrtRTEI = { 382,/* lineNo */
  13,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo jb_emlrtRTEI = { 389,/* lineNo */
  48,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo kb_emlrtRTEI = { 396,/* lineNo */
  77,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo lb_emlrtRTEI = { 389,/* lineNo */
  77,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo mb_emlrtRTEI = { 389,/* lineNo */
  27,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo nb_emlrtRTEI = { 396,/* lineNo */
  13,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ob_emlrtRTEI = { 390,/* lineNo */
  40,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo qb_emlrtRTEI = { 390,/* lineNo */
  33,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo rb_emlrtRTEI = { 390,/* lineNo */
  66,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo sb_emlrtRTEI = { 390,/* lineNo */
  32,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo tb_emlrtRTEI = { 389,/* lineNo */
  13,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ub_emlrtRTEI = { 379,/* lineNo */
  27,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo vb_emlrtRTEI = { 304,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo wb_emlrtRTEI = { 310,/* lineNo */
  34,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo xb_emlrtRTEI = { 310,/* lineNo */
  31,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo yb_emlrtRTEI = { 312,/* lineNo */
  37,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ac_emlrtRTEI = { 312,/* lineNo */
  33,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo bc_emlrtRTEI = { 312,/* lineNo */
  92,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo cc_emlrtRTEI = { 312,/* lineNo */
  72,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo dc_emlrtRTEI = { 312,/* lineNo */
  70,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ec_emlrtRTEI = { 312,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo fc_emlrtRTEI = { 315,/* lineNo */
  48,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo gc_emlrtRTEI = { 315,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo hc_emlrtRTEI = { 317,/* lineNo */
  8,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ic_emlrtRTEI = { 318,/* lineNo */
  9,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo jc_emlrtRTEI = { 17,/* lineNo */
  9,                                   /* colNo */
  "scalexpAlloc",                      /* fName */
  "/usr/local/MATLAB/R2020b/toolbox/eml/eml/+coder/+internal/scalexpAlloc.m"/* pName */
};

static emlrtRTEInfo kc_emlrtRTEI = { 325,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo lc_emlrtRTEI = { 326,/* lineNo */
  37,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo mc_emlrtRTEI = { 326,/* lineNo */
  31,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo nc_emlrtRTEI = { 326,/* lineNo */
  66,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo oc_emlrtRTEI = { 326,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo pc_emlrtRTEI = { 330,/* lineNo */
  8,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo qc_emlrtRTEI = { 331,/* lineNo */
  9,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo rc_emlrtRTEI = { 323,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo tc_emlrtRTEI = { 342,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo uc_emlrtRTEI = { 348,/* lineNo */
  34,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo vc_emlrtRTEI = { 348,/* lineNo */
  31,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo wc_emlrtRTEI = { 350,/* lineNo */
  36,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo xc_emlrtRTEI = { 350,/* lineNo */
  33,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo yc_emlrtRTEI = { 350,/* lineNo */
  93,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ad_emlrtRTEI = { 350,/* lineNo */
  73,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo bd_emlrtRTEI = { 350,/* lineNo */
  69,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo cd_emlrtRTEI = { 350,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo dd_emlrtRTEI = { 353,/* lineNo */
  49,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ed_emlrtRTEI = { 353,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo fd_emlrtRTEI = { 355,/* lineNo */
  8,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo gd_emlrtRTEI = { 356,/* lineNo */
  9,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo hd_emlrtRTEI = { 363,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo id_emlrtRTEI = { 364,/* lineNo */
  35,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo jd_emlrtRTEI = { 364,/* lineNo */
  30,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo kd_emlrtRTEI = { 364,/* lineNo */
  66,                                  /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo ld_emlrtRTEI = { 364,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo md_emlrtRTEI = { 368,/* lineNo */
  8,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo nd_emlrtRTEI = { 369,/* lineNo */
  9,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

static emlrtRTEInfo od_emlrtRTEI = { 361,/* lineNo */
  5,                                   /* colNo */
  "SINR_Channel_Model_5G",             /* fName */
  "/home/OD/repos/ProjectSumo/matlab/SINR_Channel_Model_5G.m"/* pName */
};

/* Function Declarations */
static real_T Calc_DS_Inteference(const emlrtStack *sp, real_T tx_p_dBm, const
  real_T TDL_C_SCALED[48], real_T CP, real_T PL_tot_sig);
static real_T PrLOS(real_T D2D_dist_out, real_T MS_t, boolean_T UMA_notUMi);
static void UMA_Model(const emlrtStack *sp, real_T fc, const emxArray_real_T
                      *D3D_dist, const emxArray_real_T *BS_t, const
                      emxArray_real_T *MS_t, real_T d_bp_pl, const
                      emxArray_real_T *pLOS, emxArray_real_T *sig);
static real_T UMI_Model(const emlrtStack *sp, real_T fc, real_T D3D_dist, real_T
  BS_t, real_T MS_t, real_T d_bp_pl, real_T pLOS);
static void b_PrLOS(const emlrtStack *sp, const emxArray_real_T *D2D_dist_out,
                    real_T MS_t, boolean_T UMA_notUMi, emxArray_real_T
                    *Prob_LOS_sig);
static void b_UMI_Model(const emlrtStack *sp, real_T fc, const emxArray_real_T
  *D3D_dist, const emxArray_real_T *BS_t, const emxArray_real_T *MS_t, real_T
  d_bp_pl, const emxArray_real_T *pLOS, emxArray_real_T *sig);

/* Function Definitions */
static real_T Calc_DS_Inteference(const emlrtStack *sp, real_T tx_p_dBm, const
  real_T TDL_C_SCALED[48], real_T CP, real_T PL_tot_sig)
{
  real_T sum_DS_intf_MP_mW;
  int32_T i;

  /* This function determine the multipath loss experienced by a single. */
  /* This loss is modeled as interference */
  /* Assume frequency flat fading */
  sum_DS_intf_MP_mW = 0.0;

  /* Worst Case attenuation SINR_model    */
  for (i = 0; i < 24; i++) {
    /* Always positive DS scaled */
    /* Act as attenutation, negative gain */
    if (TDL_C_SCALED[i] > CP) {
      /* Only account for elements which are not filtered out by the CP */
      /* Scaled is negative, so we add */
      sum_DS_intf_MP_mW += muDoubleScalarPower(10.0, ((tx_p_dBm - PL_tot_sig) -
        muDoubleScalarAbs(TDL_C_SCALED[i + 24])) / 10.0);
    }

    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  return sum_DS_intf_MP_mW;
}

static real_T PrLOS(real_T D2D_dist_out, real_T MS_t, boolean_T UMA_notUMi)
{
  real_T C;
  real_T Prob_LOS_sig;
  if (UMA_notUMi) {
    if (D2D_dist_out <= 18.0) {
      Prob_LOS_sig = 1.0;
    } else {
      if (MS_t <= 13.0) {
        C = 0.0;
      } else {
        /* should not exceed 23m */
        C = muDoubleScalarPower((MS_t - 13.0) / 10.0, 1.5);
      }

      Prob_LOS_sig = (18.0 / D2D_dist_out + muDoubleScalarExp(-D2D_dist_out /
        63.0) * (1.0 - 18.0 / D2D_dist_out)) * (C * 5.0 / 4.0 *
        muDoubleScalarPower(D2D_dist_out / 100.0, 3.0) * muDoubleScalarExp
        (-D2D_dist_out / 150.0) + 1.0);
    }
  } else if (D2D_dist_out <= 18.0) {
    Prob_LOS_sig = 1.0;
  } else {
    Prob_LOS_sig = 18.0 / D2D_dist_out + muDoubleScalarExp(-D2D_dist_out / 36.0)
      * (1.0 - 18.0 / D2D_dist_out);
  }

  return Prob_LOS_sig;
}

static void UMA_Model(const emlrtStack *sp, real_T fc, const emxArray_real_T
                      *D3D_dist, const emxArray_real_T *BS_t, const
                      emxArray_real_T *MS_t, real_T d_bp_pl, const
                      emxArray_real_T *pLOS, emxArray_real_T *sig)
{
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  emlrtStack e_st;
  emlrtStack f_st;
  emlrtStack g_st;
  emlrtStack h_st;
  emlrtStack st;
  emxArray_boolean_T *b_D3D_dist;
  emxArray_real_T *PL_UMA_LOS_dBP_sig;
  emxArray_real_T *PL_UMA_NLOS_sig;
  emxArray_real_T *PL_UMA_free_sig;
  emxArray_real_T *PL_tot_sig_LOS;
  emxArray_real_T *SF_UMA_LOS;
  emxArray_real_T *SF_UMa_NLOS;
  real_T dv[2];
  real_T SF_FS;
  real_T x;
  int32_T csz_idx_1;
  int32_T k;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  e_st.prev = &d_st;
  e_st.tls = d_st.tls;
  f_st.prev = &e_st;
  f_st.tls = e_st.tls;
  g_st.prev = &f_st;
  g_st.tls = f_st.tls;
  h_st.prev = &g_st;
  h_st.tls = g_st.tls;
  emlrtHeapReferenceStackEnterFcnR2012b(sp);
  emxInit_real_T(sp, &SF_UMA_LOS, 2, &vb_emlrtRTEI, true);
  st.site = &tb_emlrtRSI;
  b_st.site = &cc_emlrtRSI;
  c_st.site = &dc_emlrtRSI;
  dv[0] = 1.0;
  dv[1] = (uint32_T)D3D_dist->size[1];
  d_st.site = &ec_emlrtRSI;
  b_randn(&d_st, dv, SF_UMA_LOS);
  k = SF_UMA_LOS->size[0] * SF_UMA_LOS->size[1];
  csz_idx_1 = SF_UMA_LOS->size[0] * SF_UMA_LOS->size[1];
  SF_UMA_LOS->size[0] = 1;
  emxEnsureCapacity_real_T(&c_st, SF_UMA_LOS, csz_idx_1, &vb_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    SF_UMA_LOS->data[k] *= 4.0;
  }

  emxInit_real_T(&c_st, &PL_UMA_NLOS_sig, 2, &oc_emlrtRTEI, true);

  /* log10(normrnd(0, 7)); %7dB std deviation, random normal, mean 0 */
  /* SF = 0;     */
  /* Per TR 38.901, Table 7.4.1-1 */
  /* LOS SINR_model (only for 10 meters or more) */
  /* PL1 */
  k = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
  PL_UMA_NLOS_sig->size[0] = 1;
  PL_UMA_NLOS_sig->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMA_NLOS_sig, k, &wb_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMA_NLOS_sig->data[k] = D3D_dist->data[k];
  }

  st.site = &ub_emlrtRSI;
  b_log10(&st, PL_UMA_NLOS_sig);
  k = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
  csz_idx_1 = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
  PL_UMA_NLOS_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMA_NLOS_sig, csz_idx_1, &xb_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMA_NLOS_sig->data[k] *= 22.0;
  }

  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMA_NLOS_sig->size, *(int32_T (*)
    [2])SF_UMA_LOS->size, &t_emlrtECI, sp);
  st.site = &ub_emlrtRSI;
  if (fc < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  emxInit_real_T(&st, &PL_UMA_LOS_dBP_sig, 2, &ec_emlrtRTEI, true);

  /* TR 38.901 */
  /* PL2 */
  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])BS_t->size, *(int32_T (*)[2])
    MS_t->size, &s_emlrtECI, sp);
  k = PL_UMA_LOS_dBP_sig->size[0] * PL_UMA_LOS_dBP_sig->size[1];
  PL_UMA_LOS_dBP_sig->size[0] = 1;
  PL_UMA_LOS_dBP_sig->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMA_LOS_dBP_sig, k, &yb_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMA_LOS_dBP_sig->data[k] = D3D_dist->data[k];
  }

  st.site = &vb_emlrtRSI;
  b_log10(&st, PL_UMA_LOS_dBP_sig);
  k = PL_UMA_LOS_dBP_sig->size[0] * PL_UMA_LOS_dBP_sig->size[1];
  csz_idx_1 = PL_UMA_LOS_dBP_sig->size[0] * PL_UMA_LOS_dBP_sig->size[1];
  PL_UMA_LOS_dBP_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMA_LOS_dBP_sig, csz_idx_1, &ac_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMA_LOS_dBP_sig->data[k] *= 40.0;
  }

  emxInit_real_T(sp, &PL_UMA_free_sig, 2, &gc_emlrtRTEI, true);
  st.site = &vb_emlrtRSI;
  b_st.site = &pb_emlrtRSI;
  x = d_bp_pl * d_bp_pl;
  k = PL_UMA_free_sig->size[0] * PL_UMA_free_sig->size[1];
  PL_UMA_free_sig->size[0] = 1;
  PL_UMA_free_sig->size[1] = BS_t->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMA_free_sig, k, &bc_emlrtRTEI);
  csz_idx_1 = BS_t->size[0] * BS_t->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMA_free_sig->data[k] = BS_t->data[k] - MS_t->data[k];
  }

  emxInit_real_T(sp, &SF_UMa_NLOS, 2, &kc_emlrtRTEI, true);
  st.site = &vb_emlrtRSI;
  power(&st, PL_UMA_free_sig, SF_UMa_NLOS);
  k = SF_UMa_NLOS->size[0] * SF_UMa_NLOS->size[1];
  csz_idx_1 = SF_UMa_NLOS->size[0] * SF_UMa_NLOS->size[1];
  SF_UMa_NLOS->size[0] = 1;
  emxEnsureCapacity_real_T(sp, SF_UMa_NLOS, csz_idx_1, &cc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    SF_UMa_NLOS->data[k] += x;
  }

  st.site = &vb_emlrtRSI;
  b_log10(&st, SF_UMa_NLOS);
  k = SF_UMa_NLOS->size[0] * SF_UMa_NLOS->size[1];
  csz_idx_1 = SF_UMa_NLOS->size[0] * SF_UMa_NLOS->size[1];
  SF_UMa_NLOS->size[0] = 1;
  emxEnsureCapacity_real_T(sp, SF_UMa_NLOS, csz_idx_1, &dc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    SF_UMa_NLOS->data[k] *= 9.0;
  }

  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMA_LOS_dBP_sig->size, *(int32_T
    (*)[2])SF_UMa_NLOS->size, &r_emlrtECI, sp);
  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMA_LOS_dBP_sig->size, *(int32_T
    (*)[2])SF_UMA_LOS->size, &r_emlrtECI, sp);
  st.site = &vb_emlrtRSI;
  k = PL_UMA_LOS_dBP_sig->size[0] * PL_UMA_LOS_dBP_sig->size[1];
  csz_idx_1 = PL_UMA_LOS_dBP_sig->size[0] * PL_UMA_LOS_dBP_sig->size[1];
  PL_UMA_LOS_dBP_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMA_LOS_dBP_sig, csz_idx_1, &ec_emlrtRTEI);
  x = 20.0 * muDoubleScalarLog10(fc);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMA_LOS_dBP_sig->data[k] = (((PL_UMA_LOS_dBP_sig->data[k] + 28.0) + x) -
      SF_UMa_NLOS->data[k]) + SF_UMA_LOS->data[k];
  }

  /* TR 38.901 */
  /* Path Loss, free space */
  st.site = &wb_emlrtRSI;
  b_st.site = &cc_emlrtRSI;
  c_st.site = &dc_emlrtRSI;
  d_st.site = &ec_emlrtRSI;
  SF_FS = randn();
  SF_FS *= 7.8;
  st.site = &xb_emlrtRSI;
  k = PL_UMA_free_sig->size[0] * PL_UMA_free_sig->size[1];
  PL_UMA_free_sig->size[0] = 1;
  PL_UMA_free_sig->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMA_free_sig, k, &fc_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMA_free_sig->data[k] = D3D_dist->data[k];
  }

  st.site = &xb_emlrtRSI;
  b_log10(&st, PL_UMA_free_sig);
  k = PL_UMA_free_sig->size[0] * PL_UMA_free_sig->size[1];
  csz_idx_1 = PL_UMA_free_sig->size[0] * PL_UMA_free_sig->size[1];
  PL_UMA_free_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMA_free_sig, csz_idx_1, &gc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMA_free_sig->data[k] = ((x + 32.4) + 30.0 * PL_UMA_free_sig->data[k]) +
      SF_FS;
  }

  emxInit_boolean_T(sp, &b_D3D_dist, 2, &hc_emlrtRTEI, true);

  /* %%%%%%%%%%%%%%%%%%%%%%% */
  /* Model descion (PathLoss to device) */
  k = b_D3D_dist->size[0] * b_D3D_dist->size[1];
  b_D3D_dist->size[0] = 1;
  b_D3D_dist->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_boolean_T(sp, b_D3D_dist, k, &hc_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    b_D3D_dist->data[k] = (D3D_dist->data[k] <= d_bp_pl);
  }

  st.site = &sc_emlrtRSI;
  if (ifWhileCond(&st, b_D3D_dist)) {
    k = PL_UMA_LOS_dBP_sig->size[0] * PL_UMA_LOS_dBP_sig->size[1];
    PL_UMA_LOS_dBP_sig->size[0] = 1;
    PL_UMA_LOS_dBP_sig->size[1] = PL_UMA_NLOS_sig->size[1];
    emxEnsureCapacity_real_T(sp, PL_UMA_LOS_dBP_sig, k, &ic_emlrtRTEI);
    csz_idx_1 = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
    for (k = 0; k < csz_idx_1; k++) {
      PL_UMA_LOS_dBP_sig->data[k] = ((PL_UMA_NLOS_sig->data[k] + 28.0) + x) +
        SF_UMA_LOS->data[k];
    }

    /*  10m<d<d_BP': LOS1 */
  } else {
    /*  d_BP'<d<5000m: LOS2  */
  }

  /*  should greater than or equal for free space */
  st.site = &tc_emlrtRSI;
  b_st.site = &xc_emlrtRSI;
  c_st.site = &yc_emlrtRSI;
  d_st.site = &ad_emlrtRSI;
  e_st.site = &bd_emlrtRSI;
  f_st.site = &cd_emlrtRSI;
  if (PL_UMA_free_sig->size[1] <= PL_UMA_LOS_dBP_sig->size[1]) {
    csz_idx_1 = PL_UMA_free_sig->size[1];
  } else {
    csz_idx_1 = PL_UMA_LOS_dBP_sig->size[1];
  }

  k = SF_UMa_NLOS->size[0] * SF_UMa_NLOS->size[1];
  SF_UMa_NLOS->size[0] = 1;
  if (PL_UMA_free_sig->size[1] <= PL_UMA_LOS_dBP_sig->size[1]) {
    SF_UMa_NLOS->size[1] = PL_UMA_free_sig->size[1];
  } else {
    SF_UMa_NLOS->size[1] = PL_UMA_LOS_dBP_sig->size[1];
  }

  emxEnsureCapacity_real_T(&f_st, SF_UMa_NLOS, k, &jc_emlrtRTEI);
  if (!dimagree(SF_UMa_NLOS, PL_UMA_free_sig, PL_UMA_LOS_dBP_sig)) {
    emlrtErrorWithMessageIdR2018a(&f_st, &d_emlrtRTEI, "MATLAB:dimagree",
      "MATLAB:dimagree", 0);
  }

  emxInit_real_T(&f_st, &PL_tot_sig_LOS, 2, &rc_emlrtRTEI, true);
  k = PL_tot_sig_LOS->size[0] * PL_tot_sig_LOS->size[1];
  PL_tot_sig_LOS->size[0] = 1;
  PL_tot_sig_LOS->size[1] = csz_idx_1;
  emxEnsureCapacity_real_T(&e_st, PL_tot_sig_LOS, k, &pb_emlrtRTEI);
  f_st.site = &qc_emlrtRSI;
  g_st.site = &dd_emlrtRSI;
  if ((1 <= SF_UMa_NLOS->size[1]) && (SF_UMa_NLOS->size[1] > 2147483646)) {
    h_st.site = &hc_emlrtRSI;
    check_forloop_overflow_error(&h_st);
  }

  for (k = 0; k < csz_idx_1; k++) {
    PL_tot_sig_LOS->data[k] = muDoubleScalarMax(PL_UMA_free_sig->data[k],
      PL_UMA_LOS_dBP_sig->data[k]);
  }

  emxFree_real_T(&PL_UMA_free_sig);
  emxFree_real_T(&PL_UMA_LOS_dBP_sig);

  /* NLOS */
  st.site = &yb_emlrtRSI;
  b_st.site = &cc_emlrtRSI;
  c_st.site = &dc_emlrtRSI;
  dv[0] = 1.0;
  dv[1] = (uint32_T)D3D_dist->size[1];
  d_st.site = &ec_emlrtRSI;
  b_randn(&d_st, dv, SF_UMa_NLOS);
  k = SF_UMa_NLOS->size[0] * SF_UMa_NLOS->size[1];
  csz_idx_1 = SF_UMa_NLOS->size[0] * SF_UMa_NLOS->size[1];
  SF_UMa_NLOS->size[0] = 1;
  emxEnsureCapacity_real_T(&c_st, SF_UMa_NLOS, csz_idx_1, &kc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    SF_UMa_NLOS->data[k] *= 6.0;
  }

  k = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
  PL_UMA_NLOS_sig->size[0] = 1;
  PL_UMA_NLOS_sig->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMA_NLOS_sig, k, &lc_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMA_NLOS_sig->data[k] = D3D_dist->data[k];
  }

  st.site = &ac_emlrtRSI;
  b_log10(&st, PL_UMA_NLOS_sig);
  k = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
  csz_idx_1 = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
  PL_UMA_NLOS_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMA_NLOS_sig, csz_idx_1, &mc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMA_NLOS_sig->data[k] *= 39.08;
  }

  k = SF_UMA_LOS->size[0] * SF_UMA_LOS->size[1];
  SF_UMA_LOS->size[0] = 1;
  SF_UMA_LOS->size[1] = MS_t->size[1];
  emxEnsureCapacity_real_T(sp, SF_UMA_LOS, k, &nc_emlrtRTEI);
  csz_idx_1 = MS_t->size[0] * MS_t->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    SF_UMA_LOS->data[k] = 0.6 * (MS_t->data[k] - 1.5);
  }

  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMA_NLOS_sig->size, *(int32_T (*)
    [2])SF_UMA_LOS->size, &q_emlrtECI, sp);
  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMA_NLOS_sig->size, *(int32_T (*)
    [2])SF_UMa_NLOS->size, &q_emlrtECI, sp);
  st.site = &ac_emlrtRSI;
  k = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
  csz_idx_1 = PL_UMA_NLOS_sig->size[0] * PL_UMA_NLOS_sig->size[1];
  PL_UMA_NLOS_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMA_NLOS_sig, csz_idx_1, &oc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMA_NLOS_sig->data[k] = (((PL_UMA_NLOS_sig->data[k] + 13.54) + x) -
      SF_UMA_LOS->data[k]) + SF_UMa_NLOS->data[k];
  }

  emxFree_real_T(&SF_UMA_LOS);
  st.site = &uc_emlrtRSI;
  b_st.site = &xc_emlrtRSI;
  c_st.site = &yc_emlrtRSI;
  d_st.site = &ad_emlrtRSI;
  e_st.site = &bd_emlrtRSI;
  f_st.site = &cd_emlrtRSI;
  if (PL_tot_sig_LOS->size[1] <= PL_UMA_NLOS_sig->size[1]) {
    csz_idx_1 = PL_tot_sig_LOS->size[1];
  } else {
    csz_idx_1 = PL_UMA_NLOS_sig->size[1];
  }

  k = SF_UMa_NLOS->size[0] * SF_UMa_NLOS->size[1];
  SF_UMa_NLOS->size[0] = 1;
  if (PL_tot_sig_LOS->size[1] <= PL_UMA_NLOS_sig->size[1]) {
    SF_UMa_NLOS->size[1] = PL_tot_sig_LOS->size[1];
  } else {
    SF_UMa_NLOS->size[1] = PL_UMA_NLOS_sig->size[1];
  }

  emxEnsureCapacity_real_T(&f_st, SF_UMa_NLOS, k, &jc_emlrtRTEI);
  if (!dimagree(SF_UMa_NLOS, PL_tot_sig_LOS, PL_UMA_NLOS_sig)) {
    emlrtErrorWithMessageIdR2018a(&f_st, &d_emlrtRTEI, "MATLAB:dimagree",
      "MATLAB:dimagree", 0);
  }

  k = sig->size[0] * sig->size[1];
  sig->size[0] = 1;
  sig->size[1] = csz_idx_1;
  emxEnsureCapacity_real_T(&e_st, sig, k, &pb_emlrtRTEI);
  f_st.site = &qc_emlrtRSI;
  g_st.site = &dd_emlrtRSI;
  if ((1 <= SF_UMa_NLOS->size[1]) && (SF_UMa_NLOS->size[1] > 2147483646)) {
    h_st.site = &hc_emlrtRSI;
    check_forloop_overflow_error(&h_st);
  }

  emxFree_real_T(&SF_UMa_NLOS);
  for (k = 0; k < csz_idx_1; k++) {
    sig->data[k] = muDoubleScalarMax(PL_tot_sig_LOS->data[k],
      PL_UMA_NLOS_sig->data[k]);
  }

  emxFree_real_T(&PL_UMA_NLOS_sig);
  st.site = &bc_emlrtRSI;
  x = b_rand();
  k = b_D3D_dist->size[0] * b_D3D_dist->size[1];
  b_D3D_dist->size[0] = 1;
  b_D3D_dist->size[1] = pLOS->size[1];
  emxEnsureCapacity_boolean_T(sp, b_D3D_dist, k, &pc_emlrtRTEI);
  csz_idx_1 = pLOS->size[0] * pLOS->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    b_D3D_dist->data[k] = (x <= pLOS->data[k]);
  }

  st.site = &vc_emlrtRSI;
  if (ifWhileCond(&st, b_D3D_dist)) {
    k = sig->size[0] * sig->size[1];
    sig->size[0] = 1;
    sig->size[1] = PL_tot_sig_LOS->size[1];
    emxEnsureCapacity_real_T(sp, sig, k, &qc_emlrtRTEI);
    csz_idx_1 = PL_tot_sig_LOS->size[0] * PL_tot_sig_LOS->size[1];
    for (k = 0; k < csz_idx_1; k++) {
      sig->data[k] = PL_tot_sig_LOS->data[k];
    }
  }

  emxFree_boolean_T(&b_D3D_dist);
  emxFree_real_T(&PL_tot_sig_LOS);
  emlrtHeapReferenceStackLeaveFcnR2012b(sp);
}

static real_T UMI_Model(const emlrtStack *sp, real_T fc, real_T D3D_dist, real_T
  BS_t, real_T MS_t, real_T d_bp_pl, real_T pLOS)
{
  emlrtStack st;
  real_T SF_FS;
  real_T SF_UMi_LOS;
  real_T sig;
  real_T x;
  st.prev = sp;
  st.tls = sp->tls;
  SF_UMi_LOS = randn();
  SF_UMi_LOS *= 4.0;

  /* log10(normrnd(0, 7)); %7dB std deviation, random normal, mean 0 */
  /* SF = 0;     */
  /* Per TR 38.901, Table 7.4.1-1 */
  /* LOS SINR_model (only for 10 meters or more) */
  /* PL1 */
  st.site = &fd_emlrtRSI;
  if (D3D_dist < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  st.site = &fd_emlrtRSI;
  if (fc < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  /* TR 38.901 */
  /* PL2 */
  sig = BS_t - MS_t;
  st.site = &gd_emlrtRSI;
  x = d_bp_pl * d_bp_pl + sig * sig;
  if (x < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  x = muDoubleScalarLog10(x);

  /* TR 38.901 */
  /* Path Loss, free space */
  SF_FS = randn();
  SF_FS *= 8.2;

  /* %%%%%%%%%%%%%%%%%%%%%%% */
  /* Model descion (PathLoss to device) */
  if (D3D_dist <= d_bp_pl) {
    sig = ((21.0 * muDoubleScalarLog10(D3D_dist) + 32.4) + 20.0 *
           muDoubleScalarLog10(fc)) + SF_UMi_LOS;

    /*  10m<d<d_BP': LOS1 */
  } else {
    sig = (((40.0 * muDoubleScalarLog10(D3D_dist) + 32.4) + 20.0 *
            muDoubleScalarLog10(fc)) - 9.5 * x) + SF_UMi_LOS;

    /*  d_BP'<d<5000m: LOS2  */
  }

  /*  should greater than or equal for free space */
  sig = muDoubleScalarMax(((20.0 * muDoubleScalarLog10(fc) + 32.4) + 31.9 *
    muDoubleScalarLog10(D3D_dist)) + SF_FS, sig);

  /* NLOS */
  SF_UMi_LOS = randn();
  SF_UMi_LOS *= 7.82;
  x = b_rand();
  if (!(x <= pLOS)) {
    sig = muDoubleScalarMax(sig, (((35.3 * muDoubleScalarLog10(D3D_dist) + 22.4)
      + 21.3 * muDoubleScalarLog10(fc)) - 0.3 * (MS_t - 1.5)) + SF_UMi_LOS);
  }

  return sig;
}

static void b_PrLOS(const emlrtStack *sp, const emxArray_real_T *D2D_dist_out,
                    real_T MS_t, boolean_T UMA_notUMi, emxArray_real_T
                    *Prob_LOS_sig)
{
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  emlrtStack e_st;
  emlrtStack f_st;
  emlrtStack st;
  emxArray_boolean_T *b_D2D_dist_out;
  emxArray_real_T *a;
  emxArray_real_T *r;
  emxArray_real_T *z1;
  real_T C;
  int32_T k;
  int32_T nx;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  e_st.prev = &d_st;
  e_st.tls = d_st.tls;
  f_st.prev = &e_st;
  f_st.tls = e_st.tls;
  emlrtHeapReferenceStackEnterFcnR2012b(sp);
  emxInit_real_T(sp, &r, 2, &ub_emlrtRTEI, true);
  emxInit_boolean_T(sp, &b_D2D_dist_out, 2, &eb_emlrtRTEI, true);
  if (UMA_notUMi) {
    k = b_D2D_dist_out->size[0] * b_D2D_dist_out->size[1];
    b_D2D_dist_out->size[0] = 1;
    b_D2D_dist_out->size[1] = D2D_dist_out->size[1];
    emxEnsureCapacity_boolean_T(sp, b_D2D_dist_out, k, &fb_emlrtRTEI);
    nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
    for (k = 0; k < nx; k++) {
      b_D2D_dist_out->data[k] = (D2D_dist_out->data[k] <= 18.0);
    }

    st.site = &ic_emlrtRSI;
    if (ifWhileCond(&st, b_D2D_dist_out)) {
      k = Prob_LOS_sig->size[0] * Prob_LOS_sig->size[1];
      Prob_LOS_sig->size[0] = 1;
      Prob_LOS_sig->size[1] = 1;
      emxEnsureCapacity_real_T(sp, Prob_LOS_sig, k, &ib_emlrtRTEI);
      Prob_LOS_sig->data[0] = 1.0;
    } else {
      if (MS_t <= 13.0) {
        C = 0.0;
      } else {
        /* should not exceed 23m */
        st.site = &rb_emlrtRSI;
        b_st.site = &pb_emlrtRSI;
        C = muDoubleScalarPower((MS_t - 13.0) / 10.0, 1.5);
      }

      k = r->size[0] * r->size[1];
      r->size[0] = 1;
      r->size[1] = D2D_dist_out->size[1];
      emxEnsureCapacity_real_T(sp, r, k, &jb_emlrtRTEI);
      nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
      for (k = 0; k < nx; k++) {
        r->data[k] = -D2D_dist_out->data[k] / 63.0;
      }

      emxInit_real_T(sp, &a, 2, &ob_emlrtRTEI, true);
      st.site = &jc_emlrtRSI;
      b_exp(&st, r);
      k = a->size[0] * a->size[1];
      a->size[0] = 1;
      a->size[1] = D2D_dist_out->size[1];
      emxEnsureCapacity_real_T(sp, a, k, &lb_emlrtRTEI);
      nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
      for (k = 0; k < nx; k++) {
        a->data[k] = 18.0 / D2D_dist_out->data[k];
      }

      emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])r->size, *(int32_T (*)[2])
        a->size, &p_emlrtECI, sp);
      k = Prob_LOS_sig->size[0] * Prob_LOS_sig->size[1];
      Prob_LOS_sig->size[0] = 1;
      Prob_LOS_sig->size[1] = D2D_dist_out->size[1];
      emxEnsureCapacity_real_T(sp, Prob_LOS_sig, k, &mb_emlrtRTEI);
      nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
      for (k = 0; k < nx; k++) {
        Prob_LOS_sig->data[k] = 18.0 / D2D_dist_out->data[k];
      }

      k = r->size[0] * r->size[1];
      nx = r->size[0] * r->size[1];
      r->size[0] = 1;
      emxEnsureCapacity_real_T(sp, r, nx, &jb_emlrtRTEI);
      nx = k - 1;
      for (k = 0; k <= nx; k++) {
        r->data[k] *= 1.0 - a->data[k];
      }

      emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Prob_LOS_sig->size, *(int32_T (*)
        [2])r->size, &o_emlrtECI, sp);
      C = C * 5.0 / 4.0;
      st.site = &sb_emlrtRSI;
      k = a->size[0] * a->size[1];
      a->size[0] = 1;
      a->size[1] = D2D_dist_out->size[1];
      emxEnsureCapacity_real_T(&st, a, k, &ob_emlrtRTEI);
      nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
      for (k = 0; k < nx; k++) {
        a->data[k] = D2D_dist_out->data[k] / 100.0;
      }

      emxInit_real_T(&st, &z1, 2, &ub_emlrtRTEI, true);
      b_st.site = &pb_emlrtRSI;
      c_st.site = &pc_emlrtRSI;
      k = z1->size[0] * z1->size[1];
      z1->size[0] = 1;
      z1->size[1] = a->size[1];
      emxEnsureCapacity_real_T(&c_st, z1, k, &pb_emlrtRTEI);
      d_st.site = &qc_emlrtRSI;
      nx = a->size[1];
      e_st.site = &rc_emlrtRSI;
      if ((1 <= a->size[1]) && (a->size[1] > 2147483646)) {
        f_st.site = &hc_emlrtRSI;
        check_forloop_overflow_error(&f_st);
      }

      for (k = 0; k < nx; k++) {
        z1->data[k] = muDoubleScalarPower(a->data[k], 3.0);
      }

      k = z1->size[0] * z1->size[1];
      nx = z1->size[0] * z1->size[1];
      z1->size[0] = 1;
      emxEnsureCapacity_real_T(sp, z1, nx, &qb_emlrtRTEI);
      nx = k - 1;
      for (k = 0; k <= nx; k++) {
        z1->data[k] *= C;
      }

      k = a->size[0] * a->size[1];
      a->size[0] = 1;
      a->size[1] = D2D_dist_out->size[1];
      emxEnsureCapacity_real_T(sp, a, k, &rb_emlrtRTEI);
      nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
      for (k = 0; k < nx; k++) {
        a->data[k] = -D2D_dist_out->data[k] / 150.0;
      }

      st.site = &sb_emlrtRSI;
      b_exp(&st, a);
      emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])z1->size, *(int32_T (*)[2])
        a->size, &n_emlrtECI, sp);
      k = z1->size[0] * z1->size[1];
      nx = z1->size[0] * z1->size[1];
      z1->size[0] = 1;
      emxEnsureCapacity_real_T(sp, z1, nx, &sb_emlrtRTEI);
      nx = k - 1;
      for (k = 0; k <= nx; k++) {
        z1->data[k] *= a->data[k];
      }

      emxFree_real_T(&a);
      emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Prob_LOS_sig->size, *(int32_T (*)
        [2])z1->size, &m_emlrtECI, sp);
      k = Prob_LOS_sig->size[0] * Prob_LOS_sig->size[1];
      nx = Prob_LOS_sig->size[0] * Prob_LOS_sig->size[1];
      Prob_LOS_sig->size[0] = 1;
      emxEnsureCapacity_real_T(sp, Prob_LOS_sig, nx, &tb_emlrtRTEI);
      nx = k - 1;
      for (k = 0; k <= nx; k++) {
        Prob_LOS_sig->data[k] = (Prob_LOS_sig->data[k] + r->data[k]) * (z1->
          data[k] + 1.0);
      }

      emxFree_real_T(&z1);
    }
  } else {
    k = b_D2D_dist_out->size[0] * b_D2D_dist_out->size[1];
    b_D2D_dist_out->size[0] = 1;
    b_D2D_dist_out->size[1] = D2D_dist_out->size[1];
    emxEnsureCapacity_boolean_T(sp, b_D2D_dist_out, k, &eb_emlrtRTEI);
    nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
    for (k = 0; k < nx; k++) {
      b_D2D_dist_out->data[k] = (D2D_dist_out->data[k] <= 18.0);
    }

    st.site = &kc_emlrtRSI;
    if (ifWhileCond(&st, b_D2D_dist_out)) {
      k = Prob_LOS_sig->size[0] * Prob_LOS_sig->size[1];
      Prob_LOS_sig->size[0] = 1;
      Prob_LOS_sig->size[1] = 1;
      emxEnsureCapacity_real_T(sp, Prob_LOS_sig, k, &hb_emlrtRTEI);
      Prob_LOS_sig->data[0] = 1.0;
    } else {
      k = r->size[0] * r->size[1];
      r->size[0] = 1;
      r->size[1] = D2D_dist_out->size[1];
      emxEnsureCapacity_real_T(sp, r, k, &gb_emlrtRTEI);
      nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
      for (k = 0; k < nx; k++) {
        r->data[k] = -D2D_dist_out->data[k] / 36.0;
      }

      st.site = &lc_emlrtRSI;
      b_exp(&st, r);
      k = Prob_LOS_sig->size[0] * Prob_LOS_sig->size[1];
      Prob_LOS_sig->size[0] = 1;
      Prob_LOS_sig->size[1] = D2D_dist_out->size[1];
      emxEnsureCapacity_real_T(sp, Prob_LOS_sig, k, &kb_emlrtRTEI);
      nx = D2D_dist_out->size[0] * D2D_dist_out->size[1];
      for (k = 0; k < nx; k++) {
        Prob_LOS_sig->data[k] = 18.0 / D2D_dist_out->data[k];
      }

      emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])r->size, *(int32_T (*)[2])
        Prob_LOS_sig->size, &l_emlrtECI, sp);
      k = r->size[0] * r->size[1];
      nx = r->size[0] * r->size[1];
      r->size[0] = 1;
      emxEnsureCapacity_real_T(sp, r, nx, &gb_emlrtRTEI);
      nx = k - 1;
      for (k = 0; k <= nx; k++) {
        r->data[k] *= 1.0 - Prob_LOS_sig->data[k];
      }

      emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Prob_LOS_sig->size, *(int32_T (*)
        [2])r->size, &k_emlrtECI, sp);
      k = Prob_LOS_sig->size[0] * Prob_LOS_sig->size[1];
      nx = Prob_LOS_sig->size[0] * Prob_LOS_sig->size[1];
      Prob_LOS_sig->size[0] = 1;
      emxEnsureCapacity_real_T(sp, Prob_LOS_sig, nx, &nb_emlrtRTEI);
      nx = k - 1;
      for (k = 0; k <= nx; k++) {
        Prob_LOS_sig->data[k] += r->data[k];
      }
    }
  }

  emxFree_boolean_T(&b_D2D_dist_out);
  emxFree_real_T(&r);
  emlrtHeapReferenceStackLeaveFcnR2012b(sp);
}

static void b_UMI_Model(const emlrtStack *sp, real_T fc, const emxArray_real_T
  *D3D_dist, const emxArray_real_T *BS_t, const emxArray_real_T *MS_t, real_T
  d_bp_pl, const emxArray_real_T *pLOS, emxArray_real_T *sig)
{
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  emlrtStack e_st;
  emlrtStack f_st;
  emlrtStack g_st;
  emlrtStack h_st;
  emlrtStack st;
  emxArray_boolean_T *b_D3D_dist;
  emxArray_real_T *PL_UMI_LOS_dBP_sig;
  emxArray_real_T *PL_UMI_NLOS_sig;
  emxArray_real_T *PL_UMI_free_sig;
  emxArray_real_T *PL_tot_sig_LOS;
  emxArray_real_T *SF_UMI_NLOS;
  emxArray_real_T *SF_UMi_LOS;
  real_T dv[2];
  real_T SF_FS;
  real_T d;
  real_T x;
  int32_T csz_idx_1;
  int32_T k;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  e_st.prev = &d_st;
  e_st.tls = d_st.tls;
  f_st.prev = &e_st;
  f_st.tls = e_st.tls;
  g_st.prev = &f_st;
  g_st.tls = f_st.tls;
  h_st.prev = &g_st;
  h_st.tls = g_st.tls;
  emlrtHeapReferenceStackEnterFcnR2012b(sp);
  emxInit_real_T(sp, &SF_UMi_LOS, 2, &tc_emlrtRTEI, true);
  st.site = &ed_emlrtRSI;
  b_st.site = &cc_emlrtRSI;
  c_st.site = &dc_emlrtRSI;
  dv[0] = 1.0;
  dv[1] = (uint32_T)D3D_dist->size[1];
  d_st.site = &ec_emlrtRSI;
  b_randn(&d_st, dv, SF_UMi_LOS);
  k = SF_UMi_LOS->size[0] * SF_UMi_LOS->size[1];
  csz_idx_1 = SF_UMi_LOS->size[0] * SF_UMi_LOS->size[1];
  SF_UMi_LOS->size[0] = 1;
  emxEnsureCapacity_real_T(&c_st, SF_UMi_LOS, csz_idx_1, &tc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    SF_UMi_LOS->data[k] *= 4.0;
  }

  emxInit_real_T(&c_st, &PL_UMI_NLOS_sig, 2, &ld_emlrtRTEI, true);

  /* log10(normrnd(0, 7)); %7dB std deviation, random normal, mean 0 */
  /* SF = 0;     */
  /* Per TR 38.901, Table 7.4.1-1 */
  /* LOS SINR_model (only for 10 meters or more) */
  /* PL1 */
  k = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
  PL_UMI_NLOS_sig->size[0] = 1;
  PL_UMI_NLOS_sig->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMI_NLOS_sig, k, &uc_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMI_NLOS_sig->data[k] = D3D_dist->data[k];
  }

  st.site = &fd_emlrtRSI;
  b_log10(&st, PL_UMI_NLOS_sig);
  k = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
  csz_idx_1 = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
  PL_UMI_NLOS_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMI_NLOS_sig, csz_idx_1, &vc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMI_NLOS_sig->data[k] *= 21.0;
  }

  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMI_NLOS_sig->size, *(int32_T (*)
    [2])SF_UMi_LOS->size, &x_emlrtECI, sp);
  st.site = &fd_emlrtRSI;
  if (fc < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  emxInit_real_T(&st, &PL_UMI_LOS_dBP_sig, 2, &cd_emlrtRTEI, true);

  /* TR 38.901 */
  /* PL2 */
  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])BS_t->size, *(int32_T (*)[2])
    MS_t->size, &w_emlrtECI, sp);
  k = PL_UMI_LOS_dBP_sig->size[0] * PL_UMI_LOS_dBP_sig->size[1];
  PL_UMI_LOS_dBP_sig->size[0] = 1;
  PL_UMI_LOS_dBP_sig->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMI_LOS_dBP_sig, k, &wc_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMI_LOS_dBP_sig->data[k] = D3D_dist->data[k];
  }

  st.site = &gd_emlrtRSI;
  b_log10(&st, PL_UMI_LOS_dBP_sig);
  k = PL_UMI_LOS_dBP_sig->size[0] * PL_UMI_LOS_dBP_sig->size[1];
  csz_idx_1 = PL_UMI_LOS_dBP_sig->size[0] * PL_UMI_LOS_dBP_sig->size[1];
  PL_UMI_LOS_dBP_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMI_LOS_dBP_sig, csz_idx_1, &xc_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMI_LOS_dBP_sig->data[k] *= 40.0;
  }

  emxInit_real_T(sp, &PL_UMI_free_sig, 2, &ed_emlrtRTEI, true);
  st.site = &gd_emlrtRSI;
  b_st.site = &pb_emlrtRSI;
  x = d_bp_pl * d_bp_pl;
  k = PL_UMI_free_sig->size[0] * PL_UMI_free_sig->size[1];
  PL_UMI_free_sig->size[0] = 1;
  PL_UMI_free_sig->size[1] = BS_t->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMI_free_sig, k, &yc_emlrtRTEI);
  csz_idx_1 = BS_t->size[0] * BS_t->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMI_free_sig->data[k] = BS_t->data[k] - MS_t->data[k];
  }

  emxInit_real_T(sp, &SF_UMI_NLOS, 2, &hd_emlrtRTEI, true);
  st.site = &gd_emlrtRSI;
  power(&st, PL_UMI_free_sig, SF_UMI_NLOS);
  k = SF_UMI_NLOS->size[0] * SF_UMI_NLOS->size[1];
  csz_idx_1 = SF_UMI_NLOS->size[0] * SF_UMI_NLOS->size[1];
  SF_UMI_NLOS->size[0] = 1;
  emxEnsureCapacity_real_T(sp, SF_UMI_NLOS, csz_idx_1, &ad_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    SF_UMI_NLOS->data[k] += x;
  }

  st.site = &gd_emlrtRSI;
  b_log10(&st, SF_UMI_NLOS);
  k = SF_UMI_NLOS->size[0] * SF_UMI_NLOS->size[1];
  csz_idx_1 = SF_UMI_NLOS->size[0] * SF_UMI_NLOS->size[1];
  SF_UMI_NLOS->size[0] = 1;
  emxEnsureCapacity_real_T(sp, SF_UMI_NLOS, csz_idx_1, &bd_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    SF_UMI_NLOS->data[k] *= 9.5;
  }

  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMI_LOS_dBP_sig->size, *(int32_T
    (*)[2])SF_UMI_NLOS->size, &v_emlrtECI, sp);
  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMI_LOS_dBP_sig->size, *(int32_T
    (*)[2])SF_UMi_LOS->size, &v_emlrtECI, sp);
  st.site = &gd_emlrtRSI;
  k = PL_UMI_LOS_dBP_sig->size[0] * PL_UMI_LOS_dBP_sig->size[1];
  csz_idx_1 = PL_UMI_LOS_dBP_sig->size[0] * PL_UMI_LOS_dBP_sig->size[1];
  PL_UMI_LOS_dBP_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMI_LOS_dBP_sig, csz_idx_1, &cd_emlrtRTEI);
  x = muDoubleScalarLog10(fc);
  d = 20.0 * x;
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMI_LOS_dBP_sig->data[k] = (((PL_UMI_LOS_dBP_sig->data[k] + 32.4) + d) -
      SF_UMI_NLOS->data[k]) + SF_UMi_LOS->data[k];
  }

  /* TR 38.901 */
  /* Path Loss, free space */
  st.site = &hd_emlrtRSI;
  b_st.site = &cc_emlrtRSI;
  c_st.site = &dc_emlrtRSI;
  d_st.site = &ec_emlrtRSI;
  SF_FS = randn();
  SF_FS *= 8.2;
  k = PL_UMI_free_sig->size[0] * PL_UMI_free_sig->size[1];
  PL_UMI_free_sig->size[0] = 1;
  PL_UMI_free_sig->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMI_free_sig, k, &dd_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMI_free_sig->data[k] = D3D_dist->data[k];
  }

  st.site = &id_emlrtRSI;
  b_log10(&st, PL_UMI_free_sig);
  st.site = &id_emlrtRSI;
  k = PL_UMI_free_sig->size[0] * PL_UMI_free_sig->size[1];
  csz_idx_1 = PL_UMI_free_sig->size[0] * PL_UMI_free_sig->size[1];
  PL_UMI_free_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMI_free_sig, csz_idx_1, &ed_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMI_free_sig->data[k] = ((d + 32.4) + 31.9 * PL_UMI_free_sig->data[k]) +
      SF_FS;
  }

  emxInit_boolean_T(sp, &b_D3D_dist, 2, &fd_emlrtRTEI, true);

  /* %%%%%%%%%%%%%%%%%%%%%%% */
  /* Model descion (PathLoss to device) */
  k = b_D3D_dist->size[0] * b_D3D_dist->size[1];
  b_D3D_dist->size[0] = 1;
  b_D3D_dist->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_boolean_T(sp, b_D3D_dist, k, &fd_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    b_D3D_dist->data[k] = (D3D_dist->data[k] <= d_bp_pl);
  }

  st.site = &md_emlrtRSI;
  if (ifWhileCond(&st, b_D3D_dist)) {
    k = PL_UMI_LOS_dBP_sig->size[0] * PL_UMI_LOS_dBP_sig->size[1];
    PL_UMI_LOS_dBP_sig->size[0] = 1;
    PL_UMI_LOS_dBP_sig->size[1] = PL_UMI_NLOS_sig->size[1];
    emxEnsureCapacity_real_T(sp, PL_UMI_LOS_dBP_sig, k, &gd_emlrtRTEI);
    csz_idx_1 = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
    for (k = 0; k < csz_idx_1; k++) {
      PL_UMI_LOS_dBP_sig->data[k] = ((PL_UMI_NLOS_sig->data[k] + 32.4) + d) +
        SF_UMi_LOS->data[k];
    }

    /*  10m<d<d_BP': LOS1 */
  } else {
    /*  d_BP'<d<5000m: LOS2  */
  }

  /*  should greater than or equal for free space */
  st.site = &nd_emlrtRSI;
  b_st.site = &xc_emlrtRSI;
  c_st.site = &yc_emlrtRSI;
  d_st.site = &ad_emlrtRSI;
  e_st.site = &bd_emlrtRSI;
  f_st.site = &cd_emlrtRSI;
  if (PL_UMI_free_sig->size[1] <= PL_UMI_LOS_dBP_sig->size[1]) {
    csz_idx_1 = PL_UMI_free_sig->size[1];
  } else {
    csz_idx_1 = PL_UMI_LOS_dBP_sig->size[1];
  }

  k = SF_UMI_NLOS->size[0] * SF_UMI_NLOS->size[1];
  SF_UMI_NLOS->size[0] = 1;
  if (PL_UMI_free_sig->size[1] <= PL_UMI_LOS_dBP_sig->size[1]) {
    SF_UMI_NLOS->size[1] = PL_UMI_free_sig->size[1];
  } else {
    SF_UMI_NLOS->size[1] = PL_UMI_LOS_dBP_sig->size[1];
  }

  emxEnsureCapacity_real_T(&f_st, SF_UMI_NLOS, k, &jc_emlrtRTEI);
  if (!dimagree(SF_UMI_NLOS, PL_UMI_free_sig, PL_UMI_LOS_dBP_sig)) {
    emlrtErrorWithMessageIdR2018a(&f_st, &d_emlrtRTEI, "MATLAB:dimagree",
      "MATLAB:dimagree", 0);
  }

  emxInit_real_T(&f_st, &PL_tot_sig_LOS, 2, &od_emlrtRTEI, true);
  k = PL_tot_sig_LOS->size[0] * PL_tot_sig_LOS->size[1];
  PL_tot_sig_LOS->size[0] = 1;
  PL_tot_sig_LOS->size[1] = csz_idx_1;
  emxEnsureCapacity_real_T(&e_st, PL_tot_sig_LOS, k, &pb_emlrtRTEI);
  f_st.site = &qc_emlrtRSI;
  g_st.site = &dd_emlrtRSI;
  if ((1 <= SF_UMI_NLOS->size[1]) && (SF_UMI_NLOS->size[1] > 2147483646)) {
    h_st.site = &hc_emlrtRSI;
    check_forloop_overflow_error(&h_st);
  }

  for (k = 0; k < csz_idx_1; k++) {
    PL_tot_sig_LOS->data[k] = muDoubleScalarMax(PL_UMI_free_sig->data[k],
      PL_UMI_LOS_dBP_sig->data[k]);
  }

  emxFree_real_T(&PL_UMI_free_sig);
  emxFree_real_T(&PL_UMI_LOS_dBP_sig);

  /* NLOS */
  st.site = &jd_emlrtRSI;
  b_st.site = &cc_emlrtRSI;
  c_st.site = &dc_emlrtRSI;
  dv[0] = 1.0;
  dv[1] = (uint32_T)D3D_dist->size[1];
  d_st.site = &ec_emlrtRSI;
  b_randn(&d_st, dv, SF_UMI_NLOS);
  k = SF_UMI_NLOS->size[0] * SF_UMI_NLOS->size[1];
  csz_idx_1 = SF_UMI_NLOS->size[0] * SF_UMI_NLOS->size[1];
  SF_UMI_NLOS->size[0] = 1;
  emxEnsureCapacity_real_T(&c_st, SF_UMI_NLOS, csz_idx_1, &hd_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    SF_UMI_NLOS->data[k] *= 7.82;
  }

  k = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
  PL_UMI_NLOS_sig->size[0] = 1;
  PL_UMI_NLOS_sig->size[1] = D3D_dist->size[1];
  emxEnsureCapacity_real_T(sp, PL_UMI_NLOS_sig, k, &id_emlrtRTEI);
  csz_idx_1 = D3D_dist->size[0] * D3D_dist->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    PL_UMI_NLOS_sig->data[k] = D3D_dist->data[k];
  }

  st.site = &kd_emlrtRSI;
  b_log10(&st, PL_UMI_NLOS_sig);
  k = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
  csz_idx_1 = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
  PL_UMI_NLOS_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMI_NLOS_sig, csz_idx_1, &jd_emlrtRTEI);
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMI_NLOS_sig->data[k] *= 35.3;
  }

  k = SF_UMi_LOS->size[0] * SF_UMi_LOS->size[1];
  SF_UMi_LOS->size[0] = 1;
  SF_UMi_LOS->size[1] = MS_t->size[1];
  emxEnsureCapacity_real_T(sp, SF_UMi_LOS, k, &kd_emlrtRTEI);
  csz_idx_1 = MS_t->size[0] * MS_t->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    SF_UMi_LOS->data[k] = 0.3 * (MS_t->data[k] - 1.5);
  }

  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMI_NLOS_sig->size, *(int32_T (*)
    [2])SF_UMi_LOS->size, &u_emlrtECI, sp);
  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])PL_UMI_NLOS_sig->size, *(int32_T (*)
    [2])SF_UMI_NLOS->size, &u_emlrtECI, sp);
  st.site = &kd_emlrtRSI;
  k = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
  csz_idx_1 = PL_UMI_NLOS_sig->size[0] * PL_UMI_NLOS_sig->size[1];
  PL_UMI_NLOS_sig->size[0] = 1;
  emxEnsureCapacity_real_T(sp, PL_UMI_NLOS_sig, csz_idx_1, &ld_emlrtRTEI);
  x *= 21.3;
  csz_idx_1 = k - 1;
  for (k = 0; k <= csz_idx_1; k++) {
    PL_UMI_NLOS_sig->data[k] = (((PL_UMI_NLOS_sig->data[k] + 22.4) + x) -
      SF_UMi_LOS->data[k]) + SF_UMI_NLOS->data[k];
  }

  emxFree_real_T(&SF_UMi_LOS);
  st.site = &od_emlrtRSI;
  b_st.site = &xc_emlrtRSI;
  c_st.site = &yc_emlrtRSI;
  d_st.site = &ad_emlrtRSI;
  e_st.site = &bd_emlrtRSI;
  f_st.site = &cd_emlrtRSI;
  if (PL_tot_sig_LOS->size[1] <= PL_UMI_NLOS_sig->size[1]) {
    csz_idx_1 = PL_tot_sig_LOS->size[1];
  } else {
    csz_idx_1 = PL_UMI_NLOS_sig->size[1];
  }

  k = SF_UMI_NLOS->size[0] * SF_UMI_NLOS->size[1];
  SF_UMI_NLOS->size[0] = 1;
  if (PL_tot_sig_LOS->size[1] <= PL_UMI_NLOS_sig->size[1]) {
    SF_UMI_NLOS->size[1] = PL_tot_sig_LOS->size[1];
  } else {
    SF_UMI_NLOS->size[1] = PL_UMI_NLOS_sig->size[1];
  }

  emxEnsureCapacity_real_T(&f_st, SF_UMI_NLOS, k, &jc_emlrtRTEI);
  if (!dimagree(SF_UMI_NLOS, PL_tot_sig_LOS, PL_UMI_NLOS_sig)) {
    emlrtErrorWithMessageIdR2018a(&f_st, &d_emlrtRTEI, "MATLAB:dimagree",
      "MATLAB:dimagree", 0);
  }

  k = sig->size[0] * sig->size[1];
  sig->size[0] = 1;
  sig->size[1] = csz_idx_1;
  emxEnsureCapacity_real_T(&e_st, sig, k, &pb_emlrtRTEI);
  f_st.site = &qc_emlrtRSI;
  g_st.site = &dd_emlrtRSI;
  if ((1 <= SF_UMI_NLOS->size[1]) && (SF_UMI_NLOS->size[1] > 2147483646)) {
    h_st.site = &hc_emlrtRSI;
    check_forloop_overflow_error(&h_st);
  }

  emxFree_real_T(&SF_UMI_NLOS);
  for (k = 0; k < csz_idx_1; k++) {
    sig->data[k] = muDoubleScalarMax(PL_tot_sig_LOS->data[k],
      PL_UMI_NLOS_sig->data[k]);
  }

  emxFree_real_T(&PL_UMI_NLOS_sig);
  st.site = &ld_emlrtRSI;
  x = b_rand();
  k = b_D3D_dist->size[0] * b_D3D_dist->size[1];
  b_D3D_dist->size[0] = 1;
  b_D3D_dist->size[1] = pLOS->size[1];
  emxEnsureCapacity_boolean_T(sp, b_D3D_dist, k, &md_emlrtRTEI);
  csz_idx_1 = pLOS->size[0] * pLOS->size[1];
  for (k = 0; k < csz_idx_1; k++) {
    b_D3D_dist->data[k] = (x <= pLOS->data[k]);
  }

  st.site = &pd_emlrtRSI;
  if (ifWhileCond(&st, b_D3D_dist)) {
    k = sig->size[0] * sig->size[1];
    sig->size[0] = 1;
    sig->size[1] = PL_tot_sig_LOS->size[1];
    emxEnsureCapacity_real_T(sp, sig, k, &nd_emlrtRTEI);
    csz_idx_1 = PL_tot_sig_LOS->size[0] * PL_tot_sig_LOS->size[1];
    for (k = 0; k < csz_idx_1; k++) {
      sig->data[k] = PL_tot_sig_LOS->data[k];
    }
  }

  emxFree_boolean_T(&b_D3D_dist);
  emxFree_real_T(&PL_tot_sig_LOS);
  emlrtHeapReferenceStackLeaveFcnR2012b(sp);
}

void SINR_Channel_Model_5G(const emlrtStack *sp, real_T D2D_dist, real_T h_BS,
  real_T h_MS, real_T fc, real_T tx_p_dBm, real_T bandwidth, const
  emxArray_real_T *Intf_h_BS, const emxArray_real_T *Intf_h_MS, const
  emxArray_real_T *Intf_dist, const emxArray_real_T *Intf_pwr_dBm, real_T
  DS_Desired, real_T CP, boolean_T UMA_notUMI_Model, real_T tx_delta_dBm, real_T
  min_tx_pwr_dBm, boolean_T SINR_model, boolean_T NOMA_Dir, real_T CQI_out_data[],
  int32_T CQI_out_size[2], real_T *Max_SINR_rx_dB_10, real_T *min_tx_p_dBm,
  real_T *PL_dB, real_T *INTF_dBm, real_T *DS_intf_dBm, real_T
  *Min_SINR_rx_dB_10, real_T *Min_INTF_dBm, real_T *Min_Spare_dBm)
{
  static const real_T a[48] = { 0.0, 0.2099, 0.2219, 0.2329, 0.2176, 0.6366,
    0.6448, 0.656, 0.6584, 0.7935, 0.8213, 0.9336, 1.2285, 1.3083, 2.1704,
    2.7105, 4.2589, 4.6003, 5.4902, 5.6077, 6.3065, 6.6374, 7.0427, 8.6523, -4.4,
    -1.2, -3.5, -5.2, -2.5, 0.0, -2.2, -3.9, -7.4, -7.1, -10.7, -11.1, -5.1,
    -6.8, -8.7, -13.2, -13.9, -13.9, -15.9, -17.1, -16.0, -15.7, -21.6, -22.8 };

  static real_T SINR_LIM[16] = { 0.0, -6.9, -5.1, -3.1, -1.4, 0.8, 2.6, 4.7, 6.5,
    8.4, 10.4, 12.3, 14.1, 15.9, 17.75, 19.7 };

  emlrtStack b_st;
  emlrtStack st;
  emxArray_boolean_T b_CQI_out_cur_data;
  emxArray_boolean_T d_CQI_out_cur_data;
  emxArray_boolean_T *b_PL_tot_intf;
  emxArray_real_T *D3D_Intf_dist;
  emxArray_real_T *PL_tot_intf;
  emxArray_real_T *Prob_LOS_intf;
  emxArray_real_T *b_Intf_h_MS;
  emxArray_real_T *r;
  real_T TDL_C_SCALED[48];
  real_T b[2];
  real_T CQI_out_cur_data[1];
  real_T D3D_dist;
  real_T Prob_LOS_sig;
  real_T SF_FS;
  real_T SF_UMA_LOS;
  real_T d;
  real_T d_bp_pl;
  real_T pLOS;
  real_T sum_intf_MP_mW;
  int32_T CQI_out_cur_size[2];
  int32_T b_CQI_out_cur_size[2];
  int32_T tmp_size[2];
  int32_T tmp_data[1];
  int32_T TDL_C_SCALED_tmp;
  int32_T b_k;
  int32_T i;
  int32_T k;
  boolean_T b_SINR_LIM[16];
  boolean_T c_CQI_out_cur_data[1];
  boolean_T exitg1;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  SINR_LIM[0U] = rtMinusInf;
  emlrtHeapReferenceStackEnterFcnR2012b(sp);

  /* 5G SINR Channel Model */
  /*  This file implements a Tapped Delay Line (TDL-C) SINR_model for both UMa and */
  /*  UMi scenarios, per TR 38.901 */
  /*  Use: Main BS vars: D2D_dist, h_BS, h_MS, fc, tx_p_dBm, bandwidth, min_tx_pwr_dBm */
  /*       Intefrence BS: Intf_h_BS, Intf_h_MS, Intf_dist, Intf_pwr_dBm */
  /*       Common Params: DS_Desired, CP,  */
  /*       Main BS SINR_model: UMA_notUMI_Model, tx_delta_dBm, SINR_model */
  /*       Set UMA_notUMI_Model == 1 (UMA), 0 (UMI) */
  /*       Set SINR_model: */
  /*       1 (DS impacts signal power)   */
  /*       0 (DS impacts interference) */
  /*  */
  /*      NOMA_Dir: */
  /*      0 (Signal power decrease does not become interference) */
  /*      1 (Signal power decrease becomes interference) */
  /*       Notes:  DS refers to the state of all signals incoming to the RXs */
  /*       (This is considered worst case). */
  /*  Revision history: */
  /*   Dec 28, 2020)  Changed SF from normrnd to lognrnd, per text, UMA to UMI */
  /*   for PL_intf, updated dp to make clear Hz */
  /*   Dec 29, 2020)  Seperated out DS interference, moved to attenuation */
  /*   portion of SINR, from interference */
  /*   Dec 30, 2020) Verified log-normal definition, lognrnd changed to */
  /*   normrnd.  Modified DS SINR_model to seperate Main BS from interference BS. */
  /*   Updated Multi-path SINR_model to reduce impact with tx power scaling.  While */
  /*   DS is modeled as being the same (desired) for both main and interfering */
  /*   BS. */
  /*   Jan 1, 2021)  Added min SINR, min DS */
  /*   Jan 12, 2021) Added NOMA direction, NOMA_Dir (Signal decrease, */
  /*   interference increase */
  /* UNTITLED2 Summary of this function goes here */
  /*    Detailed explanation goes here */
  *Min_Spare_dBm = -100.0;

  /* Per TR 38.901, table 7.7.2-3 (normalized) (Normalized Delay, power in dB) */
  /* DS_Desired is in us */
  b[0] = DS_Desired;
  b[1] = 1.0;
  for (k = 0; k < 2; k++) {
    for (b_k = 0; b_k < 24; b_k++) {
      TDL_C_SCALED_tmp = b_k + 24 * k;
      TDL_C_SCALED[TDL_C_SCALED_tmp] = a[TDL_C_SCALED_tmp] * b[k];
    }
  }

  /* DS_Desired (ns) is the Delay Spread as observed by the UE */
  /* CP = CP * 1e3; %10^-9; */
  /* Path Loss SINR_model per TR 38.901 */
  /* Antennas */
  /* BS=h_BS; %Per TR 38.901, h_BS=25m */
  /* MS=1.5;  %Per TR 38.901, h_UT=1.5m --> 22.5m */
  /* SINR_model 3D distance */
  /* Shadow Fading */
  /* DS_u = -0.24*log10(1 + fc) - 6.83; %NLOS, table 7.5.6 part 1 TR 38.901 */
  /* DS_sd = 0.16*log10(1+fc ) + 0.28; */
  /* DS = normrnd(DS_u, DS_sd); */
  emxInit_real_T(sp, &D3D_Intf_dist, 2, &w_emlrtRTEI, true);
  emxInit_real_T(sp, &Prob_LOS_intf, 2, &cb_emlrtRTEI, true);
  emxInit_real_T(sp, &PL_tot_intf, 2, &db_emlrtRTEI, true);
  emxInit_real_T(sp, &r, 2, &r_emlrtRTEI, true);
  emxInit_real_T(sp, &b_Intf_h_MS, 2, &g_emlrtRTEI, true);
  emxInit_boolean_T(sp, &b_PL_tot_intf, 2, &i_emlrtRTEI, true);
  if (UMA_notUMI_Model) {
    /* SINR_model selection distance */
    /* fc is in GHZ, so c = 3.0 * 10^8 */
    /* 3.0 * 10^8; */
    d_bp_pl = 4.0 * h_BS * h_MS * fc / 0.3;

    /* 20/3 = 2.0 Ghz / 3.0 * 10^8, footnote 2 in winner+ SINR_model, Table 4.1, see TR 38.901 table 7.4.1.-1 note 1 */
    st.site = &emlrtRSI;
    st.site = &emlrtRSI;
    Prob_LOS_sig = h_MS - h_BS;
    D3D_dist = D2D_dist * D2D_dist + Prob_LOS_sig * Prob_LOS_sig;
    st.site = &emlrtRSI;
    if (D3D_dist < 0.0) {
      emlrtErrorWithMessageIdR2018a(&st, &f_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        4, "sqrt");
    }

    D3D_dist = muDoubleScalarSqrt(D3D_dist);

    /* Since we are outside, always, we consider D2D_dist = D2D_dist_out */
    st.site = &b_emlrtRSI;
    pLOS = PrLOS(D2D_dist, h_MS, true);
    st.site = &c_emlrtRSI;
    SF_UMA_LOS = randn();
    SF_UMA_LOS *= 4.0;

    /* log10(normrnd(0, 7)); %7dB std deviation, random normal, mean 0 */
    /* SF = 0;     */
    /* Per TR 38.901, Table 7.4.1-1 */
    /* LOS SINR_model (only for 10 meters or more) */
    /* PL1 */
    b_st.site = &ub_emlrtRSI;
    if (D3D_dist < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    b_st.site = &ub_emlrtRSI;
    if (fc < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    /* TR 38.901 */
    /* PL2 */
    Prob_LOS_sig = h_BS - h_MS;
    b_st.site = &vb_emlrtRSI;
    if (D3D_dist < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    b_st.site = &vb_emlrtRSI;
    if (fc < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    d = d_bp_pl * d_bp_pl + Prob_LOS_sig * Prob_LOS_sig;
    b_st.site = &vb_emlrtRSI;
    if (d < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    d = muDoubleScalarLog10(d);

    /* TR 38.901 */
    /* Path Loss, free space */
    SF_FS = randn();
    SF_FS *= 7.8;
    b_st.site = &xb_emlrtRSI;
    if (fc < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    b_st.site = &xb_emlrtRSI;
    if (D3D_dist < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    /* %%%%%%%%%%%%%%%%%%%%%%% */
    /* Model descion (PathLoss to device) */
    if (D3D_dist <= d_bp_pl) {
      Prob_LOS_sig = ((22.0 * muDoubleScalarLog10(D3D_dist) + 28.0) + 20.0 *
                      muDoubleScalarLog10(fc)) + SF_UMA_LOS;

      /*  10m<d<d_BP': LOS1 */
    } else {
      Prob_LOS_sig = (((40.0 * muDoubleScalarLog10(D3D_dist) + 28.0) + 20.0 *
                       muDoubleScalarLog10(fc)) - 9.0 * d) + SF_UMA_LOS;

      /*  d_BP'<d<5000m: LOS2  */
    }

    /*  should greater than or equal for free space */
    Prob_LOS_sig = muDoubleScalarMax(((20.0 * muDoubleScalarLog10(fc) + 32.4) +
      30.0 * muDoubleScalarLog10(D3D_dist)) + SF_FS, Prob_LOS_sig);

    /* NLOS */
    SF_UMA_LOS = randn();
    SF_UMA_LOS *= 6.0;
    b_st.site = &ac_emlrtRSI;
    if (D3D_dist < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    b_st.site = &ac_emlrtRSI;
    if (fc < 0.0) {
      emlrtErrorWithMessageIdR2018a(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    SF_FS = b_rand();
    if (SF_FS <= pLOS) {
      *PL_dB = Prob_LOS_sig;
    } else {
      *PL_dB = muDoubleScalarMax(Prob_LOS_sig, (((39.08 * muDoubleScalarLog10
        (D3D_dist) + 13.54) + 20.0 * muDoubleScalarLog10(fc)) - 0.6 * (h_MS -
        1.5)) + SF_UMA_LOS);
    }

    /* [Prob_LOS_sig] = PrLOS(D2D_dist_out,MS_t,UMA_notUMi) */
    /*  LOS probability */
    emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Intf_h_MS->size, *(int32_T (*)[2])
      Intf_h_BS->size, &j_emlrtECI, sp);
    emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Intf_h_MS->size, *(int32_T (*)[2])
      Intf_h_BS->size, &i_emlrtECI, sp);
    emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Intf_h_MS->size, *(int32_T (*)[2])
      Intf_h_MS->size, &h_emlrtECI, sp);
    i = D3D_Intf_dist->size[0] * D3D_Intf_dist->size[1];
    D3D_Intf_dist->size[0] = 1;
    D3D_Intf_dist->size[1] = Intf_dist->size[1];
    emxEnsureCapacity_real_T(sp, D3D_Intf_dist, i, &p_emlrtRTEI);
    k = Intf_dist->size[0] * Intf_dist->size[1];
    for (i = 0; i < k; i++) {
      d = Intf_dist->data[i];
      D3D_Intf_dist->data[i] = d * d;
    }

    i = r->size[0] * r->size[1];
    r->size[0] = 1;
    r->size[1] = Intf_h_MS->size[1];
    emxEnsureCapacity_real_T(sp, r, i, &r_emlrtRTEI);
    k = Intf_h_MS->size[0] * Intf_h_MS->size[1];
    for (i = 0; i < k; i++) {
      r->data[i] = Intf_h_MS->data[i] - Intf_h_BS->data[i];
    }

    i = r->size[0] * r->size[1];
    b_k = r->size[0] * r->size[1];
    r->size[0] = 1;
    emxEnsureCapacity_real_T(sp, r, b_k, &t_emlrtRTEI);
    k = i - 1;
    for (i = 0; i <= k; i++) {
      d = r->data[i];
      d *= d;
      r->data[i] = d;
    }

    emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])D3D_Intf_dist->size, *(int32_T (*)
      [2])r->size, &g_emlrtECI, sp);
    i = D3D_Intf_dist->size[0] * D3D_Intf_dist->size[1];
    b_k = D3D_Intf_dist->size[0] * D3D_Intf_dist->size[1];
    D3D_Intf_dist->size[0] = 1;
    emxEnsureCapacity_real_T(sp, D3D_Intf_dist, b_k, &w_emlrtRTEI);
    k = i - 1;
    for (i = 0; i <= k; i++) {
      D3D_Intf_dist->data[i] += r->data[i];
    }

    st.site = &d_emlrtRSI;
    b_sqrt(&st, D3D_Intf_dist);

    /* Since we are outside, always, we consider D2D_dist = D2D_dist_out */
    /* Prob_Los_Intf = min(18./Intf_dist,1).*(1-exp(-Intf_dist/36)) + exp(-Intf_dist/36); % LOS probability */
    st.site = &e_emlrtRSI;
    b_PrLOS(&st, Intf_dist, h_MS, true, Prob_LOS_intf);
    st.site = &f_emlrtRSI;
    UMA_Model(&st, fc, D3D_Intf_dist, Intf_h_BS, Intf_h_MS, d_bp_pl,
              Prob_LOS_intf, PL_tot_intf);
  } else {
    /* SINR_model selection distance */
    /* fc is in GsHZ, so c = 3.0 * 10^8 */
    /* 3.0 * 10^8;     */
    d_bp_pl = 4.0 * h_BS * h_MS * fc / 0.3;

    /* 20/3 = 2.0 Ghz / 3.0 * 10^8, footnote 2 in winner+ SINR_model, Table 4.1, see TR 38.901 table 7.4.1.-1 note 1 */
    st.site = &g_emlrtRSI;
    st.site = &g_emlrtRSI;
    Prob_LOS_sig = h_MS - h_BS;
    D3D_dist = D2D_dist * D2D_dist + Prob_LOS_sig * Prob_LOS_sig;
    st.site = &g_emlrtRSI;
    if (D3D_dist < 0.0) {
      emlrtErrorWithMessageIdR2018a(&st, &f_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        4, "sqrt");
    }

    D3D_dist = muDoubleScalarSqrt(D3D_dist);

    /* Since we are outside, always, we consider D2D_dist = D2D_dist_out */
    st.site = &h_emlrtRSI;
    Prob_LOS_sig = PrLOS(D2D_dist, h_MS, false);
    st.site = &i_emlrtRSI;
    *PL_dB = UMI_Model(&st, fc, D3D_dist, h_BS, h_MS, d_bp_pl, Prob_LOS_sig);
    emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Intf_h_MS->size, *(int32_T (*)[2])
      Intf_h_BS->size, &f_emlrtECI, sp);
    st.site = &j_emlrtRSI;
    power(&st, Intf_dist, D3D_Intf_dist);
    i = b_Intf_h_MS->size[0] * b_Intf_h_MS->size[1];
    b_Intf_h_MS->size[0] = 1;
    b_Intf_h_MS->size[1] = Intf_h_MS->size[1];
    emxEnsureCapacity_real_T(sp, b_Intf_h_MS, i, &g_emlrtRTEI);
    k = Intf_h_MS->size[0] * Intf_h_MS->size[1];
    for (i = 0; i < k; i++) {
      b_Intf_h_MS->data[i] = Intf_h_MS->data[i] - Intf_h_BS->data[i];
    }

    st.site = &j_emlrtRSI;
    power(&st, b_Intf_h_MS, r);
    emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])D3D_Intf_dist->size, *(int32_T (*)
      [2])r->size, &e_emlrtECI, sp);
    i = D3D_Intf_dist->size[0] * D3D_Intf_dist->size[1];
    b_k = D3D_Intf_dist->size[0] * D3D_Intf_dist->size[1];
    D3D_Intf_dist->size[0] = 1;
    emxEnsureCapacity_real_T(sp, D3D_Intf_dist, b_k, &h_emlrtRTEI);
    k = i - 1;
    for (i = 0; i <= k; i++) {
      D3D_Intf_dist->data[i] += r->data[i];
    }

    st.site = &j_emlrtRSI;
    b_sqrt(&st, D3D_Intf_dist);

    /* Since we are outside, always, we consider D2D_dist = D2D_dist_out */
    /* Prob_Los_Intf = min(18./Intf_dist,1).*(1-exp(-Intf_dist/36)) + exp(-Intf_dist/36); % LOS probability */
    st.site = &k_emlrtRSI;
    b_PrLOS(&st, Intf_dist, h_MS, false, Prob_LOS_intf);
    st.site = &l_emlrtRSI;
    b_UMI_Model(&st, fc, D3D_Intf_dist, Intf_h_BS, Intf_h_MS, d_bp_pl,
                Prob_LOS_intf, PL_tot_intf);
    i = b_PL_tot_intf->size[0] * b_PL_tot_intf->size[1];
    b_PL_tot_intf->size[0] = 1;
    b_PL_tot_intf->size[1] = PL_tot_intf->size[1];
    emxEnsureCapacity_boolean_T(sp, b_PL_tot_intf, i, &i_emlrtRTEI);
    k = PL_tot_intf->size[0] * PL_tot_intf->size[1];
    for (i = 0; i < k; i++) {
      b_PL_tot_intf->data[i] = (PL_tot_intf->data[i] < 0.0);
    }

    st.site = &m_emlrtRSI;
    if (ifWhileCond(&st, b_PL_tot_intf)) {
      /* Handle case where we are too close to the Base Station, NOMA */
      i = PL_tot_intf->size[0] * PL_tot_intf->size[1];
      PL_tot_intf->size[0] = 1;
      PL_tot_intf->size[1] = 1;
      emxEnsureCapacity_real_T(sp, PL_tot_intf, i, &j_emlrtRTEI);
      PL_tot_intf->data[0] = 0.0;
    }
  }

  emxFree_real_T(&D3D_Intf_dist);

  /* Assume frequency flat fading */
  /* sum_intf_MP_mW = 0; */
  /* sum_intf_self_MP_mW = 0; */
  /* Worst Case attenuation SINR_model */
  /* for h = 1:length(Intf_pwr_dBm) */
  /*     for i = 1:length(TDL_C_SCALED) */
  /*         DS_Cur = TDL_C_SCALED(i, 1); %Always positive DS scaled */
  /*         SR = abs(TDL_C_SCALED(i,2)); %Act as attenutation, negative gain */
  /*         if((DS_Cur > CP)) %Only account for elements which are not filtered out by the CP */
  /*             if(h == 1) */
  /*                 intf_dB_MP = tx_p_dBm -PL_tot_sig - SR; %Scaled is negative, so we add */
  /*                 sum_intf_self_MP_mW = sum_intf_self_MP_mW(h) + 10^(intf_dB_MP / 10); */
  /*             end */
  /*             intf_NOMA_dB = Intf_pwr_dBm(h) - PL_tot_intf(h) - SR; %Assume interference also undergoes delay spread interference */
  /*             sum_intf_MP_mW = sum_intf_MP_mW + 10^(intf_NOMA_dB / 10); */
  /*         end */
  /*     end */
  /* end */
  /* sum_intf_MP = () + sum_intf_dB_MP; */
  /* sum_intf_MP_mW = 10^(sum_intf_MP / 10); */
  /* Delay Spread Model */
  /* Caculate multiple other BS Multi-Path loss */
  st.site = &n_emlrtRSI;

  /* This function determine the multipath loss experienced by a single. */
  /* This loss is modeled as interference */
  /* Assume frequency flat fading */
  i = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
  Prob_LOS_intf->size[0] = 1;
  Prob_LOS_intf->size[1] = Intf_pwr_dBm->size[1];
  emxEnsureCapacity_real_T(&st, Prob_LOS_intf, i, &k_emlrtRTEI);
  k = Intf_pwr_dBm->size[1];
  for (i = 0; i < k; i++) {
    Prob_LOS_intf->data[i] = 0.0;
  }

  /* Worst Case attenuation SINR_model    */
  for (TDL_C_SCALED_tmp = 0; TDL_C_SCALED_tmp < 24; TDL_C_SCALED_tmp++) {
    /* Always positive DS scaled */
    Prob_LOS_sig = muDoubleScalarAbs(TDL_C_SCALED[TDL_C_SCALED_tmp + 24]);

    /* Act as attenutation, negative gain */
    if (TDL_C_SCALED[TDL_C_SCALED_tmp] > CP) {
      /* Only account for elements which are not filtered out by the CP */
      emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Intf_pwr_dBm->size, *(int32_T (*)
        [2])PL_tot_intf->size, &b_emlrtECI, &st);

      /* Scaled is negative, so we add */
      i = b_Intf_h_MS->size[0] * b_Intf_h_MS->size[1];
      b_Intf_h_MS->size[0] = 1;
      b_Intf_h_MS->size[1] = Intf_pwr_dBm->size[1];
      emxEnsureCapacity_real_T(&st, b_Intf_h_MS, i, &m_emlrtRTEI);
      k = Intf_pwr_dBm->size[0] * Intf_pwr_dBm->size[1];
      for (i = 0; i < k; i++) {
        b_Intf_h_MS->data[i] = ((Intf_pwr_dBm->data[i] - PL_tot_intf->data[i]) -
          Prob_LOS_sig) / 10.0;
      }

      b_st.site = &qd_emlrtRSI;
      b_power(&b_st, b_Intf_h_MS, r);
      emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Prob_LOS_intf->size, *(int32_T (*)
        [2])r->size, &emlrtECI, &st);
      i = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
      b_k = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
      Prob_LOS_intf->size[0] = 1;
      emxEnsureCapacity_real_T(&st, Prob_LOS_intf, b_k, &o_emlrtRTEI);
      k = i - 1;
      for (i = 0; i <= k; i++) {
        Prob_LOS_intf->data[i] += r->data[i];
      }
    }

    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(&st);
    }
  }

  b_st.site = &rd_emlrtRSI;
  D3D_dist = sum(&b_st, Prob_LOS_intf);

  /* Caclulate Main BS Multi-Path loss */
  st.site = &o_emlrtRSI;
  SF_UMA_LOS = Calc_DS_Inteference(&st, tx_p_dBm, TDL_C_SCALED, CP, *PL_dB);
  i = b_Intf_h_MS->size[0] * b_Intf_h_MS->size[1];
  b_Intf_h_MS->size[0] = 1;
  b_Intf_h_MS->size[1] = Intf_pwr_dBm->size[1];
  emxEnsureCapacity_real_T(sp, b_Intf_h_MS, i, &l_emlrtRTEI);
  k = Intf_pwr_dBm->size[0] * Intf_pwr_dBm->size[1];
  for (i = 0; i < k; i++) {
    b_Intf_h_MS->data[i] = Intf_pwr_dBm->data[i] / 10.0;
  }

  st.site = &p_emlrtRSI;
  b_power(&st, b_Intf_h_MS, Prob_LOS_intf);
  i = b_Intf_h_MS->size[0] * b_Intf_h_MS->size[1];
  b_Intf_h_MS->size[0] = 1;
  b_Intf_h_MS->size[1] = PL_tot_intf->size[1];
  emxEnsureCapacity_real_T(sp, b_Intf_h_MS, i, &n_emlrtRTEI);
  k = PL_tot_intf->size[0] * PL_tot_intf->size[1];
  for (i = 0; i < k; i++) {
    b_Intf_h_MS->data[i] = PL_tot_intf->data[i] / 10.0;
  }

  emxFree_real_T(&PL_tot_intf);
  st.site = &p_emlrtRSI;
  b_power(&st, b_Intf_h_MS, r);
  emlrtSizeEqCheckNDR2012b(*(int32_T (*)[2])Prob_LOS_intf->size, *(int32_T (*)[2])
    r->size, &d_emlrtECI, sp);
  i = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
  b_k = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
  Prob_LOS_intf->size[0] = 1;
  emxEnsureCapacity_real_T(sp, Prob_LOS_intf, b_k, &q_emlrtRTEI);
  k = i - 1;
  for (i = 0; i <= k; i++) {
    Prob_LOS_intf->data[i] -= r->data[i];
  }

  i = b_PL_tot_intf->size[0] * b_PL_tot_intf->size[1];
  b_PL_tot_intf->size[0] = 1;
  b_PL_tot_intf->size[1] = Prob_LOS_intf->size[1];
  emxEnsureCapacity_boolean_T(sp, b_PL_tot_intf, i, &s_emlrtRTEI);
  k = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
  for (i = 0; i < k; i++) {
    b_PL_tot_intf->data[i] = (Prob_LOS_intf->data[i] > 0.0);
  }

  st.site = &q_emlrtRSI;
  if (ifWhileCond(&st, b_PL_tot_intf)) {
    /* Ensure external direct inerference is lower bounded */
    st.site = &r_emlrtRSI;
    b_log10(&st, Prob_LOS_intf);
    i = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
    b_k = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
    Prob_LOS_intf->size[0] = 1;
    emxEnsureCapacity_real_T(sp, Prob_LOS_intf, b_k, &v_emlrtRTEI);
    k = i - 1;
    for (i = 0; i <= k; i++) {
      Prob_LOS_intf->data[i] *= 10.0;
    }
  } else {
    i = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
    Prob_LOS_intf->size[0] = 1;
    Prob_LOS_intf->size[1] = 1;
    emxEnsureCapacity_real_T(sp, Prob_LOS_intf, i, &u_emlrtRTEI);
    Prob_LOS_intf->data[0] = 0.0;
  }

  /* Noise */
  st.site = &s_emlrtRSI;

  /*  AWGN Noise [Thermal noise density = -174dBm/Hz]  */
  /* SINR Model */
  /* Direct Model */
  d = 3.9810717055349858E-21 * bandwidth;
  st.site = &t_emlrtRSI;
  if (d < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  d = muDoubleScalarLog10(d);
  st.site = &u_emlrtRSI;
  d_bp_pl = muDoubleScalarPower(10.0, (10.0 * d + 30.0) / 10.0);
  if (SINR_model) {
    /* Here we remove the cancelled signal power */
    st.site = &v_emlrtRSI;
    Prob_LOS_sig = muDoubleScalarPower(10.0, (tx_p_dBm - *PL_dB) / 10.0) -
      SF_UMA_LOS;

    /* was PL_DB_free_sig, cancellation */
    sum_intf_MP_mW = D3D_dist;
  } else {
    st.site = &w_emlrtRSI;
    Prob_LOS_sig = muDoubleScalarPower(10.0, (tx_p_dBm - *PL_dB) / 10.0);
    sum_intf_MP_mW = D3D_dist + SF_UMA_LOS;
  }

  i = b_PL_tot_intf->size[0] * b_PL_tot_intf->size[1];
  b_PL_tot_intf->size[0] = 1;
  b_PL_tot_intf->size[1] = Prob_LOS_intf->size[1];
  emxEnsureCapacity_boolean_T(sp, b_PL_tot_intf, i, &x_emlrtRTEI);
  k = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
  for (i = 0; i < k; i++) {
    b_PL_tot_intf->data[i] = (Prob_LOS_intf->data[i] == 0.0);
  }

  st.site = &x_emlrtRSI;
  if (!ifWhileCond(&st, b_PL_tot_intf)) {
    i = b_Intf_h_MS->size[0] * b_Intf_h_MS->size[1];
    b_Intf_h_MS->size[0] = 1;
    b_Intf_h_MS->size[1] = Prob_LOS_intf->size[1];
    emxEnsureCapacity_real_T(sp, b_Intf_h_MS, i, &y_emlrtRTEI);
    k = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
    for (i = 0; i < k; i++) {
      b_Intf_h_MS->data[i] = Prob_LOS_intf->data[i] / 10.0;
    }

    st.site = &y_emlrtRSI;
    b_power(&st, b_Intf_h_MS, r);
    st.site = &y_emlrtRSI;
    sum_intf_MP_mW += sum(&st, r);

    /* 10^(sum(Intf_pwr_dBm - PL_DB_free_intf) / 10); */
  } else {
    /* lower bound interference */
  }

  /*  %Signal (mW) */
  /*  %Noise */
  /*  %Intf */
  d = d_bp_pl + sum_intf_MP_mW;
  Prob_LOS_sig /= d;
  st.site = &ab_emlrtRSI;
  if (Prob_LOS_sig < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  Prob_LOS_sig = muDoubleScalarLog10(Prob_LOS_sig);
  *Max_SINR_rx_dB_10 = 10.0 * Prob_LOS_sig;

  /* SINR_rx_dB = 10*log10(SINR_rx)+30; */
  st.site = &bb_emlrtRSI;
  if (SF_UMA_LOS < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  *DS_intf_dBm = 10.0 * muDoubleScalarLog10(SF_UMA_LOS);

  /* mW to dBm */
  /* UE_CQI = SelectCQI(SINR_rx_dB, 0.1); %determine CQI for UE %submit r0 */
  for (i = 0; i < 16; i++) {
    b_SINR_LIM[i] = (SINR_LIM[i] <= *Max_SINR_rx_dB_10);
  }

  eml_find(b_SINR_LIM, tmp_data, tmp_size);
  CQI_out_size[0] = 1;
  CQI_out_size[1] = tmp_size[1];
  TDL_C_SCALED_tmp = tmp_size[0] * tmp_size[1];
  for (i = 0; i < TDL_C_SCALED_tmp; i++) {
    CQI_out_data[i] = (real_T)tmp_data[i] - 1.0;
  }

  /* cqi_index = find(SINR_LIM <= SNR_UPPERBOUND,1,'last'); */
  /* determine CQI for UE %9-25 */
  /* CQI_out == 0 (outage) */
  /* Determine minimum tx_power, used for NOMA */
  /* min_tx_p_dBm = -9999; %Loop has not run */
  if (tx_p_dBm < min_tx_pwr_dBm) {
    *min_tx_p_dBm = -140.0;
  } else {
    *min_tx_p_dBm = min_tx_pwr_dBm;

    /* Set to default */
  }

  st.site = &cb_emlrtRSI;
  if (d < 0.0) {
    emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
      "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
      5, "log10");
  }

  *INTF_dBm = 10.0 * muDoubleScalarLog10(d);

  /* interference dBm */
  *Min_SINR_rx_dB_10 = *Max_SINR_rx_dB_10;
  *Min_INTF_dBm = sum_intf_MP_mW;
  i = (int32_T)((min_tx_pwr_dBm + (-tx_delta_dBm - tx_p_dBm)) / -tx_delta_dBm);
  emlrtForLoopVectorCheckR2012b(tx_p_dBm, -tx_delta_dBm, min_tx_pwr_dBm,
    mxDOUBLE_CLASS, i, &emlrtRTEI, sp);
  TDL_C_SCALED_tmp = 0;
  exitg1 = false;
  while ((!exitg1) && (TDL_C_SCALED_tmp <= i - 1)) {
    pLOS = tx_p_dBm + (real_T)TDL_C_SCALED_tmp * -tx_delta_dBm;

    /* Set minimum     */
    st.site = &db_emlrtRSI;
    SF_UMA_LOS = Calc_DS_Inteference(&st, pLOS, TDL_C_SCALED, CP, *PL_dB);
    if (SINR_model) {
      /* Here we remove the cancelled signal power */
      st.site = &eb_emlrtRSI;
      SF_FS = muDoubleScalarPower(10.0, (pLOS - *PL_dB) / 10.0) - SF_UMA_LOS;

      /* was PL_DB_free_sig, cancellation */
      sum_intf_MP_mW = D3D_dist;
    } else {
      st.site = &fb_emlrtRSI;
      SF_FS = muDoubleScalarPower(10.0, (pLOS - *PL_dB) / 10.0);
      sum_intf_MP_mW = D3D_dist + SF_UMA_LOS;
    }

    /* Calculate the spare power in dBm. */
    st.site = &gb_emlrtRSI;
    st.site = &gb_emlrtRSI;
    d = muDoubleScalarPower(10.0, tx_p_dBm / 10.0) - muDoubleScalarPower(10.0,
      pLOS / 10.0);
    st.site = &gb_emlrtRSI;
    if (d < 0.0) {
      emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    d = muDoubleScalarLog10(d);

    /* Prevent restrict the lower bound of cur_spare_pwr_dBm  */
    /* to -100 to prevent -Inf dBm. */
    SF_UMA_LOS = muDoubleScalarMax(10.0 * d, -100.0);
    if (NOMA_Dir) {
      /* Signal decrease causes interference */
      st.site = &hb_emlrtRSI;
      Prob_LOS_sig = Calc_DS_Inteference(&st, SF_UMA_LOS, TDL_C_SCALED, CP,
        *PL_dB);
      st.site = &ib_emlrtRSI;
      sum_intf_MP_mW = (muDoubleScalarPower(10.0, (SF_UMA_LOS - *PL_dB) / 10.0)
                        + sum_intf_MP_mW) + Prob_LOS_sig;
    } else {
      /* Signal decrease does not cause interference */
    }

    b_k = b_PL_tot_intf->size[0] * b_PL_tot_intf->size[1];
    b_PL_tot_intf->size[0] = 1;
    b_PL_tot_intf->size[1] = Prob_LOS_intf->size[1];
    emxEnsureCapacity_boolean_T(sp, b_PL_tot_intf, b_k, &ab_emlrtRTEI);
    k = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
    for (b_k = 0; b_k < k; b_k++) {
      b_PL_tot_intf->data[b_k] = (Prob_LOS_intf->data[b_k] == 0.0);
    }

    st.site = &jb_emlrtRSI;
    if (!ifWhileCond(&st, b_PL_tot_intf)) {
      b_k = b_Intf_h_MS->size[0] * b_Intf_h_MS->size[1];
      b_Intf_h_MS->size[0] = 1;
      b_Intf_h_MS->size[1] = Prob_LOS_intf->size[1];
      emxEnsureCapacity_real_T(sp, b_Intf_h_MS, b_k, &bb_emlrtRTEI);
      k = Prob_LOS_intf->size[0] * Prob_LOS_intf->size[1];
      for (b_k = 0; b_k < k; b_k++) {
        b_Intf_h_MS->data[b_k] = Prob_LOS_intf->data[b_k] / 10.0;
      }

      st.site = &kb_emlrtRSI;
      b_power(&st, b_Intf_h_MS, r);
      st.site = &kb_emlrtRSI;
      sum_intf_MP_mW += sum(&st, r);

      /* 10^(sum(Intf_pwr_dBm - PL_DB_free_intf) / 10); */
    } else {
      /* lower bound interference */
    }

    d = SF_FS / (d_bp_pl + sum_intf_MP_mW);
    st.site = &lb_emlrtRSI;
    if (d < 0.0) {
      emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
        "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3, 4,
        5, "log10");
    }

    d = muDoubleScalarLog10(d);
    Prob_LOS_sig = 10.0 * d;
    for (b_k = 0; b_k < 16; b_k++) {
      b_SINR_LIM[b_k] = (SINR_LIM[b_k] <= Prob_LOS_sig);
    }

    eml_find(b_SINR_LIM, tmp_data, tmp_size);
    CQI_out_cur_size[0] = 1;
    CQI_out_cur_size[1] = tmp_size[1];
    k = tmp_size[0] * tmp_size[1];
    for (b_k = 0; b_k < k; b_k++) {
      CQI_out_cur_data[b_k] = (real_T)tmp_data[b_k] - 1.0;
    }

    /* cqi_index = find(SINR_LIM <= SNR_UPPERBOUND,1,'last'); */
    emlrtSizeEqCheckNDR2012b(CQI_out_cur_size, CQI_out_size, &c_emlrtECI, sp);
    b_CQI_out_cur_size[0] = 1;
    b_CQI_out_cur_size[1] = tmp_size[1];
    k = tmp_size[1];
    for (b_k = 0; b_k < k; b_k++) {
      c_CQI_out_cur_data[b_k] = (CQI_out_cur_data[b_k] != CQI_out_data[b_k]);
    }

    b_CQI_out_cur_data.data = &c_CQI_out_cur_data[0];
    b_CQI_out_cur_data.size = &b_CQI_out_cur_size[0];
    b_CQI_out_cur_data.allocatedSize = 1;
    b_CQI_out_cur_data.numDimensions = 2;
    b_CQI_out_cur_data.canFreeData = false;
    st.site = &mb_emlrtRSI;
    if (ifWhileCond(&st, &b_CQI_out_cur_data)) {
      exitg1 = true;
    } else {
      *min_tx_p_dBm = pLOS;
      *Min_SINR_rx_dB_10 = Prob_LOS_sig;
      st.site = &nb_emlrtRSI;
      if (sum_intf_MP_mW < 0.0) {
        emlrtErrorWithMessageIdR2018a(&st, &c_emlrtRTEI,
          "Coder:toolbox:ElFunDomainError", "Coder:toolbox:ElFunDomainError", 3,
          4, 5, "log10");
      }

      *Min_INTF_dBm = 10.0 * muDoubleScalarLog10(sum_intf_MP_mW);
      *Min_Spare_dBm = SF_UMA_LOS;
      b_CQI_out_cur_size[0] = 1;
      b_CQI_out_cur_size[1] = tmp_size[1];
      k = tmp_size[1];
      for (b_k = 0; b_k < k; b_k++) {
        c_CQI_out_cur_data[b_k] = (CQI_out_cur_data[b_k] == 0.0);
      }

      d_CQI_out_cur_data.data = &c_CQI_out_cur_data[0];
      d_CQI_out_cur_data.size = &b_CQI_out_cur_size[0];
      d_CQI_out_cur_data.allocatedSize = 1;
      d_CQI_out_cur_data.numDimensions = 2;
      d_CQI_out_cur_data.canFreeData = false;
      st.site = &ob_emlrtRSI;
      if (ifWhileCond(&st, &d_CQI_out_cur_data)) {
        exitg1 = true;
      } else {
        TDL_C_SCALED_tmp++;
        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }
    }
  }

  emxFree_boolean_T(&b_PL_tot_intf);
  emxFree_real_T(&b_Intf_h_MS);
  emxFree_real_T(&r);
  emxFree_real_T(&Prob_LOS_intf);

  /* min_tx_dB =  */
  emlrtHeapReferenceStackLeaveFcnR2012b(sp);
}

/* End of code generation (SINR_Channel_Model_5G.c) */
