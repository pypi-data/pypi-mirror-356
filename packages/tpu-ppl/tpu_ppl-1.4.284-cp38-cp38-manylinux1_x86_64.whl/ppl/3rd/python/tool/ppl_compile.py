#!/usr/bin/env python3
import os
import logging
import argparse
import subprocess
import shutil
import numpy as np
import re
import glob
import warnings
from profiling_parser import *
from os_system import _os_system, _os_system

# return 0-success 1-failed 2-timeout
args = None

def custom_formatwarning(msg, category, *args, **kwargs):
    return f'\033[91m{category.__name__}\033[0m: {msg}\n'


def deprecated_option(cond, msg):
    if cond:
        warnings.formatwarning = custom_formatwarning
        warnings.warn(msg, DeprecationWarning)


def shell_source(script):
    """Sometime you want to emulate the action of"source" in bash,
    settings some environment variables. Here is a way to do it."""
    pipe = subprocess.Popen('/bin/bash -c "source %s; env"' % script,
                            stdout=subprocess.PIPE,
                            shell=True)
    output = pipe.communicate()[0]
    for line in output.splitlines():
        line_decode = line.decode()
        if len(line_decode.split("=")) > 1:
            key, value = line.decode().split("=", 1)
            os.environ.update({key: value})
    print("[Success]: source {}".format(script))


class CompileArgs:

    def __init__(self):
        self.src = None
        self.chip = "bm1684x"
        self.gen_ref = False
        self.gen_test = False
        self.autotune = False
        self.profiling = False
        self.out = None
        self.disable_print_ir = False
        self.disable_pipline = False
        self.disable_canonicalize = False
        self.gdb = False
        self.desc = False
        self.mode = "cmodel"
        self.devid = 0
        self.time_out = 0


