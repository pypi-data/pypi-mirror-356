#!/usr/bin/env python3
import os
import argparse
import shutil
import subprocess
from example import full_list, sample_list, python_list
import logging
from ppl_compile import ppl_compile, CompileArgs
from os_system import _os_subprocess, _os_system
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s -\n%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

SUCCESS = 0
FAILURE = 1


class BaseTestFiles:

    def __init__(self, top_dir, chips, file_list, mode, is_full, time_out):
        self.result_message = ""
        self.top_dir = top_dir
        self.file_list = file_list
        self.chips = chips
        self.test_failed_list = []
        self.vali_failed_list = []
        self.time_out_list = []
        self.dubious_pl_list = {}
        self.file_not_found_list = {}
        self.chip_index_map = {
            'bm1684x': 1,
            'bm1688': 2,
            'bm1690': 3,
            'sg2260e': 4,
            'sg2262': 5,
            'sg2262rv': 6,
            'mars3': 7,
            'bm1684xe': 8,
        }
        self.mode = mode
        self.is_full = is_full
        self.time_out = time_out
        self.time_cost_list = []

    def summarize(self):
        self.result_message = f"\n====================== {str(self.__class__.__name__)} test summarize ======================\n"
        if self.file_not_found_list:
            self.result_message += "\n[WARNING]: File does not exist:\n"
            for fileName, _ in self.file_not_found_list.items():
                self.result_message += f"- {fileName}\n"

        if self.test_failed_list:
            self.result_message += "[FAILED]: These PL files failed in compilation:\n"
            for chip, fileName in self.test_failed_list:
                self.result_message += f"- {fileName} tested in PLATFORM: {chip}\n"
        else:
            self.result_message += "[SUCCESS]: All PL files passed compilation\n"

        if self.vali_failed_list:
            self.result_message += "[FAILED]: These PL files do not passed the correctness validation:\n"
            for chip, fileName in self.vali_failed_list:
                self.result_message += f"- {fileName} validated in PLATFORM: {chip}\n"
        else:
            self.result_message += "[SUCCESS]: All correctness validation passed.\n"

        if self.dubious_pl_list:
            self.result_message += "\n[WARNING]: These PL files do not have correctness validation scripts:\n"
            for fileName, _ in self.dubious_pl_list.items():
                self.result_message += f"- {fileName}\n"

        if self.time_out_list:
            self.result_message += "\n[WARNING]: These PL files run time out:\n"
            for chip, fileName in self.time_out_list:
                self.result_message += f"- {fileName} tested in PLATFORM: {chip}\n"

        if self.time_cost_list:
            self.result_message += "\n[INFO]: The time consume summary:\n"
            for chip, time_cost, local_time_list in self.time_cost_list:
                self.result_message += f"- run models for {chip}: {time_cost:.1f} seconds\n"
                for file, ret, output_info, local_time_cost in local_time_list:
                    res = 'SUCCESS' if (ret == 0) else 'FAILED'
                    self.result_message += f"---- test {file} ({res}) [{local_time_cost:.1f} seconds]\n"
                    if ret != 0:
                        self.result_message += f"{output_info}\n"
    def check_test_open(self, case):
        flag = 1 if self.is_full else 0
        if type(case) == list:
            return case[flag]
        else:
            return case

    def get_applicable_tests(self, chip):
        applicable_tests = {}
        chip_index = self.chip_index_map[chip]

        for category, tests in self.file_list.items():
            applicable_tests[category] = [
                test[0] for test in tests
                if self.check_test_open(test[chip_index])
            ]

        return applicable_tests

    def check_file_exists(self, path):
        if not os.path.exists(path):
            self.file_not_found_list[path] = ""
            logging.warning(f"[WARNING]: File does not exist - {path}")
            return False
        else:
            return True

    def test_all(self):
        raise NotImplementedError("Subclasses should implement this method")


