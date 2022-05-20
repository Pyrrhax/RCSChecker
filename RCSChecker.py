import os
import sys
import time
import psutil
from fnmatch import fnmatch


class RCSChecker:
    class Feature:
        def __init__(self, name, processFeature, fileFeature):
            self.name = name
            self.processFeature = processFeature
            self.fileFeature = fileFeature

    def __init__(self):
        self.featureLib = []
        self.featureLib.append(self.Feature('飞秋', 'feiq.exe', '*feiq*.exe'))
        self.featureLib.append(self.Feature('向日葵', 'sunloginclient', '*sunloginclient*.exe'))
        self.resultFiles = dict()
        self.resultProcesses = dict()

    @staticmethod
    def printBanner():
        print('\
     ____   ____ ____   ____ _               _\n\
    |  _ \ / ___/ ___| / ___| |__   ___  ___| | _____ _ __\n\
    | |_) | |   \___ \| |   | |_ \ / _ \/ __| |/ / _ \ __|\n\
    |  _ <| |___ ___) | |___| | | |  __/ (__|   <  __/ |\n\
    |_| \_\\\\____|____/ \____|_| |_|\___|\___|_|\_\___|_|\
    ', end="\n")
        print("Remote Control Software Checker V0.1   本程序用于检测当前主机是否存在向日葵或飞秋")

    def memoryCheck(self):
        print("\n-进程检测:")
        detected = False
        for proc in psutil.process_iter():
            for feature in self.featureLib:
                if feature.processFeature in proc.name().lower():
                    detected = True
                    if feature.name not in self.resultProcesses:
                        self.resultProcesses.update({feature.name: [{proc.name(): [proc.pid]}]})
                    else:
                        for process in self.resultProcesses[feature.name]:
                            if proc.name() in process:
                                process[proc.name()].append(proc.pid)
                            else:
                                self.resultProcesses[feature.name].append({proc.name(): [proc.pid]})
                        pass
        if not detected:
            print("进程检测完成，未检测到相关进程。\n")
        else:
            for key in self.resultProcesses:
                print("检测到" + key + "正在运行:")
                for process in self.resultProcesses[key]:
                    for item in process.keys():
                        print("进程名:" + item + " 进程ID" + str(process[item]))

    def diskCheck(self):
        print("\n-文件检测:")
        detected = False
        for diskPart in psutil.disk_partitions():
            if diskPart.fstype == "NTFS":
                baseDir = diskPart.device
                sys.stdout.write("\r正在扫描:" + baseDir)
                sys.stdout.flush()
                for root, dirs, files in os.walk(baseDir):
                    if "$Recycle.Bin" in root:
                        del dirs[:]
                    if "C:\\Windows" in root:
                        del dirs[:]
                    nestedLevels = root.split('\\')
                    if len(nestedLevels) == 5:
                        del dirs[:]
                    for file in files:
                        path = os.path.join(root, file)
                        for feature in self.featureLib:
                            if fnmatch(path, feature.fileFeature):
                                detected = True
                                if feature.name not in self.resultFiles:
                                    self.resultFiles.update({feature.name: [path]})
                                else:
                                    self.resultFiles[feature.name].append(path)
        sys.stdout.write("\r")
        sys.stdout.flush()
        if not detected:
            print("硬盘检测完成,未检测到相关文件。")
        else:
            for key in self.resultFiles:
                print("检测到" + key + "可执行程序:")
                for file in self.resultFiles[key]:
                    print(file)
        print()

    def checkAll(self):
        self.printBanner()
        self.memoryCheck()
        self.diskCheck()


if __name__ == '__main__':
    a = RCSChecker()
    a.checkAll()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " 完成", end=" ")
    input("按Enter键关闭窗口。")