class PPL_Convertion_Tool:

    def __init__(self, args):
        srcs = args.src.split(":")
        self.cpp_files = []
        self.pl_files = []
        for src in srcs:
            if not os.path.exists(src):
                print("[ERROR] file {} not exists!".format(src))
                exit(1)
            if src.endswith(".pl"):
                self.pl_files.append(src)
                continue
            if src.endswith(".cpp"):
                self.cpp_files.append(src)
                continue
        self.pl_file = self.pl_files[0]
        self.chip = args.chip
        if self.chip == "bm1688":
            self.chip_inner = "A2"
        elif self.chip == "bm1690":
            self.chip_inner = "sg2260"
        else:
            self.chip_inner = self.chip
        # self.out_name = self.out_name
        self.out_name = self.auto_set_out_name()
        self.out_dir = args.out
        self.opt_level = "--" + args.opt
        self.opt_level = "--O1" if args.disable_pipline else self.opt_level
        self.opt_level = "--O0" if args.disable_canonicalize else self.opt_level
        self.print_ir = "" if args.disable_print_ir else "--print-ir"
        self.frontend_mlir = self.out_name + "_frontend.mlir"
        self.opt_mlir = self.out_name + "_opt.mlir"
        self.ref_final_mlir = self.out_name + "_ref.mlir"
        self.final_mlir = self.out_name + "_final.mlir"
        self.auto_remove_files = list()
        self.current_path = os.path.abspath(os.getcwd())
        self.target_path = os.path.abspath(
            os.path.join(self.current_path, "test_" + self.out_name))
        self.data_path = ''
        self.gen_ref = args.gen_ref
        self.gen_test = args.gen_test
        self.use_gdb = args.gdb
        self.desc = args.desc
        self.mode = args.mode
        self.devid = args.devid
        self.time_out = args.time_out
        self.extra_cflags = args.extra_cflags
        self.extra_ldflags = args.extra_ldflags
        self.extra_includes = args.extra_include_paths
        self.extra_plflags = args.extra_plflags
        self.extra_links = args.extra_link_paths

    def auto_set_out_name(self):
        file_name = os.path.basename(self.pl_file)
        out_name = os.path.splitext(file_name)[0]
        return out_name if len(out_name) >= 1 else ""

    def creat_test_dir(self, create_ext_dir):
        if not self.out_dir is None:
            self.target_path = self.out_dir

        if os.path.exists(self.target_path):
            shutil.rmtree(self.target_path)

        self.data_path = os.path.join(self.target_path, "data")
        if not os.path.exists(self.target_path):
            os.mkdir(self.target_path)
        if not os.path.exists(os.path.join(self.target_path, "host")):
            os.mkdir(os.path.join(self.target_path, "host"))
        if not os.path.exists(os.path.join(self.target_path, "device")):
            os.mkdir(os.path.join(self.target_path, "device"))
        if not os.path.exists(os.path.join(self.target_path, "include")):
            os.mkdir(os.path.join(self.target_path, "include"))
        if create_ext_dir:
            if not os.path.exists(self.data_path):
                os.mkdir(self.data_path)
            if not os.path.exists(os.path.join(self.target_path, "src")):
                os.mkdir(os.path.join(self.target_path, "src"))
            if not os.path.exists(os.path.join(self.target_path, "profiling")):
                os.mkdir(os.path.join(self.target_path, "profiling"))

    def gen_target_file(self):
        desc_cmd = ""
        if self.desc:
            desc_cmd = "--desc"
        self.creat_test_dir(False)
        cmd = [
            "ppl-compile", self.pl_file, "--print-debug-info", self.print_ir,
            "--chip {}".format(self.chip), desc_cmd, self.opt_level, "--g",
            "--o {}".format(self.target_path), "--rv" if args.rv else ""
        ]
        return _os_system(cmd)

    def gen_test_file(self):
        desc_cmd = ""
        if self.desc:
            desc_cmd = "--desc"
        self.creat_test_dir(True)
        cmd = [
            "ppl-compile", self.pl_file, "--print-debug-info", self.print_ir,
            "--gen-test", desc_cmd, "--chip {}".format(self.chip),
            self.opt_level, "--g", "--o {}".format(self.target_path),
            "--rv" if args.rv else ""
        ]
        return _os_system(cmd)

    def gen_pio_with_cpp_file(self):
        self.creat_test_dir(True)
        ret = 0
        for pl_file in self.pl_files:
            cmd = [
                "ppl-compile", pl_file, "--print-debug-info", self.print_ir,
                "--chip {}".format(self.chip), self.opt_level, "--g", "--mode 4",
                "--o {}".format(self.target_path), "--rv" if args.rv else ""
            ]
            ret = _os_system(cmd)
            if ret != 0:
                print("[ERROR] ppl-compile failed!")
                return ret
        return ret

    def gen_autotune_file(self):
        desc_cmd = ""
        if self.desc:
            desc_cmd = "--desc"
        self.creat_test_dir(True)
        cmd = [
            "ppl-compile", self.pl_file, "--print-debug-info", self.print_ir,
            desc_cmd, "--chip {}".format(self.chip), self.opt_level,
            "--g", "--o {}".format(self.target_path), "--rv" if args.rv else ""
        ]
        if self.chip == "bm1690":
            cmd += ["--autotune {}".format(self.mode)]
        else:
            cmd += ["--gen-test"]
        return _os_system(cmd)

    def gen_all_file(self):
        self.creat_test_dir(True)
        desc_cmd = ""
        if self.desc:
            desc_cmd = "--desc"
        cmd = [
            "ppl-compile", self.pl_file, "--print-debug-info", self.print_ir,
            "--gen-test", "--gen-ref", desc_cmd, "--chip {}".format(self.chip),
            self.opt_level, "--g", "--o {}".format(self.target_path),
            "--rv" if args.rv else ""
        ]
        return _os_system(cmd)

    def restruct_dirs(self, extra_dirs):
        rst = ""
        dirs = extra_dirs.split(":")
        for dir in dirs:
            # change to absolute path
            if not os.path.isabs(dir):
                dir = os.path.realpath(dir)
            rst += dir + ":"
        return rst

    ## build ppl reference test
    def build_code(self):
        os.environ["TPUKERNEL_DEV_MODE"] = self.mode

        cmake_file = os.path.join(os.environ["PPL_RUNTIME_PATH"],
                                  "scripts/{}.cmake".format(self.mode))
        shutil.copy(cmake_file, os.path.join(self.target_path,
                                             "CMakeLists.txt"))
        extra_include_dirs = self.restruct_dirs(self.extra_includes)
        extra_link_dirs = self.restruct_dirs(self.extra_links)

        if len(self.cpp_files) > 0:
            for cpp_file in self.cpp_files:
                shutil.copy(cpp_file, os.path.join(self.target_path, "src"))
        if not os.path.exists(os.path.join(self.target_path, "build")):
            os.mkdir(os.path.join(self.target_path, "build"))
        os.chdir(os.path.join(self.target_path, "build"))
        ret = _os_system([
            "cmake .. -DDEBUG={} -DCHIP={} -DDEV_MODE={} -DEXTRA_IDIRS={} -DEXTRA_LDIRS={} -DEXTRA_CFLAGS={} -DEXTRA_LDFLAGS={}"
            .format(self.use_gdb, self.chip, self.mode, extra_include_dirs,
                    extra_link_dirs, self.extra_cflags, self.extra_ldflags)
        ])
        if ret != 0:
            print("[ERROR] build code cmake failed!")
            return ret
        if self.use_gdb:
            ret = _os_system(["make install VERBOSE=1"])
        else:
            ret = _os_system(["make install"])
        if ret != 0:
            print("[ERROR] build code make failed!")
            return ret
        os.chdir(os.environ["PPL_PROJECT_ROOT"])
        return 0

    def validate(self, with_ref=False):
        os.environ["PPL_DUMP_IR"] = "1"
        os.environ["PPL_CACHE_PATH"] = os.path.join(self.target_path, "cache")
        os.environ["PPL_FILE_NAME"] = self.out_name
        if self.desc:
            os.environ["PPL_SRC_PATH"] = os.environ["PPL_PROJECT_ROOT"]
            os.environ["PPL_WORK_PATH"] = self.target_path
        if self.chip == "bm1684x" or self.chip == "bm1684xe" or self.chip == "bm1690" or self.chip == "bm1688" or \
              self.chip == "sg2262" or self.chip == "mars3" or self.chip == "sg2260e":
            if self.chip == "bm1684x" or self.chip == "bm1684xe" or self.chip == "bm1688" or self.chip == "mars3" or self.chip == "sg2260e":
                runtime_lib = "libsophon/bmlib"
            else:
                runtime_lib = "tpuv7-runtime-emulator"

            os.environ["LD_LIBRARY_PATH"] = os.path.join(
                self.target_path, "lib") + ":" + os.path.join(
                    os.environ["PPL_RUNTIME_PATH"],
                    "%s/lib/" % self.chip)
            if self.mode == "cmodel":
                os.environ["LD_LIBRARY_PATH"] += ":" + os.path.join(
                        os.environ["PPL_RUNTIME_PATH"], "%s/%s/lib" %
                        (self.chip, runtime_lib))
            os.environ["PPL_DATA_PATH"] = self.data_path
            if self.chip == "bm1690" or self.chip == "sg2262":
                os.environ["TPU_KERNEL_PATH"] = os.path.join(
                    os.path.relpath(self.target_path, os.getcwd()), "lib")
                if self.mode == "cmodel":
                    os.environ["PPL_KERNEL_PATH"] = os.path.join(
                    self.target_path, "lib/libcmodel.so")
                    runtime_lib_path = os.path.join(
                        os.environ["PPL_RUNTIME_PATH"],
                        "%s/%s/lib" % (self.chip, runtime_lib))
                    os.environ["TPU_EMULATOR_PATH"] = os.path.join(
                        runtime_lib_path, "libtpuv7_emulator.so")
                    os.environ["TPU_SCALAR_EMULATOR_PATH"] = os.path.join(
                        runtime_lib_path, "libtpuv7_scalar_emulator.so")
                else:
                    os.environ["PPL_KERNEL_PATH"] = os.path.join(
                    self.target_path, "lib/libkernel.so")
            cmd = []
            if self.use_gdb:
                cmd.append("gdb --args")
            cmd.append(os.path.join(self.target_path, "test_case"))
            cmd.append(self.devid)
            ret = _os_system(cmd)
            if ret != 0:
                print("[ERROR] run test_case failed!")
                return ret
            print("export LD_LIBRARY_PATH=" + os.environ["LD_LIBRARY_PATH"])
            print("export PPL_DATA_PATH=" + os.environ["PPL_DATA_PATH"])
            print("[cmd:]", cmd)
            ret = self.compare(with_ref)
            if ret != 0:
                print("[ERROR] compare result failed!")
                return ret
            return 0

    def build_code_for_qemu(self):
        os.environ["CHIP_ARCH"] = self.chip
        os.environ["TPUKERNEL_DEV_MODE"] = self.mode
        main_path = os.path.join(self.target_path, "src")
        files = os.listdir(main_path)
        file_name, file_extension = os.path.splitext(files[0])
        output_file = file_name
        os.chdir(self.target_path)
        llvm_bin_path = os.path.join(os.environ["PPL_THIRD_PARTY_PATH"],
                                     "2380/llvm-project/build_elf/install")
        clang_path = os.path.join(os.environ["PPL_THIRD_PARTY_PATH"],
                                  "2380/clang")
        toolchain_path = os.path.join(
            os.environ["PPL_THIRD_PARTY_PATH"],
            "2380/riscv64-unknown-elf-toolsuite-17.9.0-2023.10.0/")
        include_path = os.path.join(
            toolchain_path, "lib/gcc/riscv64-unknown-elf/12.2.1/include/")

        cmd = [
            os.path.join(clang_path, "clang-18"),
            # os.path.join(llvm_bin_path, "bin/clang"),
            "-frecord-command-line",
            "-fintegrated-as",
            "-menable-experimental-extensions",
            "-target {}".format("riscv64-unknown-elf"),
            "-march=rv64imafdcv_zicsr_zifencei_zfh_zba_zbb_zvfh_xsfvfnrclipxfqf_xsfvfwmaccqqq_xsfvqmaccqoq_xsfvcp_xsgmat",
            "-mabi=lp64d -mcmodel=medany -ffunction-sections -fdata-sections",
            "--gcc-toolchain={}".format(toolchain_path),
            "-O0 -DNDEBUG  -Wl,--gc-sections -nostartfiles",
            "-L{}".format(
                os.path.join(os.environ["PPL_RUNTIME_PATH"],
                             "sg2380/sifive_x280mc8/lib/release")),
            "-T{}".format(
                os.path.join(os.environ["PPL_RUNTIME_PATH"],
                             "sg2380/samples/metal.cxx.ld")),
            "-I{}".format(
                os.path.join(os.environ["PPL_RUNTIME_PATH"],
                             "customize/include")),
            "-I{}".format(
                os.path.join(os.environ["PPL_RUNTIME_PATH"], "customize/src")),
            "-I{}".format(
                os.path.join(os.environ["PPL_RUNTIME_PATH"], "kernel")),
            "-I{}".format(
                os.path.join(os.environ["PPL_RUNTIME_PATH"],
                             "sg2380/include")),
            "-I{}".format(os.path.join(self.target_path, "device")),
            "-I{}".format(os.path.join(self.target_path, "host")),
            "-I{}".format(os.path.join(self.target_path, "include")),
            "-I{}".format(include_path),
            os.path.join(main_path, files[0]),
            "-o {}".format(os.path.join(self.target_path, output_file)),
            "-lm -lc -lgcc -lmetal -lmetal-gloss"
        ]
        ret = _os_system(cmd)
        if ret != 0:
            print("[ERROR] build code failed!")
            return ret

        script_path = os.path.join(os.environ["PPL_RUNTIME_PATH"],
                                   "sg2380/scripts/run-qemu-c1.sh")
        cmd = [
            "sh", script_path, "-kernel",
            os.path.join(self.target_path, output_file)
        ]
        cmd_str = ""
        for s in cmd:
            cmd_str += str(s) + " "
        print("[Running]: {}".format(cmd_str))
        os.chdir(os.path.join(self.target_path, "data"))
        with open('print.log', 'w+') as log_file:
            process = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            for line in process.stdout:
                line = line.decode().strip()
                if line.startswith("data:"):
                    log_file.write(line + '\n')
                elif line.startswith("input:"):
                    log_file.write(line + '\n')
                else:
                    print(line)
            process.wait()
        ret = process.returncode
        if ret == 0 or ret == 100:
            print("[Success]: {}".format(cmd_str))
        else:
            print("[!Error]: {}".format(cmd_str))
            return 1
        return 0
        os.chdir(os.environ["PPL_PROJECT_ROOT"])

    def validate_for_qemu(self, with_ref=False):
        os.chdir(os.path.join(self.target_path, "data"))
        outputs = []
        inputs = []
        with open('print.log', 'r') as file:
            for line in file:
                if line.strip().startswith('data') and line.strip().endswith(
                        'end'):
                    data_str = line[len('data:'):-len(" , end")]
                    data_list = [float(x) for x in data_str.split(',')]
                    data_array = np.array(data_list)
                    outputs.append(data_array)
                elif line.strip().startswith(
                        'input') and line.strip().endswith('end'):
                    data_str = line[len('input:'):-len(" , end")]
                    data_list = [float(x) for x in data_str.split(',')]
                    data_array = np.array(data_list)
                    inputs.append(data_array)
        if with_ref:
            mem_num = len(outputs) // 2
        else:
            mem_num = len(outputs)
        for i in range(mem_num):
            if with_ref:
                with open(self.out_name + "_ref_" + str(i) + ".out",
                          "w+") as f:
                    outputs[2 * i].astype(np.float32).tofile(f)
            with open(self.out_name + "_tar_" + str(i) + ".out", "w+") as f:
                outputs[2 * i + 1].astype(np.float32).tofile(f)

        for i in range(len(inputs)):
            with open(self.out_name + "_fp32_" + str(i) + ".in", "w+") as f:
                inputs[i].astype(np.float32).tofile(f)

        ret = self.compare(with_ref)
        os.chdir(os.environ["PPL_PROJECT_ROOT"])
        return ret

    def profiling_cmodel(self, autotune):
        if self.chip == "bm1684x" or self.chip == "bm1684xe" or self.chip == "bm1690" or self.chip == "bm1688" or self.chip == "sg2262" or self.chip == "mars3":
            os.environ["FILE_DUMP_CMD"] = self.out_name
            if self.chip == "bm1684x" or self.chip == "bm1684xe" or self.chip == "bm1688" or self.chip == "mars3":
                runtime_lib = "libsophon/bmlib"
            else:
                runtime_lib = "tpuv7-runtime-emulator"

            os.environ["LD_LIBRARY_PATH"] = os.path.join(
                self.target_path, "lib") + ":" + os.path.join(
                    os.environ["PPL_RUNTIME_PATH"],
                    "%s/lib/" % self.chip + ":" +
                    os.path.join(os.environ["PPL_RUNTIME_PATH"], "%s/%s/lib" %
                                 (self.chip, runtime_lib)))
            os.environ["PPL_DATA_PATH"] = self.data_path
            if self.chip == "bm1690" or self.chip == "sg2262":
                os.environ["PPL_KERNEL_PATH"] = os.path.join(
                    self.target_path, "lib/libcmodel.so")
                runtime_lib_path = os.path.join(
                    os.environ["PPL_RUNTIME_PATH"],
                    "%s/%s/lib" % (self.chip, runtime_lib))
                os.environ["TPU_EMULATOR_PATH"] = os.path.join(
                    runtime_lib_path, "libtpuv7_emulator.so")
                os.environ["TPU_SCALAR_EMULATOR_PATH"] = os.path.join(
                    runtime_lib_path, "libtpuv7_scalar_emulator.so")
                os.environ["TPU_KERNEL_PATH"] = os.path.join(
                    self.target_path, "lib")
                # os.environ["TPUKERNEL_FIRMWARE_PATH"] = os.path.join(runtime_lib_path, "libtpuv7_emulator.so")
            profiling_dir = os.path.join(self.target_path, "profiling")
            os.chdir(profiling_dir)
            cmd = [
                os.path.join(self.target_path, "test_case"),
                str(self.devid)
            ]
            if autotune and self.chip == "bm1690":
                cmd = [
                    os.path.join(self.target_path, "autotune_test"),
                    os.path.join(self.target_path, "test_case"), profiling_dir,
                    str(self.devid)
                ]
            ret = _os_system(cmd)
            if ret != 0:
                print("[ERROR] run test_case failed!")
                return ret

            os.chdir(os.path.join(os.environ["PPL_THIRD_PARTY_PATH"],
                                  "PerfAI"))
            cmd = [
                "./AutoRunner.sh", "-d", profiling_dir, "-e", self.chip_inner
            ]
            ret = _os_system(cmd)
            if ret != 0:
                print("[ERROR] profilling failed!")
                return ret
            parse_profiling(profiling_dir, self.chip)

    def profiling_pcie(self, autotune):
        if self.chip == "bm1684x" or self.chip == "bm1684xe" or self.chip == "bm1690" or self.chip == "bm1688" or self.chip == "sg2262" or self.chip == "mars3":
            os.environ["BMLIB_ENABLE_ALL_PROFILE"] = "1"
            os.environ["PPL_DATA_PATH"] = self.data_path
            os.environ["LD_LIBRARY_PATH"] += ":" + os.path.join(
                        os.environ["PPL_RUNTIME_PATH"],
                        "%s/lib/" % self.chip)
            if self.chip == "bm1690" or self.chip == "sg2262":
                os.environ["PPL_KERNEL_PATH"] = os.path.join(
                    self.target_path, "lib/libkernel.so")
            profiling_dir = os.path.join(self.target_path, "profiling")
            os.chdir(profiling_dir)
            cmd = [
                os.path.join(self.target_path, "test_case"),
                str(self.devid)
            ]
            if autotune and self.chip == "bm1690":
                cmd = [os.path.join(self.target_path, "autotune_test"),
                       os.path.join(self.target_path, "test_case"),
                       profiling_dir, str(self.devid)]
            ret = _os_system(cmd)
            if ret != 0:
                print("[ERROR] run test_case failed!")
                return ret
            os.environ["PYTHONPATH"] = os.environ[
                "PPL_PROJECT_ROOT"] + "/third_party:" + os.environ["PYTHONPATH"]
            if self.chip == "bm1684x" or self.chip == "bm1684xe":
                cmd = [
                    "python -m bmprofile --mode time bmprofile_data-%d pro_out" %
                    self.devid
                ]
                ret = _os_system(cmd)
                if ret != 0:
                    print("[ERROR] profiling failed!")
                    return ret
                parse_bm1684x_pcie(profiling_dir)
            elif self.chip == "bm1690":
                pattern = os.path.join("*", "cdm_profile_data_dev*")
                dirs = glob.glob(pattern)
                for item in dirs:
                    parts = item.split('/')
                    sub = f"{parts[0]}/" if len(parts) > 1 else ""
                    o_path = f"result_profiling/{sub}output"
                    cmd = [
                        f"python3 -m bigTpuProfile {item} {o_path} --disable_doc"
                    ]
                    print(cmd)
                    ret = _os_system(cmd)
                    if ret != 0:
                        print("[ERROR] profiling failed!")
                        return ret
                parse_profiling(profiling_dir, self.chip)

    def profiling(self, autotune=False):
        if self.mode == "pcie":
            self.profiling_pcie(autotune)
        else:
            self.profiling_cmodel(autotune)

    def compare(self, with_ref=False):
        inp_npz = os.path.join(self.data_path, self.out_name + "_input.npz")
        tar_npz = os.path.join(self.data_path, self.out_name + "_tar.npz")
        if with_ref:
            ref_npz = os.path.join(self.data_path, self.out_name + "_ref.npz")
            cmd = [
                "npz_help.py", "compare", ref_npz, tar_npz,
                "-vv --tolerance 0.99,0.99"
            ]
            return _os_system(cmd)
        else:
            return 0

    def file_clean(self):
        for n in self.auto_remove_files:
            if not os.path.exists(n):
                continue
            os.remove(n)


