#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS, cross_origin
#from flask.ext.cors import CORS, cross_origin
from sumario import LoadSummarizerByUser
from sumario import LoadQuestionTime
from analytics import analytics
from cut import cut
from recommender import recommender, lastRecommendation, changeBtnQuestionEasy
import os
import thread
import time
import threading
import sys, errno
from banco import newTeacher, searchTeacher
from werkzeug import secure_filename

sumario = list()
#sumarioL = list()
recomendation = list()
timeQuestions = list()
idQ = list()
status_class = False
idQu = list()
#btnTroca = list()
#btnTroca.append("0")

app = Flask('storage', static_folder='realtime')
CORS(app)
#moveBufferHttpRest_to_BufferChangeLogger = False
#Criando diretório sessions caso não exista	
if os.path.exists("sessions-Logs") == False:
	os.makedirs("sessions-Logs")

#Verifica se os arquivo com os dados do usuario existe
if os.path.exists("users.csv") == False:
	users_file = open("users.csv",'w')
	users_file.close()

app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['zip'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return render_template('ok.html') #redirect(url_for('uploaded_file',
                               # filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



#semaforo_sumarizerLog = True
active_sessions = list()
#recomendationUsers = list()
active_sessions.append("1")

mutex = 0


def searchAdaptation(user, timestamp, event, idView):

	global mutex
	global sumario
	while mutex:# getSemaforo(session):
		pass
	mutex = 1#setSemaforo(session)
	#atualiza o sumario
	sumario = LoadSummarizerByUser(user, timestamp, event, idView, sumario)
	#sumarioL = sumario
	recomendationUser = analytics(user, sumario, idView)
	print "sumario"
	print sumario
	#print ""
	#print "recomendation"
	#print recomendation
	#print "" 
	idQuestion = idView.split(":")
	feedback = []
	if recomendationUser == True:
		feedback = recommender(user, recomendation, int(idQuestion[1]), int(timestamp))
	else:
		feedback = lastRecommendation(user, recomendation, int(idQuestion[1]), int(timestamp))
	mutex = 0#releaseSemaforo	
	print "feedback recomendation\n\n"
	print feedback[0]
	print ""
	return feedback

def updateQuestionsTime(user, timestamp, idView):
	idQuestion = idView.split(":")
	idQ.append(idQuestion[1])
	if len(idQu) == 0:
		idQu.append(idQuestion[1])
	idQu[0] = idQuestion[1]
	#print ("\n\n\n" + idQu[0] + "\n\n\n")
	timeQuestion = LoadQuestionTime (user, timeQuestions, int(idQuestion[1]), int(timestamp))
	#print timeQuestions


@app.route("/login/<idSession>", methods=["POST"])
def login(idSession):

	global status_class

	if request.method == "POST":
		matricula = request.form["matricula"]

	file_users = open("users.csv",'r')
	for line in file_users:
		user = line.split(";")
		if user[1] == matricula:
			print("Seja Bem Vindo(a) aluno(a) " + user[0])
			file_users.close()
			return "Ok;"+user[0]+";"+user[2], 200
	print ("User Nao encontrado!")
	file_users.close()
	return "Error", 200

#@app.route("/")
#def index():
#	return redirect(url_for("Aula/index.html"))


@app.route("/loginTeacher/<idSession>", methods=["POST"])
def loginTeacher(idSession):

	global status_class

	if request.method == "POST":
		matricula = request.form["matricula"]
		senha = request.form["senha"]
		dados = searchTeacher(int(matricula), senha)
		if dados:
			print("Seja bem Vindo professor(a) " + dados[1])			
			#				nome             id
			#a = 
			return "Ok;"+dados[1]+";"+str(dados[0]), 200

	print ("User Nao encontrado!")
	return "Error", 200



@app.route("/teacherRegistration/<idSession>", methods=["POST"])
def teacherRegistration(idSession):
	global status_class
	if request.method == "POST":
		nameTeacher = request.form["nome"]
		emailTeacher = request.form["email"]
		idTeacher = request.form["matricula"]
		passwordTeacher = request.form["senha"]
		if newTeacher(nameTeacher, emailTeacher, idTeacher, passwordTeacher):
			return "Ok", 200
	return "Erro", 200
			
	


@app.route("/storage/<idSession>", methods=["POST"])
def receive_data(idSession):
	if request.method == "POST":
		try:
			if verify_active_session(idSession) == False:
				create_session(idSession)
			idUser = request.form["idUser"]					
			event = request.form["tipo"]		
			resource = request.form["tag"]
			timestamp = request.form["timeStamp"]
			x = request.form["x"]
			y = request.form["y"]
			#idView = request.form["id"]
			tela = request.form["tela"]
			idView = request.form["classId"]    	
			#print tela
			
			if x == "" and y == "" and resource == "":
				#Neste bloco está sendo atualizado a última linha que significa o timestamp e a tela atual passado pelo Player
				with open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv") as f:
					lines = f.readlines()
					if len(lines) > 0:
						lineOld = lines[-1] #pega ultima linha
						lineNew = idSession+";"+idUser+";"+timestamp+";"+event +";"+ tela+ ";"+idView+";"+resource+";"+x+";"+y+"\n"
						f.close()

						fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'r')
						filedata = fileaux.read()
						fileaux.close()

						newdata = filedata.replace(lineOld, lineNew)

						fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'w')
						fileaux.write(newdata)
						fileaux.close()
					else:
						newdata = idSession+";"+idUser+";"+timestamp+";"+event +";"+ tela +";"+idView+";"+resource+";"+x+";"+y+"\n"
						fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'w')
						fileaux.write(newdata)
						fileaux.close()

			else:
				with open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv") as f:
					lines = f.readlines()
					lineOld = lines[-1] #pega ultima linha
					f.close()
					#print lines

					fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'r')
					filedata = fileaux.read()
					fileaux.close()

					lineNew = idSession+";"+idUser+";"+timestamp+";"+event +";"+ tela +";"+idView+";"+resource+";"+x+";"+y+"\n"
					newdata = filedata.replace(lineOld, lineNew)
					newdata = newdata + lineOld 
					#print newdata
					fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'w')
					fileaux.write(newdata)
					fileaux.close()


			#data_received =	idSession+";"+idUser+";"+timestamp+";"+event +";"+idView+";"+resource+";"+x+";"+y+"\n"
			#fileBuffer = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv", "a")
			#fileBuffer.write(data_received)
			#fileBuffer.close()

			print idSession+";"+idUser+";"+timestamp+";"+event +";"+ tela +";"+idView+";"+resource+";"+x+";"+y
			print ""
			#print "btn Storage" + btnTroca[0]
			#Solicita recomendacao caso o aluno estiver em uma questao
			try:
				if idView != "" and (idView == "troca-Q1 btn btn-info btn-lg" or idView == "troca-Q2 btn btn-info btn-lg" or idView == "troca-Q3 btn btn-info btn-lg"):
					#btnTroca[0] = "1"
					changeBtnQuestionEasy(idUser, recomendation, int(idView[7]), int(timestamp))
					print "AQUI BTN"
				
				if idView != "" and idView[0] == "Q":
					idViewSplit = idView.split(":")
					#print idViewSplit
					updateQuestionsTime(idUser, timestamp, idView)
					feedback = searchAdaptation(idUser, timestamp, event, idView)
					#print feedback			
					if len(feedback) > 0:
						print "Recomendação(SENT): " + feedback[1]
						print "Questions (SENT): " + feedback[2]
						recommendation = [{"recommendation": feedback[1]}, {"questions":feedback[2]}]
						#print "----Teste Recommendation OOOOOI------", recommendation
						return jsonify({'recommendation': recommendation})
					else:
						print "AQUI ELSE1"
						recommendation = [{"recommendation": "ok"}, {"questions": "nada"} ]
						return jsonify({'recommendation': recommendation})
				else:
					print "AQUI ELSE2"
					recommendation = [{"recommendation": "ok"}, {"questions": "nada"}]
					return jsonify({'recommendation': recommendation})
			except:
				print "Broken"
				pass
				
		except:
			print "Broken"
			pass

