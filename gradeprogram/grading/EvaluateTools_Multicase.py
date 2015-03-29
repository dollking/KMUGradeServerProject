from subprocess import call
from EvaluateTools import EvaluateTools

class EvaluateTools_multicase(EvaluateTools):
    def __init__(self, usingLang, limitTime, answerPath, version, gradeMethod, caseCount, runFileName, problemName, filePath):
        EvaluateTools.__init__(self, usingLang, limitTime, answerPath, version, gradeMethod, runFileName, problemName, caseCount)
        self.filePath  = filePath
        
    def Solution(self):
        count = 0
        _list = []
        command = self.MakeCommand()
        
        for i in range(1, self.caseCount+1):
            # input.txt file copy
            try:
                call('input.txt', shell = True) # ...ing....
                call('cp ' + self.answerPath + self.problemName + '_case' + str(i) + '.in input.txt', shell = True) # ...ing...
            except Exception as e:
                print e
                return 'error'
                
            # program run
            call(command, shell = True)
            
            answerFile = open(self.answerPath + self.problemName + '_case' + str(i) + '.out', 'r') # answer output open
            stdOutput = open('output.txt', 'r') # student output open
            
            answer = answerFile.read()
            student = stdOutput.read()
            
            answerFile.close()
            stdOutput.close()
            
            answer = answer.strip('\r\n')
            student = student.strip('\r\n')
            
            if answer != student:
                count += 1
                _list.append(i)
           
        if count == 0:
            return 100
        else:
            return int( ((self.caseCount - count) * 100) / self.caseCount )
        
    def Checker(self):
        count = 0
        _list = []
        command = self.MakeCommand()
        call('cp ' + self.answerPath + self.problemName + '.out checker.out', shell = True)
        
        for i in range(1, self.caseCount+1):
            # input.txt file copy
            try:
                call('input.txt', shell = True) # ...ing....
                call(self.answerPath + self.problemName + '_case' + str(i) + '.in input.txt', shell = True) # ...ing...
            except Exception as e:
                print e
                return 'error'
         
            # program run
            call(command, shell = True)
            
            call('./checker.out 1>result.txt', shell = True)
            rf = open('reuslt.txt', 'r')
            
            score = rf.readline()
            
            rf.close()
            
            if int(score) != 100:
                count += 1
                _list.append(i)
           
        if count == 0:
            return 100
        else:
            return int( ((self.caseCount - count) * 100) / self.caseCount )
        
        def MakeCaseList(_list):
            wf = open(self.filePath + 'caselist.txt', 'w')
            size = len(_list)
            
            wf.wrtie(str(size))
            
            for i in size:
                rf = open(self.answerPath + self.problemName + '_case' + str(_list[i]) + '.in', 'r')
                case = rf.readlines()
                rf.close()
                
                if case[-1].find('\n'):
                    case[-1] = case[-1] + '\n'
                
                wf.write(case)
                
            wf.close()