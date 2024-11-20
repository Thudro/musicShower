from flask import Flask, jsonify
import win32com.client  # This can interact with windows processes
import time

app = Flask(__name__)

def get_current_playing():
    try:
        #From what i've read, this works with spotify so I hope it works with Amazon.
        wmi = win32com.client.GetObject('winmgmts:')

        for process in wmi.InstancesOf('Win32_Process'):
            if process.Name.lower() == 'amazon music.exe':
                return process.Caption
        return "No song playing"
    
    except Exception as e:
        return str(e)

@app.route('/now-playing', methods=['GET'])
def now_playing():
    playing_info = get_currently_playing()
    return jsonify({'now_playing': playing_info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
