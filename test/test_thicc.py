import unittest
import subprocess
import os
import thicc

class TestThicc(unittest.TestCase):

    def test_stage1_valid(self):
        path = "test/data/stage_1/"
        self.runSampleTestsValid(path)

    def test_stage1_invalid(self):
        path = "test/data/stage_1/"
        self.runSampleTestsInvalid(path)

    
    def test_stage2_valid(self):
        path = "test/data/stage_2/"
        self.runSampleTestsValid(path)

    def test_stage2_invalid(self):
        path = "test/data/stage_2/"
        self.runSampleTestsInvalid(path)
    

    def runSampleTestsValid(self, rootpath):
        path = rootpath+"valid/"
        files = os.listdir(path)

        for filename in files:
            #Expected Result
            command = ["gcc", path+filename]
            subprocess.run(command)
            command = ["./a.out"]
            output0 = subprocess.run(command)
            command = ["rm", "a.out"]
            subprocess.run(command)

            #Test Result
            with open(path+filename, "r") as f:
                text = f.read()
            code = thicc.compileC(text)

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

            self.assertTrue(output0.returncode==output.returncode)

    def runSampleTestsInvalid(self, rootpath):
        # Valid
        path = rootpath+"invalid/"
        files = os.listdir(path)

        for filename in files:
            #Test Result
            with open(path+filename, "r") as f:
                text = f.read()
           
            self.assertRaises(Exception, thicc.compileC, text)


if __name__ == "__main__":
    unittest.main()
