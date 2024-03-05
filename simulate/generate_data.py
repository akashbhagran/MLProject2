import numpy as np
import pandas as pd
from fastapi import FastAPI
import json

app = FastAPI()
num = 250


@app.get("/")
async def generate():

    while(1):

        apples = {'Mass': [np.random.normal(165,10) for i in range(0,num)], \
        'Width':[np.random.normal(7.6,0.8) for i in range(0,num)], \
        'height':[np.random.normal(7.2,0.6) for i in range(0,num)], \
        'color':[np.random.uniform(0.55,0.95) for i in range(0,num)],
        'fruit':['apple' for i in range(0,num)]}

        mandarin = {'Mass': [np.random.normal(81,5) for i in range(0,num)], \
        'Width':[np.random.uniform(5.8,6.2) for i in range(0,num)], \
        'height':[np.random.normal(4.3,0.5) for i in range(0,num)], \
        'color':[np.random.uniform(0.77,0.81) for i in range(0,num)],
        'fruit':['mandarin' for i in range(0,num)]}

        orange = {'Mass': [np.random.normal(150,50) for i in range(0,num)], \
        'Width':[np.random.normal(7.2,0.8) for i in range(0,num)], \
        'height':[np.random.normal(7.0,10) for i in range(0,num)], \
        'color':[np.random.uniform(0.72,0.82) for i in range(0,num)],
        'fruit':['orange' for i in range(0,num)]}

        lemon = {'Mass': [np.random.uniform(120,200) for i in range(0,num)], \
        'Width':[np.random.normal(6.6,0.6) for i in range(0,num)], \
        'height':[np.random.uniform(7.5,10.5) for i in range(0,num)], \
        'color':[np.random.normal(0.72,0.82) for i in range(0,num)], \
        'fruit':['lemon' for i in range(0,num)]}

        apples = pd.DataFrame(apples)
        mandarin = pd.DataFrame(mandarin)
        orange = pd.DataFrame(orange)
        lemon = pd.DataFrame(lemon)

        fruits2 = pd.concat([apples,mandarin,orange,lemon])
        fruits2 = fruits2.sample(frac = 1.0)

        return fruits2