@app.route("/realtime/<idSession>", methods=["GET"])
def realTimeStateStudents(idSession):
	if request.method == "GET":
		#return buildGraphTimeLine(idSession), 200
		return flotchart2(), 200

def buildGraphTimeLine(idSession):
	html = ""
	print idQ[0]
	if idQ[0] == "1":
		html = """
		<meta http-equiv="refresh" content="3">
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
  google.charts.load("current", {packages:["timeline"]});
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var container = document.getElementById('graphTimeLine');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'Question' });
    dataTable.addColumn({ type: 'string', id: 'idUser' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows([
      [ 'Q1', '1 ', new Date(0), new Date("""+str(timeQuestions[0][1][3])+""") ],
      [ 'Q2', '1', new Date(0), new Date("""+str(timeQuestions[0][2][3])+""") ],
      [ 'Q3', '1', new Date(0), new Date("""+str(timeQuestions[0][3][3])+""") ]]);

    var options = {
      colors: ['#2DB000','#F00'],
    };

    chart.draw(dataTable, options);
  }

</script>

<div id="graphTimeLine"></div>
"""

	elif idQ[0] == "2":
		html = """<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<script type="text/javascript">
  google.charts.load("current", {packages:["timeline"]});
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var container = document.getElementById('graphTimeLine');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'Question' });
    dataTable.addColumn({ type: 'string', id: 'idUser' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows([
      [ 'Q1', '1', new Date(0), new Date("""+str(timeQuestions[0][1][3])+""") ],
      [ 'Q2', '1 ', new Date(0), new Date("""+str(timeQuestions[0][2][3])+""") ],
      [ 'Q3', '1', new Date(0), new Date("""+str(timeQuestions[0][3][3])+""") ]]);

    var options = {
      colors: ['#2DB000','#F00','#2DB000'],
    };

    chart.draw(dataTable, options);
  }

</script>

<div id="graphTimeLine"></div>
"""
	elif idQ[0] == "3":
		html = """<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<script type="text/javascript">
  google.charts.load("current", {packages:["timeline"]});
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var container = document.getElementById('graphTimeLine');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'Question' });
    dataTable.addColumn({ type: 'string', id: 'idUser' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows([
      [ 'Q1', '1', new Date(0), new Date("""+str(timeQuestions[0][1][3])+""") ],
      [ 'Q2', '1', new Date(0), new Date("""+str(timeQuestions[0][2][3])+""") ],
      [ 'Q3', '1 ', new Date(0), new Date("""+str(timeQuestions[0][3][3])+""") ]]);

    var options = {
      colors: ['#F00','#F00','#2DB000'],
    };

    chart.draw(dataTable, options);
  }

</script>

<div id="graphTimeLine"></div>
"""

	return html

