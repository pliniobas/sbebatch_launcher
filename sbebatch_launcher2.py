# -*- coding: latin-1 -*-
"""
Created on Fri Apr 16 13:00:25 2021

@author: plinio.silva
@feat: Papai Saulo Meirelles 
"""
#%%
import os
from os.path import split,join
import re
from subprocess import run,Popen
import sys
import time
from tkinter import *
import json

# import tkinter.__main__
from tkinter import ttk
from glob import glob


    # /cString Use String as instrument configuration (.con or .xmlcon) file. String must include full path and file name.
# /iString Use String as input file name. String must include full path and file name.
# /oString Use String as output directory (not including file name).
# /fString Use String as output file name (not including directory).
# /pString Use String as Program Setup (.psa) file. String must include full path and file name.

curdir = r"C:\Users\plinio silva\Desktop\Pernada_01_2021_03_30ç"

# conpsa = r"D:\OneDrive\Projetos Primarios\Pythonaria\SBE\arquivos psa de conversao do SBE-DataProcessing\acustica_19plus.psa"
# tipo = "SBE37"

conpsa = r"D:\OneDrive\Projetos Primarios\Pythonaria\SBE\arquivos psa de conversao do SBE-DataProcessing\acustica_19plus.psa"
xmlcon = r"D:\OneDrive\Projetos Primarios\Pythonaria\SBE\CTD 19Plus 7424 xmlcon\SBE19plusV2_SN7424_20210331.xmlcon"
tipo = "SBE19"

plotpsa = r"D:\OneDrive\Projetos Primarios\Pythonaria\SBE\arquivos psa de conversao do SBE-DataProcessing\acustica_SeaPlot.psa"

outputfolder = r"C:\Users\plinio silva\Desktop\Pernada_01_2021_03_30ç\Output"
sufix = "-teste"

def sbebatch_lookup(curdir,conpsa,tipo,xmlcon='',plotpsa='',outputfolder='', sufix = ''):
    if tipo == "SBE19" and xmlcon == '':
        print("arquivo xmlcon nao especificado para CTD 19Plus")
        sys.exit(1)
#%%
   
    dic = {}
    print("curdir",curdir)
    for file in glob(curdir + "/**", recursive = True):
                       
        if tipo == "SBE37":
            fil = "SBE37.+(?=.hex)"
        if tipo == "SBE19":
            fil = "SBE19.+(?=.hex)"
        
        dfname = re.findall(fil,file)
        if dfname:
            print(file)
            fullpath = file
            
            if tipo == "SBE37":
                temp = re.findall("SBE[0-9A-Za-z\-]*_[0-9]{3}([0-9]*)",file)[0]
                temp = tipo + temp #nome da chave do dictionary
            elif tipo == "SBE19":
                temp = re.findall("SBE[0-9A-Za-z\-]*_[0-9]{3}([0-9]*.*(?=.hex))",file)[0]
                temp = "SBE19Plus" + temp
            else:
                pass
            
            if temp in dic:
                temp = temp + "-" + str(time.time()).split('.')[0] #muda um pouco a chave caso ja exista
            
            if tipo =="SBE37":
                c = fullpath.replace('hex','xmlcon')
            else:
                c = xmlcon
            
            i = fullpath
            if outputfolder:
                o = outputfolder
            else:
                o = split(fullpath)[0]
            if sufix:
                f = split(fullpath)[1].replace('.hex','%s.cnv'%sufix)
            else:
                f = split(fullpath)[1].replace('hex','cnv')
            p = conpsa
            plotp = plotpsa
            ploti = fullpath.replace('hex','cnv')
            dic[temp] = dict(c = c, i = i, o = o, f = f, p = p, plotp = plotp, ploti = ploti)
        else:
            pass
        pass
    
    #%%
    return dic
    pass

def sbebatch_laucher(dic,plotpsa=""):
    for aux in dic:
        ctd = dic[aux]

        string = 'Datcnv /c"{c}" /i"{i}" /o"{o}" /f"{f}" /p"{p}"'.format(c=ctd['c'],i=ctd['i'],o=ctd['o'],f=ctd['f'],p=ctd['p'])
        string = string.replace("\\","/")
        try:
            f = open("%s_batch.txt"%aux,'wb')
        except Exception as e:
            print(e)
            aux = aux + '_' + str(time.time())[-5:]
            f = open("%s_batch.txt"%aux,'wb')
        f.write(string.encode("latin-1"))
        f.close()
        run(['sbebatch',"%s_batch.txt"%aux])
                
        if plotpsa != "": 
            string = 'seaplot /c"{c}" /i"{ploti}" /o"{o}" /f"{f}" /p"{plotp}"'.format(c=ctd['c'],ploti=ctd['ploti'],o=ctd['o'],f=ctd['f'],plotp=ctd['plotp'])
            string = string.replace("\\","/")
            f = open("%s_plot_batch.txt"%aux,'wb')
            f.write(string.encode("latin-1"))
            f.close()
            run(['sbebatch',"%s_plot_batch.txt"%aux])
        
