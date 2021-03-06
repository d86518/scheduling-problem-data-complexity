# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 20:30:31 2017

@author: USER
"""
import sys
import random
import numpy as np
import csv
import time
from gurobipy import *
import matplotlib.pyplot as plt
cons = []
p = []
for x in range(30):
    cons.append(0)
f=open('pdata.txt','r')
file = f.read()
file =file[:].split(' ')
f.close()

file = list(file)
m = file.pop()
n = file.pop()
n = int(n) #j
o = n
m = int(m) #k
file = np.asarray(file)
file = file.reshape(m,n)
p = file.tolist()

try:
  M=Model("mip1")
  #m為job n為工作 有4job 5work [, , , ]X5
  
  x=M.addVars(n,o,vtype=GRB.BINARY,name="x")
  c=M.addVars(m,o,vtype=GRB.INTEGER,name="c")
##  可以設lb ub (int用)
#  i=M.addVars(n,vtype=GRB.INTEGER,name="i")
#  w=M.addVars(n,vtype=GRB.INTEGER,name="w")
    
  M.update()
  Line = LinExpr()
#      Line.addTerms(1,c[2,i]) #前面係數後面變數 c0 c1 c2的係數都是1
  Line.addTerms(1,c[(m-1),(o-1)])
      
      
  M.setObjective(Line,GRB.MINIMIZE)
  
  for k in range(o):
      cons[0] = LinExpr()
      for j in range(n):
          cons[0].addTerms(1,x[j,k])
      M.addConstr(cons[0]==1)
  
  for j in range(n):
      cons[1] = LinExpr()
      for k in range(o):
          cons[1].addTerms(1,x[j,k])
      M.addConstr(cons[1]==1)
      
  cons[2] = LinExpr()
  for j in range(n):
      cons[2].addTerms(p[0][j],x[j,0])
  M.addConstr(c[0,0]==cons[2])
  
  for k in range(o-1):
      cons[3] = LinExpr()
      for j in range(n):
          cons[3].addTerms(p[0][j],x[j,k+1])
      M.addConstr(c[0,k+1]==cons[3]+c[0,k])
  
  i=k=j=0
  for i in range(m-1):
      for k in range(o):
          cons[2*i+4] = LinExpr()   
          for j in range(n):
              cons[2*i+4].addTerms(p[i+1][j],x[j,k])
          M.addConstr(c[i+1,k]>=cons[2*i+4]+c[i,k])          
 
  i=k=j=0
  for i in range(m-1):
      for k in range(o-1):
          cons[2*i+5] = LinExpr()
          for j in range(n):
                cons[2*i+5].addTerms(p[i+1][j],x[j,k+1])
          M.addConstr(c[i+1,k+1]>=cons[2*i+5]+c[i+1,k])
 
  starttime = time.time()     
  M.optimize()
  endtime = time.time()     
  
  for v in M.getVars():
      print('%s %g'%(v.varName,v.x))
      
  print('Obj:%g'%M.objVal)
  
except GurobiError:
    print('Encountered a Gurobi error')
    
except AttributeError:
    print('Encountered an attribute error')
    
    print('Total:',endtime-starttime)    

#for i in range(n):
#   for j in range(n):
#       if(x[i,j].x == 1):
#           print("(",i,",",j,")")
#tosc = []

    
p2=[[i*0 for i in range(n)] for i in range(m)]
for i in range(n): 
  for j in range(n):  
     if((x[j,i].x)!=0):
        for k in range(m):
            p2[k][i] = int(p[k][j])
                
#jobnum = [5,9,13,17,21,25,29,33,37,41,45]
#
#joboftpd = [ 0.06407332420349121
#            ,0.14515948295593262
#            ,0.22525453567504883
#            ,0.4364891052246094
#            ,1.393571138381958
#            ,1.951875925064087
#            ,2.4807217121124268
#            ,3.360306978225708
#            ,8.14754605293274
#            ,13.248310804367065
#            ,18.515535354614258
#            ]
#
#jobofrd = [0.0590670108795166
#           ,0.0670766830444336
#           ,0.06908154487609863
#           ,0.07808470726013184
#           ,0.13013839721679688
#           ,0.18932833671569824
#           ,0.19622206687927246
#           ,0.2462766170501709
#           ,0.3123505115509033
#           ,0.37631306648254395
#           ,0.39545583724975586
#           ]
#plt.xlabel("job")
#plt.ylabel("time")
#plt.plot(jobnum,joboftpd)
#plt.plot(jobnum,jobofrd)