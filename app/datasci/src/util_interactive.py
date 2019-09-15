import matplotlib
import io
import urllib, base64

def printfigs(name="fig", size=None, ending=".png"):
    images = []

    if len(matplotlib.pyplot.get_fignums()) == 1:
        num = matplotlib.pyplot.get_fignums()[0]
        fig = matplotlib.pyplot.figure(num)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        output = 'data:image/png;base64,' + urllib.parse.quote(string)
        images.append("<img src='{}'>".format(output))
        return {'images':images}
        
    for num in matplotlib.pyplot.get_fignums():
        fig = matplotlib.pyplot.figure(num)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        output = 'data:image/png;base64,' + urllib.parse.quote(string)
        images.append("<img src='{}'>".format(output))
    
    return {'images':images}
    #for im in images:
    #print(im)