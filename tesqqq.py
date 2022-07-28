# Create the Flask 'app'
from flask import Flask, g
app = Flask(__name__)

# Set the configuration items manually for the example
app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
# You can use a different instance of freegeoip like so
# app.config['TRACK_USAGE_FREEGEOIP_ENDPOINT'] = 'https://example.org/api/'
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'include'

# We will just print out the data for the example
from flask_track_usage import TrackUsage

# We will just print out the data for the example
from flask_track_usage.storage.printer import PrintWriter
from flask_track_usage.storage.output import OutputWriter

# Make an instance of the extension and put two writers
t = TrackUsage(app, [
    PrintWriter(),
    OutputWriter(transform=lambda s: "OUTPUT: " + str(s))
])

# Include the view in the metrics
@t.include
@app.route('/')
def index():
    g.track_var["optional"] = "something"
    return "Hello"

# Run the application!
app.run(debug=True)