class TestPLFiles(BaseTestFiles):

    def __init__(self, pl_file_dir, chips, file_list, save_dir, mode, is_full, time_out):
        super().__init__(pl_file_dir, chips, file_list, mode, is_full, time_out)
        self.save_dir = save_dir
        self.is_full = is_full

    def test_one(self, fileName, chip):
        self.check_file_exists(fileName)
        logging.info(f"+++++++++++ testing {fileName} in {chip} +++++++++++")
        test_opt = "--gen_ref"
        if chip == "sg2260e":
          test_opt = "--gen_ref --opt O3"
        if chip == "sg2262rv":
            cmd = [
                "ppl_compile.py", "--src", fileName, "--chip", "sg2262", test_opt,
                "--mode", self.mode, "--rv"
            ]
        else:
            cmd = [
                "ppl_compile.py", "--src", fileName, "--chip", chip, test_opt,
                "--mode", self.mode
            ]
        ret, output_info = _os_subprocess(cmd, self.time_out)
        # args = CompileArgs()
        # args.src = fileName
        # args.chip = chip
        # args.gen_ref = True
        # args.mode = self.mode
        # args.time_out = self.time_out
        # ret = ppl_compile(args)
        if ret != 0:
            logging.error(f"ppl_compile failed with return code {ret}")
            if ret == 1:
                self.test_failed_list.append((chip, fileName))
            if ret == 2:
                self.time_out_list.append((chip, fileName))
        return ret, output_info



    def verify_one(self, fileName, chip):
        if chip == "sg2262rv":
            chip = "sg2262"
        testFile = fileName.replace(".pl", ".py")
        if os.path.exists(testFile):
            cmd = ["python", testFile, "--chip", chip]
            ret, output_info = _os_subprocess(cmd, self.time_out)
            if ret != 0:
                logging.error(f"verify failed with return code {ret}")
                self.vali_failed_list.append((chip, fileName))
                return ret, output_info
        else:
            logging.warning("File does not exist at the specified path.")
            self.dubious_pl_list[fileName] = ""
        return 0, ""

    def test_all(self):
        for chip in self.chips:
            local_time_cost_list = []
            st = time.time()
            applicable_tests = self.get_applicable_tests(chip)
            for sub_dir, files in applicable_tests.items():
                for file in files:
                    pl_file = os.path.join(self.top_dir, sub_dir, file)
                    st_local = time.time()
                    ret, output_info = self.test_one(pl_file, chip)
                    if ret == 0:
                        ret, output_info = self.verify_one(pl_file, chip)
                    local_time_cost_list.append((pl_file, ret, output_info, time.time()-st_local))
            self.time_cost_list.append((chip, time.time()-st, local_time_cost_list))
        self.summarize()
        return FAILURE if (len(self.file_not_found_list) or len(
            self.vali_failed_list) or len(self.test_failed_list)) else SUCCESS

class TestSampleFiles(BaseTestFiles):
    def __init__(self, sample_dir, chips, file_list, mode, time_out):
        super().__init__(sample_dir, chips, file_list, mode, True, time_out)

    def verify_one(self, script_name, chip, filePath):
        if chip == "sg2262rv":
            chip = "sg2262"
        cmd = [script_name, chip, self.mode]
        ret, output_info = _os_subprocess(cmd, self.time_out)
        if ret != 0:
            logging.error(f"Error from {script_name}: {ret}")
            if ret == 1:
                self.test_failed_list.append((chip, filePath))
            if ret == 2:
                self.time_out_list.append((chip, filePath))
        else:
            logging.info(f"Output from {script_name}: {ret}")
        return ret, output_info

    def test_one(self, filePath, chip):
        logging.info(f"+++++++++++ testing {filePath} in {chip} +++++++++++")
        self.check_file_exists(filePath)
        os.chdir(filePath)
        ret, output_info = self.verify_one("./build.sh", chip, filePath)
        if ret == 0:
            self.verify_one("./run.sh", chip, filePath)
        return ret, output_info

    def test_all(self):
        for chip in self.chips:
            local_time_cost_list = []
            st = time.time()
            applicable_tests = self.get_applicable_tests(chip)
            for sub_dir, files in applicable_tests.items():
                if len(files):
                    filePath = os.path.join(self.top_dir, sub_dir)
                    st_local = time.time()
                    ret, output_info = self.test_one(filePath, chip)
                    local_time_cost_list.append((filePath, ret, output_info, time.time()-st_local))
            self.time_cost_list.append((chip, time.time()-st, local_time_cost_list))
        self.summarize()
        return FAILURE if (len(self.file_not_found_list) or
                           len(self.test_failed_list)) else SUCCESS

