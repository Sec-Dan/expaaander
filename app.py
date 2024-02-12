from flask import Flask, request, render_template_string, redirect, url_for
import requests

app = Flask(__name__)

# Updated HTML template for the home page with "Learn More" button and modal
HOME_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>URL Expander</title>
    <!-- Include Bootstrap for styling and modal functionality -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <h1 style="text-align: center;">Expaaander</h1>
    <form action="/expand" method="post" style="text-align: center;">
        <input type="text" name="short_url" placeholder="Enter shortened URL" required>
        <button type="submit">Expand</button>
    </form>

    <!-- Learn More Button -->
    <button type="button" class="btn btn-info" data-toggle="modal" data-target="#learnMoreModal" style="display: block; margin: 20px auto;">
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
            Expaaander is a web-based application designed to enhance online safety and transparency by expanding shortened URLs...
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap JS and dependencies for modal functionality -->
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
    method = request.form.get('method', 'head')
    try:
        if method == 'get':
            response = requests.get(short_url, allow_redirects=True)
        else:  # Default to HEAD request
            response = requests.head(short_url, allow_redirects=True)
        if response.status_code >= 400:
            raise requests.RequestException("URL could not be expanded.")
        expanded_url = response.url
        # The rest of your expand_url logic remains unchanged

        # Remember to include the Bootstrap JS links in the result and error pages as well
        return result_page  # Ensure result_page includes Bootstrap JS if modified
    except requests.RequestException as e:
        # Show an error message if the URL could not be expanded
        # Ensure the error page includes Bootstrap JS if modified
        return error_page

if __name__ == '__main__':
    app.run(debug=True)
