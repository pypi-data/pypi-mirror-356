#!/usr/bin/env python3

Y, N = True, False

full_list = {
    # (filename,                                              bm1684x, bm1688, bm1690, sg2260e, sg2262, 2262rv, masr3, bm1684xe)
    #                                                         [base, full]
    "regression/unittest/arith":
      [
       ("arith.pl",                                              Y,       Y,      Y,      Y,      N,      Y,     N,      N),
      ],
    "regression/unittest/arith_int":
      [("c_sub_int.pl",                                          N,       N,      N,      N,      N,      N,     N,     N),],
    "regression/unittest/attention":
      [("rotary_embedding_static.pl",                            N,       N,      N,      N,      N,      N,     N,     N),
       ("mlp_left_trans_multicore.pl",                           N,       N,      Y,      N,      N,      N,     N,     N)],
    "regression/unittest/cmp":
      [("greater_fp16.pl",                                       Y,       N,      N,      N,      N,      N,     Y,     N),
       ("equal_int16.pl",                                        Y,       N,      N,      N,      N,      N,     N,     N),],
    "regression/unittest/conv":
      [("Conv2D.pl",                                             Y,       N,      Y,      N,      N,      N,     N,     N),
       ("depthwise2d_int8.pl",                                   Y,       N,    [N,Y],    N,      N,      N,     N,     N),
       ("quant_conv2d_for_deconv2d_int8_asym_int16_int8.pl",     Y,       N,      Y,      N,      N,      N,     N,     N),],
    "regression/unittest/divide":
      [("fp32_tunable_div_multi_core.pl",                        N,       N,      Y,      N,      N,      N,     Y,     N),],
    "regression/unittest/dma":
      [("dma_test.pl",                                           Y,       Y,      Y,      Y,      N,      Y,     N,     N),
       ("dma_nonzero_l2s.pl",                                  [N,Y],     N,      N,      N,      N,      Y,     N,     N),
       ("dma_nonzero_s2s.pl",                                  [N,Y],     N,      N,      N,      N,      Y,     N,     N),],
    "regression/unittest/gather_scatter":
      [
       ("gather_test.pl",                                        Y,       N,      Y,      Y,      N,      Y,     N,      N),
       ("scatter_test.pl",                                       Y,       N,      Y,      Y,      N,      Y,     N,      N),
      ],
    "regression/unittest/hau":
      [("hau_sort_2d.pl",                                        N,       N,      N,      N,      N,      N,     N,     N),
       ("topk.pl",                                               N,       N,      N,      N,      N,      N,     N,     N),
       ("hau.pl",                                                Y,       N,      N,      N,      N,      N,     N,     N),
       ("hau_poll.pl",                                           Y,       N,      Y,      N,      N,      N,     N,     N),],
    "regression/unittest/mask":
      [("mask_select_batch_bcast_bf16_multi_core.pl",            Y,       N,      N,      N,      N,      N,     N,     N),],
    "regression/unittest/matmul":
      [("matmul.pl",                                             Y,       Y,      Y,      Y,      Y,      N,     Y,     Y),
       ("mm_fp32.pl",                                          [N,Y],     N,      N,      N,      N,      N,     N,     N),],
    "regression/unittest/npu":
      [("npu_bcast_fp16.pl",                                   [N,Y],     N,      N,      N,    [N,Y],    N,     N,     N),],
    "regression/unittest/round":
      [("round_bf16.pl",                                       [N,Y],     N,      N,      N,      N,      N,     N,     N),],
    "regression/unittest/rqdq":
      [
       ("dq_test.pl",                                            Y,       Y,      Y,      Y,      Y,      Y,     N,     N),
       ("rq_test.pl",                                            Y,       Y,      Y,      Y,      Y,      Y,     N,     N),
      ],
    "regression/unittest/scalebias":
      [("fp_scale_bias_bf16.pl",                               [N,Y],     N,      N,      N,      N,      N,     N,     N),],
    "regression/unittest/sdma":
      [("sdma.pl",                                               N,       N,      Y,      Y,      N,      N,     N,     N),],
    "regression/unittest/unary":[],
    "examples/cxx/arith":
      [("add_c_dual_loop.pl",                                    N,       N,      N,      N,      N,      N,     N,     N),
       ("add_dyn_block.pl",                                      Y,       Y,      Y,      N,      N,      N,     Y,     N),
       ("add_pipeline.pl",                                       N,       N,    [N,Y],    N,      N,      N,     Y,     N),
       ("add_broadcast.pl",                                      N,       N,    [N,Y],    N,    [N,Y],    N,     Y,     N),],
    "examples/cxx/llm":
      [("attention_dyn.pl",                                      Y,       Y,      Y,      N,      N,      N,     N,     N),
       ("exp.pl",                                                Y,       N,      Y,      Y,      N,      Y,     N,     N),
       ("rope.pl",                                               Y,       N,      Y,      Y,      N,      Y,     N,     N),
       ("flash_attention.pl",                                    Y,       N,      N,      N,      N,      N,     N,     N),
       ("rmsnorm.pl",                                            Y,       N,      Y,      Y,      N,      Y,     N,     N),
       ("mlp_multicore.pl",                                      N,       N,      Y,      N,      N,      N,     N,     N),
       ("swi_glu.pl",                                            Y,       N,      N,      N,    [N,Y],    N,     N,     N),
       ("flash_attention_backward_multicore.pl",                 N,       N,    [N,Y],    N,    [N,Y],    N,     N,     N),
       ("flash_attention_GQA_multicore.pl",                      N,       N,      Y,      Y,      Y,      Y,     N,     N),
       ("paged_attention_multicore.pl",                          N,       N,      Y,      N,      N,      N,     N,     N),],
    "examples/cxx/llm/tgi":
      [("w4a16_matmul.pl",                                       N,       N,      Y,      N,      N,      N,     N,     N),
       ("rmsnorm_small_row.pl",                                  N,       N,      Y,      N,      N,      N,     N,     N)],
    "examples/cxx/matmul":
      [("mm2_fp16_sync.pl",                                      N,       N,      Y,      N,      N,      N,     N,     N),
       ("mm.pl",                                               [N,Y],     N,      N,      N,      N,      N,     N,     N),
      ],
    "regression/unittest/fileload":
      [("test_read.pl",                                          Y,       N,      N,      N,      N,      N,     N,     N),],
    "regression/unittest/pool":
      [("avg_pool2d.pl",                                       [N,Y],     N,      N,      N,      N,      N,     N,     N),],
    "examples/cxx/activation":
      [("softmax_h_dim.pl",                                      Y,       N,    [N,Y],    N,      N,      N,     N,     N),],
    "regression/unittest/func":
      [("sin.pl",                                                Y,       N,      N,      N,      N,      N,     N,     N),
       ("cos.pl",                                              [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("arcsin.pl",                                           [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("arccos.pl",                                           [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("tan.pl",                                              [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("cot.pl",                                                Y,       N,      N,      N,      N,      N,     N,     N),
       ("sqrt.pl",                                             [N,Y],     N,      N,      N,    [Y,Y],    N,     N,     N),
       ("sqrt_mars3_bf16.pl",                                  [N,Y],     N,      N,      N,      N,      N,     Y,     N),
       ("relu.pl",                                             [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("prelu.pl",                                            [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("exp.pl",                                              [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("softplus.pl",                                         [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("mish.pl",                                             [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("sinh.pl",                                             [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("cosh.pl",                                             [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("tanh.pl",                                             [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("arcsinh.pl",                                          [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("arccosh.pl",                                          [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("arctanh.pl",                                          [N,Y],     N,      N,      N,      N,      N,     N,     N),
       ("softsign.pl",                                         [N,Y],     N,      N,      N,      N,      N,     N,     N),],
}

sample_list = {
    # (filename,                      bm1684x, bm1688, bm1690, sg2260e, sg2262, 2262rv, mars3, bm1684xe)
    "samples/add_pipeline":
      [("test",                         Y,       N,      Y,      N,      N,      N,      N,     N),],
    "samples/llama2":
      [("test",                         Y,       N,      N,      N,      N,      N,      N,     N),],
    "regression/unittest/pl_with_cpp":
      [("test",                         Y,       N,      N,      N,      N,      N,      N,     N),],
    "regression/unittest/torch_tpu":
      [("test",                         N,       N,      Y,      N,      N,      N,      N,     N),],
    "regression/unittest/tpu_mlir":
      [("test",                         Y,       N,      N,      N,      N,      N,      N,     N),],
}

python_list = {
    # (filename,                      bm1684x, bm1688, bm1690, sg2260e, sg2262, 2262rv, mars3, bm1684xe)
    "examples/python":
      [("01-element-wise.py",            Y,       Y,      Y,      N,      Y,      N,      N,     N),
       ("02-avg-max-pool.py",            Y,       Y,      N,      N,      N,      N,      N,     N),
       ("03-conv.py",                    N,       N,      N,      N,      N,      N,      N,     N),
       ("03-conv-bm1688.py",             N,       N,      N,      N,      N,      N,      N,     N),
       ("04-matmul.py",                  Y,       N,      N,      N,      N,      N,      N,     N),
       ("04-matmul-bm1688.py",           N,       N,      N,      N,      N,      N,      N,     N),
       ("05-attention-GQA.py",           Y,       N,      Y,      N,      Y,      N,      N,     N),
       ("06-gather-scatter.py",          Y,       N,      N,      N,      N,      N,      N,     N),
       ("07-arange_broadcast.py",        Y,       N,      N,      N,      N,      N,      N,     N),
       ("09-dma.py",                     Y,       N,      N,      N,      N,      N,      N,     N),
       ("10-vc-op.py",                   Y,       N,      N,      N,      N,      N,      N,     N),
       ("11-tiu-transpose.py",           Y,       N,      N,      N,      N,      N,      N,     N),
       ("13-hau.py",                     Y,       N,      N,      N,      N,      N,      N,     N),
       ("14-sdma.py",                    N,       N,      N,      N,      N,      N,      N,     N),
       ("15-rq-dq.py",                   Y,       N,      Y,      N,      Y,      N,      N,     N),
       ("15-rq-dq-bm1688-bm1690.py",     N,       N,      N,      N,      N,      N,      N,     N),
       ("16-multicore.py",               N,       N,      Y,      N,      Y,      N,      N,     N),
       ("17-uint.py",                    Y,       Y,      Y,      N,      N,      N,      N,     N),
       ("19_autotiling.py",              N,       N,      Y,      N,      N,      N,      N,     N),
       ("add_const_fp.py",               N,       N,      Y,      N,      N,      N,      N,     N),
       ],
}
