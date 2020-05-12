import os
import sys
import youtube_dl
from flask import Flask, jsonify, request
from flask_restx import Resource, Api, fields, reqparse

app = Flask(__name__)

api = Api(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


print(app.config, file=sys.stderr)


class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong',
        }


api.add_resource(Ping, '/ping')


video = api.model('Video', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'source_url': fields.String(required=True, description='Source URL'),
})


class VideoDAO(object):
    def __init__(self):
        self.videos = []

    def all(self):
        return self.videos

    def create(self, data):
        video = data
        # print(data.form['source_url'], file=sys.stderr)
        # return request.form['source_url']

        class YDLLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg, file=sys.stderr)

        def my_hook(d):
            # print(d, file=sys.stderr)
            if d['status'] == 'finished':
                print('Done downloading, now converting ...', file=sys.stderr)
                # print("Owner id of the file:", os.stat(d['filename']).st_uid, file=sys.stderr)
                # print("Group id of the file:", os.stat(d['filename']).st_gid, file=sys.stderr)
                # os.chown(d['filename'], 1000, 0)
                # os.chmod(d['filename'], 0o664)
                # print("Owner id of the file:", os.stat(d['filename']).st_uid, file=sys.stderr)
                # print("Group id of the file:", os.stat(d['filename']).st_gid, file=sys.stderr)

        options = {
            # 'format': 'bestaudio/best',
            'logger': YDLLogger(),
            'progress_hooks': [my_hook],
            'outtmpl': 'project/downloads/%(title)s-%(id)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=E27v_Irt8eU'])



DAO = VideoDAO()
ns = api.namespace('videos', description='Video handler')


@ns.route('/')
class Video(Resource):
    def get(self):
        '''List all videos'''
        return DAO.all()

    @ns.marshal_with(video, code=201)
    def post(self):
        '''Download video'''
        return DAO.create(api.payload), 201
