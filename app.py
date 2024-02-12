from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Updated HTML template for the home page with "Learn More" button and modal
HOME_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>URL Expander</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div style="text-align: center;">
        <h1>Expaaander</h1>
        <form action="/expand" method="post">
            <input type="text" name="short_url" placeholder="Enter shortened URL" required>
            <button type="submit">Expand</button>
        </form>

        <!-- Learn More Button -->
        <button type="button" class="btn btn-info" data-toggle="modal" data-target="#learnMoreModal">
          Learn More
        </button>

        <!-- Learn More Modal -->
        <div class="modal fade" id="learnMoreModal" tabindex="-1" role="dialog" aria-labelledby="learnMoreModalLabel" aria-hidden="true">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="learnMoreModalLabel">About Expaaander</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                Expaaander is a web-based Flask application designed with Python for online safety and transparency by expanding shortened URLs.
                
                There is 0 logging, idc what's entered
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</body>
</html>
"""

@app.route('/')
def home():
    return HOME_PAGE_TEMPLATE

@app.route('/expand', methods=['POST'])
def expand_url():
    short_url = request.form['short_url']
    try:
        response = requests.head(short_url, allow_redirects=True)
        if response.status_code >= 400:
            raise requests.RequestException("URL could not be expanded.")
        expanded_url = response.url
        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Expanded URL</title>
</head>
<body style="text-align: center; margin-top: 20%;">
    <h2>✨<a href="{{expanded_url}}" target="_blank">{{expanded_url}}</a>✨</h2>
    <form action="/" style="margin-bottom: 20px;">
        <button type="submit">Search Again</button>
    </form>
</body>
</html>
        """, expanded_url=expanded_url)
    except requests.RequestException as e:
        # Render error message if the URL could not be expanded
        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Error</title>
</head>
<body style="text-align: center; margin-top: 20%;">
    <h2>Error expanding URL: {{error_message}}</h2>
    <form action="/" style="margin-bottom: 20px;">
        <button type="submit">Try Another URL</button>
    </form>
</body>
</html>
        """, error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