if "__main__" in __name__:
    
    #para teste
    # dic = sbebatch_lookup(curdir, conpsa, tipo, xmlcon = xmlcon, plotpsa = plotpsa, outputfolder= outputfolder, sufix = sufix)
    # sbebatch_laucher(dic, plotpsa=plotpsa)
    # sys.exit()
    
    root = Tk()
    # frame = ttk.Frame(root)
    # frame.pack()    
    # frame.config(height = 100, width = 200)
    
    label = ttk.Label(root, text = "Choose CTD type").pack()
    tipot = StringVar()
    
    sbe37 = ttk.Radiobutton(root, text = 'SBE37', variable = tipot, value = 'SBE37')
    sbe37.pack()
    
    sbe19 = ttk.Radiobutton(root, text = 'SBE19', variable = tipot, value = 'SBE19')
    sbe19.pack()
    
    ttk.Label(root, text = "Choose folderpath to scan").pack()    
    curdirt = ttk.Entry(root, width = 200)
    # curdir.insert(0,"Choose folder path to scan")
    curdirt.pack()
    
    ttk.Label(root, text = "Choose convert config .psa filepath ").pack()    
    conpsat = ttk.Entry(root, width = 200)
    conpsat.pack()
     
    ttk.Label(root, text = "If SBE19 - xmlcon filepath").pack()    
    xmlcont = ttk.Entry(root, width = 200)
    xmlcont.pack()
   
    ttk.Label(root, text = "If want to plot - seaplot config .psa filepath").pack()    
    plotpsat = ttk.Entry(root, width = 200)
    plotpsat.pack()
 
    ttk.Label(root, text = "Choose a output folder or leave blank for output in same folder").pack()    
    outputfoldert = ttk.Entry(root, width = 200)
    outputfoldert.pack()
    
    ttk.Label(root, text = "Choose sufix to append to filename or leave blank").pack()    
    sufixt = ttk.Entry(root, width = 200)
    sufixt.pack()
       
    start = ttk.Button(root, text = "Start batch!")
    start.pack()

    save = ttk.Button(root, text = "Save folder and filepaths for later")
    save.pack()
    
    try:
        with open('sbebatch_laucher_save.txt','rb') as f:
            temp = f.read()
            f.close()
        
        dic = json.loads(temp)
        
        #pega os dados salvos e insere nos campos.
        curdirt.insert(0,dic['curdir']) 
        conpsat.insert(0,dic['conpsa'])
        xmlcont.insert(0,dic['xmlcon'])
        plotpsat.insert(0,dic['plotpsa'])
        outputfoldert.insert(0,dic['outputfolder'])
        sufixt.insert(0,dic['sufix'])
                
    except Exception as e:
        print(e)
        print('nao foi possivel recuperar a configuracao anterior.')


    def start_batch():
        print("Start batch!")
        tipo = tipot.get()
        if tipo == "":
            messagebox.showerror("Alert","You must choose a CTD type!")
            return
        
        curdir = curdirt.get()
        if curdir == "":
            messagebox.showerror("Alert","You must choose a folder path!")
            
        conpsa = conpsat.get()
        if conpsa == "":
            messagebox.showerror("Alert","You must choose a .psa file")
        
        xmlcon = xmlcont.get()
        plotpsa = plotpsat.get()
        outputfolder = outputfoldert.get()
        sufix = sufixt.get()
        
        dic = sbebatch_lookup(curdir,conpsa,tipo, xmlcon=xmlcon, plotpsa=plotpsa, outputfolder=outputfolder, sufix=sufix)
        if plotpsa:
            print("plotpsa enable")
            sbebatch_laucher(dic,plotpsa = plotpsa)
        else:
            sbebatch_laucher(dic)
            print('plotpsa disable')
            
   
    def save4late():
        print("save4late")
        tipo = tipot.get()
        curdir = curdirt.get()
        conpsa = conpsat.get()
        xmlcon = xmlcont.get()
        plotpsa = plotpsat.get()
        outputfolder = outputfoldert.get()
        sufix = sufixt.get()
        
        print('curdir',curdir)
        temp = dict(tipo = tipo,
                    curdir = curdir,
                    conpsa = conpsa,
                    xmlcon = xmlcon,
                    plotpsa = plotpsa,
                    outputfolder = outputfolder,
                    sufix = sufix
                    )
        
        temp2 = json.dumps(temp).encode('latin-1')
        
        with open('sbebatch_laucher_save.txt','wb') as f:
            f.write(temp2)
            f.close()
        
           
    start.config(command = start_batch)
    save.config(command = save4late)
        
    root.mainloop()
    
# %%


