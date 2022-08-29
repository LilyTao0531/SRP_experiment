#!/usr/bin/env python
# coding: utf-8

import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt


## Plot Methods

CSS_COLORS = ["red", "blue", "limegreen", "darkorange", "gold", "magenta", "cyan", "turquoise"]
DASH_STYLE = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"]


def _plotData(data, title, writingPath):
    """
    Subroutine to plot data of some methods/instances over time or iterations.
    
    - data is a dictionary:
        data["id"][key]: list of data to plot over each time unit/iteration of x_axis for a given instance/method key.
        data["color"][i]: the color of the ith set of data (same order as the keys in data["id"])
        data["dash"][i]: the dash style of the ith set of data
        data["x_axis"]["type"]: "time" or "iteration"
        data["x_axis"]["steps"]: array of time unit or iterations used in the XP
        data["y_axis"]: "Relative Error", "Mean Relative Error" or "Objective"
    
    - title is the title of the plot.

    - writingPath is the path where the plot will be saved.
    
    """
    
    # Create traces
    fig = go.Figure()
    
    # We add a curve for each data
    for p, key in enumerate(data["id"].keys()):
        # We remove the data when no feasible solution is found or if a bug occured (i.e. data[key][t] < 0)
        x_key = [data["x_axis"]["steps"][t] for t in range(len(data["x_axis"]["steps"])) if data["id"][key][t] >= 0]
        y_key = [data["id"][key][t] for t in range(len(data["x_axis"]["steps"])) if data["id"][key][t] >= 0]
            
        fig.add_trace(go.Scatter(x=x_key, y=y_key,
                mode='lines',
                name=key,
                line = dict(color = data["color"][p], dash = data["dash"][p])))
    
    # Setup layout and axes
    fig.update_yaxes(
        title_text = data["y_axis"],
        gridcolor = "lightgrey",
        linecolor='black',
        zeroline = False,
        title_standoff = 5
        )

    fig.update_xaxes(
        title_text = data["x_axis"]["type"],
        gridcolor = "lightgrey",
        linecolor='black',
        title_standoff = 0)

    fig.update_layout(
        title = title,
        autosize=False,
        width=500,
        height=300,
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=30,
        pad=4),
        plot_bgcolor='white'
    )
    
    # Saving plot in writingPath
    fig.write_image(writingPath)
    
    # Show plot
    fig.show()
    

def _plotBarData(barData, title, writingPath):
    
    """
    Subroutine to plot data in bar over time or iterations, used for plotting nb of instances solved at each step.
    
    - barData is a dictionary:
        barData["id"][key]: list of data to plot over each time unit/iteration of x_axis for a given instance/method key.
        barData["maxRange"] : give max range of the bar (nb. instances for example)
        barData["color"][i]: the color of the ith set of data (same order as the keys in data).
        barData["x_axis"]["type"]: "time" or "iteration".
        barData["x_axis"]["steps"]: array of time unit or iterations used in the XP.
        barData["y_axis"]: "Nb. Solved" or other.
    
    - title is the title of the plot.

    - writingPath is the path where the plot will be saved.
    
    """
    
    # Create x_axis of the plot
    if barData["x_axis"]["type"] == "time":
        bar_xaxis=["t = "+str(barData["x_axis"]["steps"][k])+"s" for k in range(len(barData["x_axis"]["steps"]))]
    else:
        bar_xaxis=["iter "+str(barData["x_axis"]["steps"][k]) for k in range(len(barData["x_axis"]["steps"]))]
    

    # Create figure with all bars corresponding to data
    fig = go.Figure(data=[
        go.Bar(name=key, marker={"color":barData["color"][p]}, x=bar_xaxis, y=barData["id"][key]) for p, key in enumerate(barData["id"].keys())])

    # Group bar mode
    fig.update_layout(barmode='group')

    # Set up axes and layout
    fig.update_xaxes(
        title_text = barData["x_axis"]["type"],
        linecolor='black',
        title_standoff = 5
        )
    
    fig.update_yaxes(
        title_text = barData["y_axis"],
        title_standoff = 5,
        gridcolor = "lightgrey",
        linecolor='black',
        range = [0,barData["maxRange"]])

    fig.update_layout(
        title = title,
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=30,
            pad=4
        ),
        plot_bgcolor='white'
    )
    
    # Save figure and show it
    fig.write_image(writingPath)
    fig.show()
    


def plotRE(res, title, writingPath):
    
    """
    Plot Relative Error of some methods/instances over time or iterations.
    
    - res is a dictionary:
        res["instances_id"]: list of instances id
        res["methods"][key] : Objective values obtained for each instance and each step for method key
        res["x_axis"]["type"]: "time" or "iteration"
        res["x_axis"]["steps"]: array of time unit or iterations used in the XP
        res["BKS"][i]: Best known solution for instance i (same order as res["instances_id"]) 
                including the objective values in res["methods"]
    
    - title is the title of the figure.

    - writingPath is the path of the directory where the plot will be saved.
    
    """
    
    N = len(res["instance_id"])
    
    data = dict()
    data["id"] = {} # where are stored data for each method
    color = [] # one color per instance
    dash = [] # one dash style per method
    
    for p, key in enumerate(res["methods"].keys()):
        for i in range(N):
            
            # Compute Relative Error for each method/instance and iteration/time unit
            data_name = key+"_"+res["instance_id"][i] # name of the data based on method used and instance solved
            data_key_i = []
            for t in range(len(res["x_axis"]["steps"])):
                v = res["methods"][key][i][t]
                print("i: ", i, "t: ", t)
                if v != "bug" and v != "TO":
                    data_key_i.append((v-res["BKS"][i])/res["BKS"][i]) # Compute RE
                else:
                    data_key_i.append(-1) # If instance was not solved or if a bug occured --> -1
            
            # Add data and corresponding color and dash style
            data["id"][data_name] = data_key_i
            color.append(CSS_COLORS[i])
            dash.append(DASH_STYLE[p])
            
    data["color"] = color
    data["dash"] = dash
    data["x_axis"] = {
        "steps" : res["x_axis"]["steps"],
        "type" : res["x_axis"]["type"]
    }
    data["y_axis"] = "Relative Error"
    
    _plotData(data, title, writingPath+title+".png")
    


