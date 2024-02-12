from flask import Flask, request, render_template_string, redirect, url_for
import requests

app = Flask(__name__)

# HTML template for the home page
HOME_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>URL Expander</title>
</head>
<body>
    <h1 style="text-align: center;">Expaaander</h1>
    <form action="/expand" method="post" style="text-align: center;">
        <input type="text" name="short_url" placeholder="Enter shortened URL" required>
        <button type="submit">Expand</button>
    </form>
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
        # Check if the URL could not be expanded (e.g., status code 4xx/5xx)
        if response.status_code >= 400:
            raise requests.RequestException("URL could not be expanded.")
        expanded_url = response.url
        result_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Expanded URL</title>
</head>
<body style="text-align: center; margin-top: 20%;">
    <h2>✨<a href="{expanded_url}" target="_blank">{expanded_url}</a>✨</h2>
    <form action="/" style="margin-bottom: 20px;">
        <button type="submit">Search Again</button>
    </form>
    {'<form action="/expand" method="post" style="display: inline;"><input type="hidden" name="short_url" value="' + short_url + '"><input type="hidden" name="method" value="get"><button type="submit">Try with GET request</button></form>' if method != 'get' else ''}
</body>
</html>
"""
        return result_page
    except requests.RequestException as e:
        # Show an error message if the URL could not be expanded
        error_message = str(e)
        return render_template_string(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Error</title>
</head>
<body style="text-align: center; margin-top: 20%;">
    <h2>Error expanding URL: {error_message}</h2>
    <form action="/" style="margin-bottom: 20px;">
        <button type="submit">Try Another URL</button>
    </form>
</body>
</html>
""")

if __name__ == '__main__':
    app.run(debug=True)
