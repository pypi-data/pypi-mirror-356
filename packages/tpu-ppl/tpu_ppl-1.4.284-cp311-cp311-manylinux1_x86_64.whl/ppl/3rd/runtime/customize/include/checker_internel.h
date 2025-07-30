#pragma once
#include "ppl_helper.h"
#include "assert.h"

// dma maroc
#define GDMA_VALUE_DIR_S2L  0
#define GDMA_VALUE_DIR_L2S  1
#define GDMA_VALUE_DIR_S2S  2
#define GDMA_VALUE_DIR_L2L  3
#define GDMA_VAULE_DIR_NUM  4

#define GDMA_VALUE_FORMAT_FLOAT32  0
#define GDMA_VALUE_FORMAT_INT16    1
#define GDMA_VALUE_FORMAT_UINT8    2
#define GDMA_VALUE_FORMAT_INT8     3
#define GDMA_VALUE_FORMAT_FLOAT16  4
#define GDMA_VALUE_FORMAT_NUM 5

#define LMEM_TAG                (0x1ful)

#if defined(__bm1686__)
  #define MAX_TPU_CORE_NUM 2
# elif defined(__mars3__)
  #define MAX_TPU_CORE_NUM 1
# elif defined(__sg2260__)
  #define MAX_TPU_CORE_NUM 8
# elif defined(__sg2260e__) || defined(__sg2380__)
  #define MAX_TPU_CORE_NUM 4
# elif defined(__sg2262__)
  #define MAX_TPU_CORE_NUM 64
#endif

#ifdef __mars3__
  #define STATIC_MEM_SIZE 0x800
#else
  #define STATIC_MEM_SIZE 0x10000
#endif
#if defined(__sg2260__) || defined(__sg2260e__)
  #define GLOBAL_MEM_START_ADDR 0x0UL
# elif defined(__mars3__) || defined(__sg2262__) || defined(__sg2380__)
  #define GLOBAL_MEM_START_ADDR 0x80000000UL
#else
  #define GLOBAL_MEM_START_ADDR 0x100000000UL
#endif

#ifdef __bm1684xe_
  #define MAX_GMEM_BIT            (35)
# elif defined(__bm1686__)
  #define MAX_GMEM_BIT            (36)
#else
  #define MAX_GMEM_BIT            (40)
#endif
#define MAX_GMEM_SIZE           (1ull << MAX_GMEM_BIT)
#define CONFIG_GLOBAL_MEM_SIZE 0x10000

#ifdef __bm1686_
 #define NNVLC_ALIGN_SHIFT       4
#else
 #define NNVLC_ALIGN_SHIFT       7
#endif
#define NNVLC_ALIGN_BYTES       (1 << NNVLC_ALIGN_SHIFT)

#define SRC_IS_LOCAL(direction) \
    ((direction) == GDMA_VALUE_DIR_L2L || (direction) == GDMA_VALUE_DIR_L2S)
#define DST_IS_LOCAL(direction) \
    ((direction) == GDMA_VALUE_DIR_S2L || (direction) == GDMA_VALUE_DIR_L2L)

#define FORMAT_IS_FLOAT(format) \
    ((format) == GDMA_VALUE_FORMAT_FLOAT32 || (format) == GDMA_VALUE_FORMAT_FLOAT16)

#define  ADD_TAG(addr, mask, tag) \
  (((addr) & (mask)) | (((u64)tag) << MAX_GMEM_BIT))
#define  CALC_STATIC_ADDR(addr) \
  (ADD_TAG(addr, STATIC_MEM_SIZE - 1, SMEM_TAG) | (1 << 26))

#define  CALC_LOCAL_ADDR(mem_idx, mem_offset) \
  ADD_TAG((mem_idx * LOCAL_MEM_SIZE + mem_offset), LOCAL_MEM_SIZE * NPU_NUM - 1, LMEM_TAG)

// tiu maroc
#define SIGN(dtype) ((dtype) & 0x1)
#define FP8TYPE(dtype) ((dtype) >> 5)
#define PRECISION(dtype) (((dtype) >> 1) & 0xf)
#define IS_FLOAT(dtype) (dtype==DT_FP32 || dtype==DT_FP16 || dtype==DT_BFP16 || dtype==DT_FP8E5M2 || dtype==DT_FP8E4M3 || dtype==DT_FP20)
#define GETSIGN(dtype) (IS_FLOAT(dtype) ? FP8TYPE(dtype) : SIGN(dtype))

#define WIDTH(dtype) tpu_data_type_bits(dtype)
#define DSIZE(dtype) tpu_data_type_size(dtype)
#define ALIGNED_OR_USER(stride) ((stride) == NULL ? 0 : 3)
#define IS_FLOAT(dtype) (dtype==DT_FP32 || dtype==DT_FP16 || dtype==DT_BFP16 || dtype==DT_FP8E5M2 || dtype==DT_FP8E4M3 || dtype==DT_FP20)
#define ASSERT(cond) assert(cond)

typedef enum {
  GDMA_FUNC_NONE       = 0,
  GDMA_FUNC_TRANS      = 1, // NC Transpose or Matrix Transpose
  GDMA_FUNC_BROADCAST  = 3,
} GDMA_FUNC_TYPE;

typedef enum {
  GDMA_ARE_NOP = 0,
  GDMA_ARE_MUL = 1,
  GDMA_ARE_MAX = 2,
  GDMA_ARE_MIN = 3,
  GDMA_ARE_ADD = 4,
} GDMA_ARE_OPCODE_TYPE;

