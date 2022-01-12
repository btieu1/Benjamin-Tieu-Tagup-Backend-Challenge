from http.server import HTTPServer, SimpleHTTPRequestHandler,BaseHTTPRequestHandler
from flask import Flask, url_for, render_template, request
import pandas as pd
import json
import requests


if __name__ == "__main__":

    with open('samples/post_data_ex1.json') as d1, open('samples/post_data_ex2.json') as d2, open('samples/post_data_ex3.json') as d3:
        data1 = json.load(d1)
        data2 = json.load(d2)
        data3 = json.load(d3)
        
        # testing the post /data 
        r = requests.post('http://localhost:8080/data', json=data1)
        #r = requests.post('http://localhost:8080/data', json=data2)
        #r = requests.post('http://localhost:8080/data', json=data3)
        
    # testing the get /statistics/
    r = requests.get('http://localhost:8080/statistics/sensor0')
    #r = requests.get('http://localhost:8080/statistics/sensor1')
    
    # testing the delete /statistics/
    #r = requests.delete('http://localhost:8080/statistics/sensor0')
    #r = requests.delete('http://localhost:8080/statistics/sensor1')
    
    # testing get /healthz
    #r = requests.get('http://localhost:8080/healthz')