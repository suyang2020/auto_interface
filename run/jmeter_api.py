#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import subprocess


class JmeterApi:

    def execcmd(self, command):
        print(f"command={command}")
        output = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
            universal_newlines=True)
        stderrinfo, stdoutinfo = output.communicate()
        print(f"stderrinfo={stderrinfo}")
        print(f"stdoutinfo={stdoutinfo}")
        print("returncode={0}".format(output.returncode))

    # def execjmxs(self, Num_Threads, Loops):
    #     tmpstr = ''
    #     with open(self.script_file, "r", encoding="utf-8") as file:
    #         tmpstr = Template(file.read()).safe_substitute(
    #             num_threads=Num_Threads,
    #             loops=Loops
    #         )
    #     now = self.getDateTime()
    #     tmpjmxfile = SCRIPT_DIR + r"/T{0}XL{1}{2}.jmx".format(
    #         Num_Threads, Loops, now)
    #     with open(tmpjmxfile, "w+", encoding="utf-8") as file:
    #         file.writelines(tmpstr)
    #     jtlfilename = RESULT_DIR + "/result{0}.jtl".format(now)
    #     htmlreportpath = REPORT_DIR + "/htmlreport{0}".format(now)
    #     if not os.path.exists(htmlreportpath):
    #         os.makedirs(htmlreportpath)
    #     # execjmxouthtml = f"cmd.exe /c {JMETER_Home} -n -t {tmpjmxfile} -l {csvfilename} -e -o {htmlreportpath}"
    #     execjmxouthtml = f"cmd.exe /c {JMETER_PATH} -n -t {JmxTemlFileName} -l {jtlfilename}"
    #     self.execcmd(execjmxouthtml)

    def script_jmx(self, jmeter_path, result_jtl_file, script_jmx_file, log_file):
        '''执行jmx脚本文件，并生成jtl结果文件'''
        if os.path.exists(result_jtl_file):
            os.remove(result_jtl_file)
        if os.path.exists(log_file):
            os.remove(log_file)
        if os.path.exists(log_file):
            fb = open(log_file, 'w')
            fb.close()
        sh = f"{jmeter_path} -n -t {script_jmx_file} -l {result_jtl_file} -j {log_file}"
        # sh = f"{jmeter_path} -n -t {script_jmx_file} -l {result_jtl_file}"
        os.system(sh)


if __name__ == '__main__':
    pass
    # jmeter = JmeterApi()
    # jmeter.jmx()
