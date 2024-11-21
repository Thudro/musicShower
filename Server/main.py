from flask import Flask, jsonify
import asyncio

from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

app = Flask(__name__)

#This helped a lot, just changing the winrt to winsdk 
#https://github.com/curtisgibby/winrt-slack-python/blob/master/winrt-track-change-to-slack.py#L177-L183

async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        info = await current_session.try_get_media_properties_async()

        #This adds ALL the data from the sdk to a dictionary
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        #We only want the title and artist tho
        concat = info_dict['title'] + " -" + info_dict['artist']
        return concat


@app.route('/now-playing', methods=['GET'])
def now_playing():
    current_media_info = asyncio.run(get_media_info())
    #We want to use json for the data on the server, so Im using jsonify 
    return jsonify({'now_playing': current_media_info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