def plotMRE(res, title, writingPath):
    
    """
    Plot Mean Relative Error and nb. solved instances of some methods over time or iterations.
    
    - res is a dictionary:
        res["instances_id"]: list of instances id
        res["methods"][key] : Objective values obtained for each instance and each step for method key
        res["x_axis"]["type"]: "time" or "iteration"
        res["x_axis"]["steps"]: array of time unit or iterations used in the XP
        res["BKS"][i]: Best known solution for instance i (same order as res["instances_id"]) 
                including the objective values in res["methods"]
    
    - title is the title of the XP. 
        MRE_title.png will be the name of the MRE plot
        NbSolved_title.png will be the name of the bar charts showing nb of solved instances
 
    - writingPath is the path of the directory where the plot will be saved.
    """
    
    N = len(res["instance_id"])
        
    data = dict() # for plotting MRE
    data["id"] = {}
    barData = dict() # for plotting nb. instances solved
    barData["id"] = {}
    
    color = [] # one color per method
    dash = [] # same dash style for each method
    

    # Compute Mean Relative Error for each method and iteration/time unit over all instances
    for p, key in enumerate(res["methods"].keys()):
        
        
        # First compute RE for each instance and each step...
        RE_key =[]
        nb_solved_at_step = np.full(len(res["x_axis"]["steps"]), N) # nb instances solved at each step
        for i in range(N):
            # print(key + "_" + i + ":" + res["methods"][key][i])
            RE_key.append([])
            RE_key[i] = []
            for s in range(len(res["x_axis"]["steps"])):
                v = res["methods"][key][i][s]
                if v != "bug" and v != "TO":
                    RE_key[i].append((v-res["BKS"][i])/res["BKS"][i]) # Compute RE
                else:
                    RE_key[i].append(-1) # If instance was not solved or if a bug occured --> -1
                    nb_solved_at_step[s]-=1
        
        # ... then compute MRE over all instances for each step
        MRE_key = np.full(len(res["x_axis"]["steps"]), -1.0, np.float16)
        for s in range(len(res["x_axis"]["steps"])):
            # If no instance were solved for a given step, then MRE is -1 and will not be plot
            if nb_solved_at_step[s]>0:
                MRE_key[s] = sum([RE_key[i][s] for i in range(N) if RE_key[i][s]>=0])/nb_solved_at_step[s]
   
        # Add data and corresponding color and dash style
        data["id"][key] = MRE_key
        barData["id"][key] = nb_solved_at_step
        color.append(CSS_COLORS[p])
        dash.append(DASH_STYLE[0])
    
    # Complete data for plotting MRE
    data["color"] = color
    data["dash"] = dash
    data["x_axis"] = {
        "steps" : res["x_axis"]["steps"],
        "type" : res["x_axis"]["type"]
    }
    data["y_axis"] = "Mean Relative Error"
    
    # print(data)
    
    # Complete barData for plotting nb instances solved
    barData["color"] = color
    barData["dash"] = dash
    barData["maxRange"] = N
    barData["x_axis"] = {
        "steps" : res["x_axis"]["steps"],
        "type" : res["x_axis"]["type"]
    }
    barData["y_axis"] = "Nb. Solved"
    
    _plotData(data, "Mean Relative Error "+title, writingPath+"MRE_"+title+".png")
    _plotData(barData, "NbSolved_"+title, writingPath+"NbSolved_"+title+".png")
    

def plotBisector(obj_1, obj_2, method_1, method_2):
    
    """
    Create a cloud of points with coordinates (obj_1[i], obj_2[i]) for each instance i.
    And compare it to the bisector y=x.
    
    - obj_i: objective value obtained with method i
    - method_i: String for method i name
    
    """

    N = len(obj_1)
    
    # Set bounds for plotting
    a = int(min(min(obj_1), min(obj_2))-10)
    b = int(max(max(obj_1), max(obj_2))+10)
    plt.figure(figsize=(10,10))
    plt.rc('axes', labelsize=20)

    # Create bisector y=x
    line = [k for k in range(a,b)]
    plt.plot(line, line, color ='tab:red') 
    plt.scatter(obj_1, obj_2)
    
    # Set axes
    plt.xlabel(method_1) 
    plt.ylabel(method_2) 
    
    #Show figure
    plt.show()
    
    
res = {
    "instance_id": ["instances_1", "instances_2", "instances_3", "instances_4"],
    "methods": {
        "random" : [[800, 500, 300 , 245], [950, 750, 650, 635], ["TO", 500, 450, 410], [2544, "bug", 800, 756]],
        "incredible" : [[400, 350, 300, 210], [810, "bug", 610, 599], [450, 425, 390, 388], [933, 855, 800, 754]]
    },
    "x_axis":{
        "type": "time",
        "steps": [0.01,0.02,0.03,0.04]
    },
    "BKS" : [210, 532, 388, 754]
}


# plotRE(res, "Relative Error", "graphs")