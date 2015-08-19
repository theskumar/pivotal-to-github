import re
import os
from dotenv import load_dotenv

from busyflow.pivotal import PivotalClient
from flask import Flask, render_template

app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

pivotal_token = os.environ['PIVOTAL_TOKEN']
client = PivotalClient(token=pivotal_token)


def get_story(url):
    regex = re.compile('.*projects/(\d+)/stories/(\d+).*')
    try:
        project_id, story_id = regex.findall(url)[0]
    except IndexError:
        return None
    return client.stories.get(project_id, story_id)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    data = get_story(path)
    if data:
        return render_template('index.html', story=data['story'])
    else:
        return render_template('bookmarklet.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
