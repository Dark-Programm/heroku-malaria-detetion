from flask import Flask,send_from_directory
import final 
import main

app = Flask(__name__,static_folder='static')

@app.route('/maleria')
def dynamic_page():
    return final.Malarial.runScript("images/111.jpg")


@app.route('/size')
def size_dist():
    return main.SizeMesurment.getSize()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)

