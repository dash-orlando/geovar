import numpy as np
from stl import mesh

import plotly
import plotly.graph_objs as go
from plotly.offline import *

mesh = mesh.Mesh.from_file('output/2019-05-26__17_29_33/Part_1_var1.stl')


# transform data to plotly array
Ntris = len(mesh.points)
Nnodes = 3 # 3 points per triangle

x = []
y = []
z = []
u = []
v = []
w = []
data = np.zeros((Ntris,3))

for i in range( 0, Ntris ):
    for j in range( 0, Nnodes ):
        x.append( mesh.x[i][j] )
        y.append( mesh.y[i][j] )
        z.append( mesh.z[i][j] )
    u.append( Nnodes*i + 0 )
    v.append( Nnodes*i + 1 )
    w.append( Nnodes*i + 2 )

data = [
    go.Mesh3d(
        x = x,
        y = y,
        z = z,
        colorbar = {
            "title" : "z"
            },
        colorscale = 'Portland',
        intensity = z,
        i = u,
        j = v,
        k = w,
    )
]
layout = go.Layout(
    xaxis=go.layout.XAxis(
        title='x'
    ),
    yaxis=go.layout.YAxis(
        title='y'
    )
)
#fig = go.Figure(data=data, layout=layout)
#py.iplot(fig, filename='3d-mesh-tetrahedron-python')


'''
https://plot.ly/python/reference/#mesh3d
'''
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig)
