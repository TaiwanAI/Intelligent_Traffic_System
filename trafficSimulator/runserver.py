from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template,jsonify
from qlearningAgents import QLearningAgent
from flask import request

actionFn = lambda x: actions
learner = QLearningAgent(actionFn=actionFn)
app = Flask(__name__)

@app.route('/observeTransition', methods=['POST'])
def observeTransition():
	oldState = request.json['oldState']
	
	lastAction = request.json['lastAction']
	
	currentState = request.json['currentState']
	
	reward = request.json['reward']
	

	oldState = tuple(oldState)
	currentState = tuple(currentState)
	lastAction = tuple(lastAction)
	print("--------------",file=sys.stderr)
	print(oldState, file=sys.stderr)
	print(lastAction,file=sys.stderr)
	print(currentState,file=sys.stderr)
	print(reward,file=sys.stderr)
	print("--------------",file=sys.stderr)
	learner.observeTransition(oldState, lastAction, currentState, reward)
	res = dict(status_code=200)
	return jsonify(res)

@app.route('/getAction', methods=['POST'])
def getAction():
	currentState = request.json['currentState']
	currentState = tuple(currentState)
	lastAction = learner.getAction(currentState)
	print(lastAction,file=sys.stderr)
	res = dict(lastAction=lastAction)
	return jsonify(res)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
   app.run(port=8080)