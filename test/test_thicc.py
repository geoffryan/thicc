import unittest
import subprocess
import os
import thicc

class TestThicc(unittest.TestCase):

    def test_stage1_valid(self):
        path = "test/data/stage_1/"
        self.runSampleTestsValid(path, "m64")

    def test_stage1_invalid(self):
        path = "test/data/stage_1/"
        self.runSampleTestsInvalid(path, "m64")

    #def test_stage1_32_valid(self):
    #    path = "test/data/stage_1/"
    #    self.runSampleTestsValid(path, "m32")

    #def test_stage1_32_invalid(self):
    #    path = "test/data/stage_1/"
    #    self.runSampleTestsInvalid(path, "m32")

    
    def test_stage2_valid(self):
        path = "test/data/stage_2/"
        self.runSampleTestsValid(path, "m64")

    def test_stage2_invalid(self):
        path = "test/data/stage_2/"
        self.runSampleTestsInvalid(path, "m64")
    
    #def test_stage2_32_valid(self):
    #    path = "test/data/stage_2/"
    #    self.runSampleTestsValid(path, "m32")

    #def test_stage2_32_invalid(self):
    #    path = "test/data/stage_2/"
    #    self.runSampleTestsInvalid(path, "m32")
    
    
    def test_stage3_valid(self):
        path = "test/data/stage_3/"
        self.runSampleTestsValid(path, "m64")

    def test_stage3_invalid(self):
        path = "test/data/stage_3/"
        self.runSampleTestsInvalid(path, "m64")
    
    #def test_stage3_32_valid(self):
    #    path = "test/data/stage_3/"
    #    self.runSampleTestsValid(path, "m32")

    #def test_stage3_32_invalid(self):
    #    path = "test/data/stage_3/"
    #    self.runSampleTestsInvalid(path, "m32")
    
    def test_stage4_valid(self):
        path = "test/data/stage_4/"
        self.runSampleTestsValid(path, "m64")

    def test_stage4_invalid(self):
        path = "test/data/stage_4/"
        self.runSampleTestsInvalid(path, "m64")
    
    def test_stage5_valid(self):
        path = "test/data/stage_5/"
        self.runSampleTestsValid(path, "m64")

    def test_stage5_invalid(self):
        path = "test/data/stage_5/"
        self.runSampleTestsInvalid(path, "m64")
    

    def runSampleTestsValid(self, rootpath, genType):
        path = rootpath+"valid/"
        files = os.listdir(path)

        for filename in files:
            if filename[-2:] != ".c":
                continue
            #Expected Result
            flags = ["-Wno-constant-logical-operand", "-Wno-unused-value"]
            if genType == "m32":
                flags += ["-m32"]
            command = ["gcc"]+flags+[path+filename]
            subprocess.run(command)
            command = ["./a.out"]
            output0 = subprocess.run(command)
            command = ["rm", "a.out"]
            subprocess.run(command)

            #Test Result
            with open(path+filename, "r") as f:
                text = f.read()
            code = thicc.compileC(text, genType)

            sname = filename[:-2] + ".s"

            with open(sname, "w") as f:
                f.write(code)

            command = ["gcc", sname]
            subprocess.run(command)
            command = ["./a.out"]
            output = subprocess.run(command)
            command = ["rm", sname]
            subprocess.run(command)
            command = ["rm", "a.out"]
            subprocess.run(command)

            self.assertEqual(output0.returncode,output.returncode,msg=filename)

    def runSampleTestsInvalid(self, rootpath, genType):
        # Valid
        path = rootpath+"invalid/"
        files = os.listdir(path)

        for filename in files:
            #Test Result
            with open(path+filename, "r") as f:
                text = f.read()
           
            self.assertRaises(thicc.exception.ThiccError, thicc.compileC, text, genType)


if __name__ == "__main__":
    unittest.main()
