import matplotlib
import io
import urllib, base64

def printfigs(name="fig", size=None, ending=".png"):
    #print("Print Figures")
    images = []
    try:
        if len(matplotlib.pyplot.get_fignums()) == 1:
            num = matplotlib.pyplot.get_fignums()[0]
            fig = matplotlib.pyplot.figure(num)
            buf = io.BytesIO()
            if buf :
                fig.savefig(buf, format='png')
                buf.seek(0)
                string = base64.b64encode(buf.read())
                output = 'data:image/png;base64,' + urllib.parse.quote(string)
                image = "<img src='{}' class='img-responsive'>".format(output)
                images.append({"no":1, "src":image})
                matplotlib.pyplot.close()
            #print("(img)")
            return images
        else:
            for num in matplotlib.pyplot.get_fignums():
                fig = matplotlib.pyplot.figure(num)
                buf = io.BytesIO()
                if buf :
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    string = base64.b64encode(buf.read())
                    output = 'data:image/png;base64,' + urllib.parse.quote(string)
                    image = "<img src='{}' class='img-responsive'>".format(output)
                    images.append({"no":num, "src":image})
            matplotlib.pyplot.close()
            return images
    except Exception as e:
        # print(e)
        return False