typedef enum {
  INT8 = 0,
  FP16 = 1,
  FP32 = 2,
  INT16 = 3,
  INT32 = 4,
  BFP16 = 5,
  INT4 = 6,
  FP8 = 7,
  FP20 = 8,
  TF32 = 9,
} PREC;

typedef enum {
  GDMA_INT8 = 0,
  GDMA_FP16 = 1,
  GDMA_FP32 = 2,
  GDMA_INT16 = 3,
  GDMA_INT32 = 4,
  GDMA_BF16 = 5,
  GDMA_FP20 = 6,
  GDMA_FP8_E4M3 = 7,
  GDMA_FP8_E5M2 = 8,
  GDMA_FORMAT_NUM,
} GDMA_FORMAT;

typedef enum {
  // S: systerm memory: dram and l2sram
  GDMA_S2L = 0,
  GDMA_L2S = 1,
  GDMA_S2S = 2,
  GDMA_L2L = 3,
  GDMA_DIR_NUM,
} GDMA_DIRECTION;

typedef enum {
  AR_MUL = 0,
  AR_NOT = 1,
  AR_ADD = 2,
  AR_SUB = 3,
  AR_MAX = 4,
  AR_MIN = 5,
  AR_LOGIC_SHIFT = 6,
  AR_AND = 7,
  AR_OR = 8,
  AR_XOR = 9,
  AR_SG = 10,
  AR_SE = 11,
  AR_DIV = 12,
  AR_SL = 13,
  AR_DATA_CONVERT = 14,
  AR_ADD_SATU = 15,
  AR_SUB_SATU = 16,
  // AR_CLAMP = 17,
  AR_MAC = 18,
  AR_COPY = 19,
  AR_MUL_SATU = 20,
  AR_AR_SHIFT = 21,
  AR_ROTATE_SHIFT = 22,
  // AR_MULDHR = 23, // not support
  // AR_EU_IDX_GEN = 24,
  // AR_NPU_IDX_GEN = 25,
  AR_ABS = 26,
  AR_FSUBABS = 27,
  // AR_COPY_MB = 28, // not support
  AR_GET_FIRST_ONE = 29,
  AR_GET_FIRST_ZERO = 30,
  AR_DIFF_ABS = 32
} AR_OP;

static inline int tpu_get_dma_dtype(data_type_t dtype) {
    switch (dtype)
    {
    case DT_INT8:
    case DT_UINT8:
        return GDMA_INT8;
    case DT_INT16:
    case DT_UINT16:
        return GDMA_INT16;
    case DT_FP16:
        return GDMA_FP16;
    case DT_BFP16:
        return GDMA_BF16;
    case DT_INT32:
    case DT_UINT32:
        return GDMA_INT32;
    case DT_FP8E4M3:
        return GDMA_FP8_E4M3;
    case DT_FP8E5M2:
        return GDMA_FP8_E5M2;
    case DT_FP32:
    case DT_TF32:
        return GDMA_FP32;
    case DT_FP20:
        return GDMA_FP20;
    default:
        ASSERT(0);
        return -1;
    }
}

static inline int get_gdma_format_type_len(int t) {
  switch (t) {
    case GDMA_INT8:
    case GDMA_FP8_E4M3:
    case GDMA_FP8_E5M2:
      return 1;
    case GDMA_FP16:
    case GDMA_BF16:
    case GDMA_INT16:
      return 2;
    case GDMA_FP32:
    case GDMA_INT32:
      return 4;
  }
  return 0;
}

inline static int get_npu_index(u32 local_addr) {
  return (local_addr / LOCAL_MEM_SIZE);
}

inline static int get_bytesize(PREC precision) {
  int bytesize = 4;
  if (precision == INT8 || precision == INT4 || precision == FP8) {
    bytesize = 1;
  } else if (precision == INT16 || precision == FP16 || precision == BFP16) {
    bytesize = 2;
  }
#ifdef __sg2262__
  else if (precision == FP4) {
    bytesize = 1;
  }
#endif
  return bytesize;
}

inline static bool is_float_prec(PREC precision) {
#ifdef __sg2262__
  return (precision == FP32 || precision == FP16 || precision == BFP16 || precision == FP4 ||
          precision == FP8 || precision == TF32);
#endif
  return (precision == FP32 || precision == FP16 || precision == BFP16 || precision == FP20 ||
          precision == FP8 || precision == TF32);
}

inline static bool is_fixed_prec(PREC precision) {
  return (precision == INT4 || precision == INT8 ||
          precision == INT16 || precision == INT32);
}

inline static bool is_half_fp_prec(PREC precision) {
  return (precision == FP16 || precision == BFP16);
}

static inline int is_lmem(u64 addr) {
  return (addr >= LOCAL_MEM_START_ADDR &&
          addr < (LOCAL_MEM_SIZE * NPU_NUM + LOCAL_MEM_START_ADDR));
}

static inline int is_smem(u64 addr) {
  return addr >= STATIC_MEM_START_ADDR &&
         addr < (STATIC_MEM_START_ADDR + STATIC_MEM_SIZE);
}

static inline int is_gmem(u64 addr) {
  addr &= (MAX_GMEM_SIZE - 1);
  return addr >= 0 &&
         addr < (GLOBAL_MEM_START_ADDR + CONFIG_GLOBAL_MEM_SIZE);
}

static inline int is_l2mem(u64 addr) {
  addr &= (MAX_GMEM_SIZE - 1);
  return (addr >= L2_SRAM_START_ADDR &&
          addr < (L2_SRAM_START_ADDR  + L2_SRAM_SIZE));
}

static inline local_addr_t tpu_npu_addr(local_addr_t addr) {
    return addr & (LOCAL_MEM_SIZE - 1);
}