def ppl_compile(args):
    os.environ["PPL_SRC_DIR_PATH"] = os.path.dirname(os.path.abspath(args.src))
    os.environ["PPL_DEVID"] = str(args.devid)
    os.environ["CHIP"] = args.chip
    tool = PPL_Convertion_Tool(args)
    ret = -1
    srcs = args.src.split(":")
    with_cpp = False
    if args.chip == "sg2262" and args.rv:
        os.environ["TVGEN_USING_TXP"] = "1"
    # check if there is cpp file in srcs
    for src in srcs:
        if src.endswith(".cpp"):
            with_cpp = True
            break
    if args.profiling:
        ret = tool.gen_test_file()
        if ret != 0:
            print("[!Error]: gen test file failed")
            return ret
        ret = tool.build_code()
        if ret != 0:
            print("[!Error]: build code failed")
            return ret
        status = tool.profiling()
    elif args.autotune:
        ret = tool.gen_autotune_file()
        if ret != 0:
            print("[!Error]: gen autotune file failed")
            return ret
        ret = tool.build_code()
        if ret != 0:
            print("[!Error]: build code failed")
            return ret
        status = tool.profiling(True)
    elif with_cpp:
        if args.gen_ref or args.gen_test:
            print(
                "[!Error]: if set cpp files, gen_ref and gen_test must be false"
            )
            return -1
        ret = tool.gen_pio_with_cpp_file()
        if ret != 0:
            print("[!Error]: gen pio with cpp file failed")
            return ret
        if args.chip == "bm1684x" or args.chip == "bm1684xe" or args.chip == "bm1690" \
            or args.chip == "bm1688" or args.chip == "sg2262" or args.chip == "mars3" or args.chip == "sg2260e":
            ret = tool.build_code()
            if ret != 0:
                print("[!Error]: build code failed")
                return ret
            ret = tool.validate(False)
            if ret != 0:
                print("[!Error]: validate failed")
                return ret
        elif args.chip == "sg2380":
            tool.build_code_for_qemu()
            if tool.mode != 'cmodel':
                print(
                    f"Target is build in {tool.mode} mode, please run on {tool.mode} device."
                )
            else:
                tool.validate_for_qemu(False)
    elif args.gen_ref:
        ret = tool.gen_all_file()
        if ret != 0:
            print("[!Error]: gen all file failed")
            return ret
        if args.chip == "bm1684x" or args.chip == "bm1684xe" or args.chip == "bm1690" \
            or args.chip == "bm1688" or args.chip == "sg2262" or args.chip == "mars3" or args.chip == "sg2260e":
            ret = tool.build_code()
            if ret != 0:
                print("[!Error]: build code failed")
                return ret
            ret = tool.validate(True)
            if ret != 0:
                print("[!Error]: validate failed")
                return ret
        elif args.chip == "sg2380":
            tool.build_code_for_qemu()
            if tool.mode != 'cmodel':
                print(
                    f"Target is build in {tool.mode} mode, please run on {tool.mode} device."
                )
            else:
                tool.validate_for_qemu(True)
    elif args.gen_test:
        ret = tool.gen_test_file()
        if ret != 0:
            print("[!Error]: gen test file failed")
            return ret
        if args.chip == "bm1684x" or args.chip == "bm1684xe" or args.chip == "bm1690" \
            or args.chip == "bm1688" or args.chip == "sg2262" or args.chip == "mars3" or args.chip == "sg2260e":
            ret = tool.build_code()
            if ret != 0:
                print("[!Error]: build code failed")
                return ret
            ret = tool.validate(False)
            if ret != 0:
                print("[!Error]: validate failed")
                return ret
        elif args.chip == "sg2380":
            tool.build_code_for_qemu()
            if tool.mode != 'cmodel':
                print(
                    f"Target is build in {tool.mode} mode, please run on {tool.mode} device."
                )
            else:
                tool.validate_for_qemu(False)
    else:
        ret = tool.gen_target_file()
    # if not args.debug:
    #     tool.file_clean()
    return ret


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--src",
                        required=True,
                        type=str,
                        help="pl or cpp files")
    # parser.add_argument("--PPL_RUNTIME_PATH", required=True, help="runtime path")
    parser.add_argument("--chip",
                        required=True,
                        type=str.lower,
                        choices=[
                            'bm1684x', 'bm1684xe', 'bm1690', 'bm1688',
                            'sg2380', 'sg2262', 'mars3', 'sg2260e'
                        ],
                        help="chip platform name")
    parser.add_argument("--gen_ref",
                        default=False,
                        action='store_true',
                        help="generate reference kernel func")
    parser.add_argument("--gen_test",
                        default=False,
                        action='store_true',
                        help="generate test func")
    parser.add_argument("--autotune",
                        default=False,
                        action='store_true',
                        help="do autotune")
    parser.add_argument("--profiling",
                        default=False,
                        action='store_true',
                        help="do profile")
    parser.add_argument("--out", type=str.lower, required=False, help="")
    parser.add_argument("--disable_print_ir",
                        action='store_true',
                        help="disable to print ir")
    parser.add_argument("--disable_pipline",
                        action='store_true',
                        help="disable to do ppl pipeline")
    parser.add_argument("--disable_canonicalize",
                        action='store_true',
                        help="disable to do ppl canonicalize")
    parser.add_argument("--gdb",
                        default=False,
                        action='store_true',
                        help="use gdb")
    parser.add_argument("--desc",
                        action='store_true',
                        help="generate descriptor mode")
    parser.add_argument("--opt",
                        default='O2',
                        help="Optimization level, e.g. O2, O3")
    parser.add_argument("--mode",
                        default='cmodel',
                        help="target building & running mode")
    parser.add_argument("--rv",
                        default=False,
                        action='store_true',
                        help="use rv mode for sg2262")
    parser.add_argument("--devid", type=int, default=0, help="tpu device id")
    parser.add_argument("--time_out", type=int, default=0, help="time_out")
    parser.add_argument(
        "--extra_cflags",
        type=str,
        default="",
        help=
        "optional list of compiler flags, separated by \":\", e.g. \"\-DDEBUG:-O2\""
    )
    parser.add_argument(
        "--extra_plflags",
        type=str,
        default="",
        help=
        "optional list of ppl flags, separated by \":\", e.g. \"\-DTEST:-DTEST1\""
    )
    parser.add_argument(
        "--extra_ldflags",
        type=str,
        default="",
        help="optional list of link flags, separated by \":\", e.g. pthread:z")
    parser.add_argument(
        "--extra_include_paths",
        type=str,
        default="",
        help=
        "optional list of include paths, separated by \":\", e.g. include:include2"
    )
    parser.add_argument(
        "--extra_link_paths",
        type=str,
        default="",
        help="optional list of link paths, separated by \":\", e.g. lib:lib2")

    args = parser.parse_args()
    # if args.out_name:
    #     print("Warning: --out_name has no effect, is a deprecated param")
    deprecated_option(
        args.profiling,
        "--profiling deprecated, please use --autotune. Ref to examples/cxx/arith/add_pipeline.pl"
    )

    ret = ppl_compile(args)
    if ret != 0:
        sys.exit(ret)