def flotchart ():
	print "aqui"
	html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
 
<html xmlns="http://www.w3.org/1999/xhtml">
<meta charset = "utf-8">

<head>
	<meta http-equiv="refresh" content="3">
    <title>Gráfico tempo por questão</title>

    <script src="js/flot/jquery-3.1.0.min.js" type='text/javascript'></script>  
    <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="/js/flot/excanvas.min.js"></script><![endif]-->
     
    <script type="text/javascript" src="js/flot/jquery.flot.min.js"></script>    
    <script type="text/javascript" src="js/flot/jquery.flot.symbol.js"></script>
    <script type="text/javascript" src="js/flot/jquery.flot.axislabels.js"></script>
 <!--<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="http://www.flotcharts.org/flot/jquery.flot.js"></script> -->

    <script type="text/javascript">
  
//
        //******* 2012 Average Temperature - BAR CHART
       // var data = [{color: "red", data: [[1, 11]]},
         //           {color: "blue", data: [[2, 15]]},
           //        {color: "blue", data: [[3, 25]]}
             //      ];
       var data = [[0,11],[1,15],[2,25]];
       // var color = ["red", "blue", "blue"]            
  
var color01 = '#00cde2';
var color02 = '#ffb700';
var color03 = '#7ac70c';"""

	if idQ[0] == "1":
		html = html + """
  var data = [
            {data: [[0,""" + str(timeQuestions[0][1][2]) + """]], color: color02},
            {data: [[1,""" + str(timeQuestions[0][2][2]) + """]], color: color02},
            {data: [[2,""" + str(timeQuestions[0][3][2]) + """]], color: color02},  
            ]; """

	if idQ[0] == "2":
		html = html + """
  var data = [
            {data: [[0,""" + str(timeQuestions[0][1][2]) + """]], color: color02},
            {data: [[1,""" + str(timeQuestions[0][2][2]) + """]], color: color02},
            {data: [[2,""" + str(timeQuestions[0][3][2]) + """]], color: color02},  
            ]; """

	if idQ[0] == "3":
		html = html + """
  var data = [
            {data: [[0,""" + str(timeQuestions[0][1][2]) + """]], color: color02},
            {data: [[1,""" + str(timeQuestions[0][2][2]) + """]], color: color02},
            {data: [[2,""" + str(timeQuestions[0][3][2]) + """]], color: color02},  
            ]; """
	html = html + """
    //  var data = [[0,11],[1,15],[2,25]];

        //var dataset = [{ label: "Tempo por questão em segundos", data: data, color: "red" }];
        var ticks = [[0, "Q1"], [1, "Q2"], [2, "Q3"]];
 
        var options = {
            series: {
               // stack: 1,
                bars: {
                    show: true
                }
            },
            bars: {
                align: "center",
                barWidth: 0.5,
                //fill:1
            },
            xaxis: {
                axisLabel: "Questões",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 10,
                ticks: ticks
            },
            yaxis: {
                axisLabel: "Tempo por questão em segundos",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 3,
                tickFormatter: function (v, axis) {
                    return v + " S";
                }
            },
            legend: {
                noColumns: 0,
                labelBoxBorderColor: "#000000",
                position: "nw"
            },
            grid: {
                hoverable: true,
                borderWidth: 2,
                backgroundColor: { colors: ["#ffffff", "#EDF5FF"] }
            }
        };
 
        $(document).ready(function () {
            $.plot($("#flot-placeholder"), data, options);
            $("#flot-placeholder").UseTooltip();
        });
 
        function gd(year, month, day) {
            return new Date(year, month, day).getTime();
        }
 
        var previousPoint = null, previousLabel = null;
 
        $.fn.UseTooltip = function () {
            $(this).bind("plothover", function (event, pos, item) {
                if (item) {
                    if ((previousLabel != item.series.label) || (previousPoint != item.dataIndex)) {
                        previousPoint = item.dataIndex;
                        previousLabel = item.series.label;
                        $("#tooltip").remove();
 
                        var x = item.datapoint[0];
                        var y = item.datapoint[1];
 
                        var color = item.series.color;
 
                        //console.log(item.series.xaxis.ticks[x].label);                
 
                        showTooltip(item.pageX,
                        item.pageY,
                        color,
                        "<strong>"+"Tempo gasto por segundo</strong><br>" + item.series.xaxis.ticks[x].label + " : <strong>" + y + "</strong> Segundos");
                    }
                } else {
                    $("#tooltip").remove();
                    previousPoint = null;
                }
            });
        };
 
        function showTooltip(x, y, color, contents) {
            $('<div id="tooltip">' + contents + '</div>').css({
                position: 'absolute',
                display: 'none',
                top: y - 40,
                left: x - 120,
                border: '2px solid ' + color,
                padding: '3px',
                'font-size': '9px',
                'border-radius': '5px',
                'background-color': '#fff',
                'font-family': 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
                opacity: 0.9
            }).appendTo("body").fadeIn(200);
        }
    </script>