class TestPythonFiles(BaseTestFiles):

    def __init__(self, ppl_dir, chips, file_list, mode, time_out):
        super().__init__(ppl_dir, chips, file_list, mode, True, time_out)

    def test_one(self, fileName, chip):
        self.check_file_exists(fileName)
        env = os.environ.copy()
        env['DEBUG'] = '1'
        env['CHIP'] = chip
        env['MODE'] = self.mode
        env['SAVE_DIR'] = os.getcwd()
        os.environ.update(env)
        cmd = ["python3", fileName]
        cmd_str = " ".join(map(str, cmd))
        logging.info("[Running]: {}".format(cmd_str))
        ret, output_info = _os_subprocess(cmd, self.time_out)
        if ret != 0:
            logging.error(f"[Failed]: {cmd_str}")
            if ret == 1:
                self.test_failed_list.append((chip, fileName))
            if ret == 2:
                self.time_out_list.append((chip, fileName))
        else:
            logging.error(f"[success]: {cmd_str}")
        return ret, output_info

    def test_all(self):
        for chip in self.chips:
            local_time_cost_list = []
            st = time.time()
            applicable_tests = self.get_applicable_tests(chip)
            for sub_dir, files in applicable_tests.items():
                for file in files:
                    py_file = os.path.join(self.top_dir, sub_dir, file)
                    st_local = time.time()
                    ret, output_info = self.test_one(py_file, chip)
                    local_time_cost_list.append((py_file, ret, output_info, time.time()-st_local))
            self.time_cost_list.append((chip, time.time()-st, local_time_cost_list))
        self.summarize()
        return FAILURE if (len(self.file_not_found_list)
                           or len(self.test_failed_list)) else SUCCESS


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--reg_save_dir",
                        type=str,
                        default="./regression_out",
                        help="dir to save the test result")
    parser.add_argument("--reg_mode",
                        type=str.lower,
                        default="basic",
                        choices=["basic", "full"],
                        help="chip platform name")
    parser.add_argument("--chip",
                        type=str.lower,
                        default="bm1684x,bm1688,bm1690,sg2262,mars3,bm1684xe,sg2260e,sg2262rv",
                        help="chip platform name")
    parser.add_argument("--mode",
                        default='cmodel',
                        help="target building & running mode")
    parser.add_argument("--time_out",
                        type = int,
                        default = 0,
                        help="timeout")
    args = parser.parse_args()
    if os.path.exists(args.reg_save_dir):
        shutil.rmtree(args.reg_save_dir)
    os.makedirs(args.reg_save_dir)
    os.chdir(args.reg_save_dir)
    ppl_dir = os.getenv('PPL_PROJECT_ROOT')
    chips = args.chip.split(",")
    is_full = True if args.reg_mode == "full" else False

    plTest = TestPLFiles(ppl_dir, chips, full_list, args.reg_save_dir,
                         args.mode, is_full, args.time_out)
    sampleTest = TestSampleFiles(ppl_dir, chips, sample_list, args.mode, args.time_out)
    pyTest = TestPythonFiles(ppl_dir, chips, python_list, args.mode, args.time_out)
    exit_status = 0
    testers = [plTest, sampleTest, pyTest]
    result_message = ""
    for test_runner in testers:
        if not isinstance(test_runner, BaseTestFiles):
            continue
        exit_status = test_runner.test_all() or exit_status
        result_message += test_runner.result_message

    logging.critical(result_message)
    exit(exit_status)
