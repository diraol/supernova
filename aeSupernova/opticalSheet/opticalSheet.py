#encoding: utf8
from aeSupernova.opticalSheet.ColumnsController import *
from aeSupernova.opticalSheet.QuestionController import *
from aeSupernova.opticalSheet.OpticalSheetController import *
from aeSupernova.opticalSheet.OpticalSheetPrinter import *
from aeSupernova.opticalSheet.QualitativeQuestionnairePrinter import *
from aeSupernova.header.Header import Header

from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from django import http
from django.http import *

def openSite(request):
    if request.user.is_authenticated(): 
        header = Header()
        header.setTermFunction('loadOpticalSheet($("#headerTimePeriod").val(),$("#headerCycle").val(),$("#headerTerm").val())')
        return render_to_response('folha2.html',{'header':header.getHtml()},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def findCourses(request):
    data = request.GET
    response = ColumnsController.findCourses(data['abbreviation'], data['courseCode'], '', int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    return HttpResponse(json.dumps(response))

def getCourses(request):
    data = request.GET
    response = ColumnsController.findCourses('', '', '', int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    return HttpResponse(json.dumps(response))

def expandCourse(request):
    data = request.GET
    response = ColumnsController.expandCourse(int(data['idCourse']), int(data['idTimePeriod']))
    return HttpResponse(json.dumps(response))

def findOffers(request):
    data = request.GET
    response = ColumnsController.getOffers(data['courseCode'], int(data['idTimePeriod']))
    return HttpResponse(json.dumps(response))

def getAnswerTypes(request):
    response = QuestionController.getAnswerTypes()
    return HttpResponse(json.dumps(response))

def getQuestions(request):
    data = request.GET
    response = QuestionController.findQuestion('')
    return HttpResponse(json.dumps(response))

def storeQuestions(request):
    data = request.GET
    response = QuestionController.storeQuestion(data['idAnswerType'], data['questionWording'])
    return HttpResponse(json.dumps(response))


def findOpticalSheetByTimePeriod_Cycle_Term(request):
    data = request.GET
    response = OpticalSheetController.findOpticalSheetByTimePeriod_Cycle_Term(int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    return HttpResponse(json.dumps(response))

def findOpticalSheetById(request):
    data = request.GET
    response = OpticalSheetController.findOpticalSheetById(int(data['idOpticalSheet']))
    return HttpResponse(json.dumps(response))

def store(request):
    data = request.POST
    data = json.loads(data['json'])
    response = OpticalSheetController.storeOpticalSheet(data['idOpticalSheet'], data['surveyType'], data['idCycle'], data['term'], data['idTimePeriod'], data['fields'], data['surveys'], data['encoded'])
    return HttpResponse(json.dumps(response))

def printOpticalSheet(request):
    data = request.POST
    jsonString = data['json']
    data = json.loads(jsonString)
    opticalSheetPrinter = OpticalSheetPrinter(data['idCycle'], data['term'], data['idTimePeriod'])
    opticalSheetPrinter.printOpticalSheet(data['idOpticalSheet'], data['fields'], data['survey'], data['positions'])
    return HttpResponse('ok')

def getPrintedOpticalSheet(request):
   data = request.GET
   opticalSheetPrinter = OpticalSheetPrinter(int(data['idCycle']), int(data['term']), int(data['idTimePeriod']))
   if data['downloadType'] == 'pdf':
       return opticalSheetPrinter.getPDF()
   elif data['downloadType'] == 'tex':
       return opticalSheetPrinter.getTex()

def printQualitativeQuestionnaire(request):
    data = request.POST
    data = json.loads(data['json'])
    qqPrinter = QualitativeQuestionnairePrinter( int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    qqPrinter.printQualitativeQuestionnaire(int(data['idOpticalSheet']), int(data['numberOfAnswerLines']), int(data['qualitativeQuestionnaireType']))
    return HttpResponse('ok')

def getPrintedQualitativeQuestionnaire(request):
    data = request.GET
    qqPrinter = QualitativeQuestionnairePrinter( int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    if data['downloadType'] == 'pdf':
        return qqPrinter.getPDF()
    elif data['downloadType'] == 'tex':
        return qqPrinter.getTex()

def getEncodings(request):
    data = request.GET
    response = ColumnsController.getEncodings(data['idTimePeriod'])
    return HttpResponse(json.dumps(response))

def removeCycleFromOpticalSheet(request):
    data = request.GET
    ColumnsController.removeCycleFromOpticalSheet(data['idCycle'], data['term'], data['idOpticalSheet'])
    return HttpResponse('')

def listOldOpticalSheets(request):
    data = request.GET
    response = OpticalSheetController.getOldOpticalSheets(data['idCycle'])
    return HttpResponse(json.dumps(response))

