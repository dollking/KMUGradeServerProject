from GradeServer.database import dao
from datetime import datetime
from GradeServer.model.members import Members
from GradeServer.model.registeredCourses import RegisteredCourses
from GradeServer.model.problems import Problems
from GradeServer.model.submittedFiles import SubmittedFiles
from GradeServer.model.submissions import Submissions
from GradeServer.model.languages import Languages
from GradeServer.model.languagesOfCourses import LanguagesOfCourses
from GradeServer.model.registeredProblems import RegisteredProblems
from GradeServer.utils.utilMessages import unknown_error, get_message
from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.otherResources import OtherResources
from GradeServer.resource.routeResources import RouteResources
from sqlalchemy import and_, func, update


'''
Select Langues
'''
def select_languages(courseId):
    return dao.query(LanguagesOfCourses.languageIndex,
                     Languages.languageName,
                     Languages.languageVersion).\
               join(Languages,
                    LanguagesOfCourses.languageIndex == Languages.languageIndex).\
               filter(LanguagesOfCourses.courseId == courseId)
               
               

def get_course_name(courseId):
    try:
        courseName = dao.query(RegisteredCourses.courseName).\
                         filter(RegisteredCourses.courseId == courseId).\
                         first().\
                         courseName
        return courseName
    except Exception as e:
        return unknown_error(get_message('dbError'))

def get_member_name(memberId):
    try:
        memberName = dao.query(Members.memberName).\
                         filter(Members.memberId == memberId).\
                         first().\
                         memberName
        return memberName
    except Exception as e:
        return unknown_error(get_message('dbError'))

def get_submission_info(memberId, courseId, problemId):
    try:
        submissionInfo = dao.query(func.max(Submissions.submissionCount).\
                                    label(OtherResources.const.SUBMISSION_COUNT),
                                    func.max(Submissions.solutionCheckCount).\
                                    label(OtherResources.const.SOLUTION_CHECK_COUNT),
                                    func.max(Submissions.viewCount).\
                                    label(OtherResources.const.VIEW_COUNT)).\
                              filter(Submissions.memberId == memberId,
                                     Submissions.courseId == courseId,
                                     Submissions.problemId == problemId).\
                              first()
        submissionCount = submissionInfo.submissionCount + 1
        solutionCheckCount = submissionInfo.solutionCheckCount
        viewCount = submissionInfo.viewCount
    except:
        submissionCount = 1
        solutionCheckCount = 0
        viewCount = 0
    return submissionCount, solutionCheckCount, viewCount

def insert_submitted_files(memberId, courseId, problemId, fileIndex, fileName, filePath, fileSize):
    submittedFiles = SubmittedFiles(memberId = memberId,
                                    courseId = courseId,
                                    problemId = problemId,
                                    fileIndex = fileIndex,
                                    fileName = fileName,
                                    filePath = filePath,
                                    fileSize = fileSize)                
    dao.add(submittedFiles)
    
def get_used_language_index(usedLanguageName):
    try:
        usedLanguageIndex = dao.query(Languages.languageIndex).\
                           filter(Languages.languageName == usedLanguageName).\
                           first().\
                           languageIndex
    except Exception as e:
        return unknown_error(get_message('dbError'))
    return usedLanguageIndex

def get_problem_info(problemId, problemName):
    try:
        problemPath, limitedTime, limitedMemory, solutionCheckType, isAllInputCaseInOneFile, numberOfTestCase = dao.query(Problems.problemPath,
                                                                                                                          Problems.limitedTime,
                                                                                                                          Problems.limitedMemory,
                                                                                                                          Problems.solutionCheckType,
                                                                                                                          RegisteredProblems.isAllInputCaseInOneFile,
                                                                                                                          RegisteredProblems.numberOfTestCase).\
                                                                                                                    join(RegisteredProblems, Problems.problemId == RegisteredProblems.problemId).\
                                                                                                                    filter(Problems.problemId == problemId).\
                                                                                                                    first()
        problemCasesPath = '%s/%s_%s_%s' %(problemPath, problemId, problemName, solutionCheckType)
    except Exception as e:
        return unknown_error(get_message('dbError'))
    return problemPath, limitedTime, limitedMemory, solutionCheckType, isAllInputCaseInOneFile, numberOfTestCase, problemCasesPath

def get_used_language_version(courseId, usedLanguage):
    try:
        usedLanguageVersion = dao.query(Languages.languageVersion).\
                                  join(LanguagesOfCourses, LanguagesOfCourses.languageIndex == Languages.languageIndex).\
                                  filter(LanguagesOfCourses.courseId == courseId,
                                         LanguagesOfCourses.languageIndex == usedLanguage).\
                                  first().\
                                  languageVersion
    except Exception as e:
        return unknown_error(get_message('dbError'))
    return usedLanguageVersion

def delete_submitted_files_data(memberId, problemId, courseId):
    deleteData = dao.query(SubmittedFiles).\
                     filter(and_(SubmittedFiles.memberId == memberId,
                                 SubmittedFiles.problemId == problemId,
                                 SubmittedFiles.courseId == courseId)).\
                     delete()
                     
def insert_to_submissions(courseId, memberId, problemId, submissionCount, solutionCheckCount, viewCount, usedLanguageIndex, sumOfSubmittedFileSize):
    submissions = Submissions(memberId = memberId,
                              problemId = problemId,
                              courseId = courseId,
                              submissionCount = submissionCount,
                              solutionCheckCount = solutionCheckCount,
                              viewCount = viewCount,
                              status = ENUMResources.const.JUDGING,
                              codeSubmissionDate = datetime.now(),
                              sumOfSubmittedFileSize = sumOfSubmittedFileSize,
                              usedLanguageIndex = usedLanguageIndex)
    dao.add(submissions)