</head>
<body>
    <div style="width:600px;height:450px;text-align:center;margin:10px">        
        <div id="flot-placeholder" style="width:100%;height:100%;"></div>        
    </div>

    <h1>Questao atual: """+str(idQ[0]) +"""</h1>
</body>
</html>
"""
	print ("IDQ" + str(idQ))
	return html

def flotchart2 ():
	print "aqui"
	html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
 
<html xmlns="http://www.w3.org/1999/xhtml">
<meta charset = "utf-8">

<head>
	<meta http-equiv="refresh" content="3">
    <title>Gráfico tempo por questão</title>

    <script src="js/flot/jquery-3.1.0.min.js" type='text/javascript'></script>  
    <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="/js/flot/excanvas.min.js"></script><![endif]-->
     
    <script type="text/javascript" src="js/flot/jquery.flot.min.js"></script>    
    <script type="text/javascript" src="js/flot/jquery.flot.symbol.js"></script>
    <script type="text/javascript" src="js/flot/jquery.flot.axislabels.js"></script>
 <!--<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="http://www.flotcharts.org/flot/jquery.flot.js"></script> -->

    <script type="text/javascript">
  
//
        //******* 2012 Average Temperature - BAR CHART
       // var data = [{color: "red", data: [[1, 11]]},
         //           {color: "blue", data: [[2, 15]]},
           //        {color: "blue", data: [[3, 25]]}
             //      ];
       var data = [[0,11],[1,15],[2,25]];
       // var color = ["red", "blue", "blue"]            
  
var color01 = '#00cde2';
var color02 = '#ffb700';
var color03 = '#7ac70c';"""

	if idQu[0] == "1":
		html = html + """
  var data = [
            {data: [[0,""" + str(timeQuestions[0][1][2]) + """]], color: color03},
            {data: [[1,""" + str(timeQuestions[0][2][2]) + """]], color: color02},
            {data: [[2,""" + str(timeQuestions[0][3][2]) + """]], color: color02},  
            ]; """

	if idQu[0] == "2":
		html = html + """
  var data = [
            {data: [[0,""" + str(timeQuestions[0][1][2]) + """]], color: color02},
            {data: [[1,""" + str(timeQuestions[0][2][2]) + """]], color: color03},
            {data: [[2,""" + str(timeQuestions[0][3][2]) + """]], color: color02},  
            ]; """

	if idQu[0] == "3":
		html = html + """
  var data = [
            {data: [[0,""" + str(timeQuestions[0][1][2]) + """]], color: color02},
            {data: [[1,""" + str(timeQuestions[0][2][2]) + """]], color: color02},
            {data: [[2,""" + str(timeQuestions[0][3][2]) + """]], color: color03},  
            ]; """
	html = html + """
    //  var data = [[0,11],[1,15],[2,25]];

        //var dataset = [{ label: "Tempo por questão em segundos", data: data, color: "red" }];
        var ticks = [[0, "Q1"], [1, "Q2"], [2, "Q3"]];
 
        var options = {
            series: {
               // stack: 1,
                bars: {
                    show: true
                }
            },
            bars: {
                align: "center",
                barWidth: 0.5,
                //fill:1
            },
            xaxis: {
                axisLabel: "Questões",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 10,
                ticks: ticks
            },
            yaxis: {
                axisLabel: "Tempo por questão em segundos",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 3,
                tickFormatter: function (v, axis) {
                    return v + " S";
                }
            },
            legend: {
                noColumns: 0,
                labelBoxBorderColor: "#000000",
                position: "nw"
            },
            grid: {
                hoverable: true,
                borderWidth: 2,
                backgroundColor: { colors: ["#ffffff", "#EDF5FF"] }
            }
        };
 
        $(document).ready(function () {
            $.plot($("#flot-placeholder"), data, options);
            $("#flot-placeholder").UseTooltip();
        });
 
        function gd(year, month, day) {
            return new Date(year, month, day).getTime();
        }
 
        var previousPoint = null, previousLabel = null;
 
        $.fn.UseTooltip = function () {
            $(this).bind("plothover", function (event, pos, item) {
                if (item) {
                    if ((previousLabel != item.series.label) || (previousPoint != item.dataIndex)) {
                        previousPoint = item.dataIndex;
                        previousLabel = item.series.label;
                        $("#tooltip").remove();
 
                        var x = item.datapoint[0];
                        var y = item.datapoint[1];
 
                        var color = item.series.color;
 
                        //console.log(item.series.xaxis.ticks[x].label);                
 
                        showTooltip(item.pageX,
                        item.pageY,
                        color,
                        "<strong>"+"Tempo gasto por segundo</strong><br>" + item.series.xaxis.ticks[x].label + " : <strong>" + y + "</strong> Segundos");
                    }
                } else {
                    $("#tooltip").remove();
                    previousPoint = null;
                }
            });
        };
 
        function showTooltip(x, y, color, contents) {
            $('<div id="tooltip">' + contents + '</div>').css({
                position: 'absolute',
                display: 'none',
                top: y - 40,
                left: x - 120,
                border: '2px solid ' + color,
                padding: '3px',
                'font-size': '9px',
                'border-radius': '5px',
                'background-color': '#fff',
                'font-family': 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
                opacity: 0.9
            }).appendTo("body").fadeIn(200);
        }
    </script>
</head>
<body>
    <div style="width:600px;height:450px;text-align:center;margin:10px">        
        <div id="flot-placeholder" style="width:100%;height:100%;"></div>        
    </div>

    <h1>Questao atual: """+str(idQu[0]) +"""</h1>
</body>
</html>
"""
	print ("IDQ" + str(idQu[0]))
	return html


#@app.route("/analytics/<idSession>", methods=["GET"])
#def receiveAnalytics(idSession):
#	if request.method == "GET":
#		idUser = request.args.get("idUser")
#		timeStamp = request.args.get("timestamp")
#		#print "idUser" + idUser				
#		if moduleSummarizer(idUser, timeStamp, idSession) == True:
#			return "True", 200
#		else:
#			return "False", 200

#Cria diretório que representa a sessão
def create_session(idSession):
	if os.path.exists("sessions-bufferHTTPRest/"+idSession) == False:
		os.makedirs("sessions-bufferHTTPRest/"+idSession)
		active_sessions.append(str(idSession))
		print "Created the directoy:" +idSession

#Verifica em memória se a sessão está ativa
def verify_active_session(idSession):
	#print idSession
	#print active_sessions
	for session in active_sessions:
		if session == idSession:
			#print "The session is active"
			return True
	#print "The session isn't active"
	return False

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
	#@crossdomain(origin='*')
