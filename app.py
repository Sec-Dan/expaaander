from flask import Flask, Response, request, render_template_string
import requests

app = Flask(__name__)

# HTML template for the home page
HOME_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>URL Expander: See Where a Short Link Goes, With No Logging | DanSec</title>
    <meta name="description" content="Free URL expander that shows where a shortened link really goes before you click it. Nothing you enter is stored, and the source code is public.">
    <link rel="canonical" href="https://expaaander.dansec.red/">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://expaaander.dansec.red/">
    <meta property="og:title" content="URL Expander: See Where a Short Link Goes, With No Logging | DanSec">
    <meta property="og:description" content="Free URL expander that shows where a shortened link really goes before you click it. Nothing you enter is stored, and the source code is public.">
    <meta name="twitter:card" content="summary">
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebApplication","name":"URL Expander","url":"https://expaaander.dansec.red/","description":"Free URL expander that shows where a shortened link really goes before you click it. Nothing you enter is stored, and the source code is public.","applicationCategory":"SecurityApplication","operatingSystem":"Any","isAccessibleForFree":true,"publisher":{"@type":"Organization","name":"DanSec","url":"https://dansec.red/"}}</script>
    <link rel="icon" href="/static/favicon.ico">
    <script defer src="https://analytics.swiftworks.dev/script.js" data-website-id="ee822acf-51a1-4199-935f-5cf15cb0e761"></script>
    <style>
        html { color-scheme: dark; }
        body { margin: 0; background: #000; color: rgba(255,255,255,.88); font: 15px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
        main, footer { max-width: 720px; margin: 0 auto; padding: 2rem 1.5rem 0; }
        h1 { color: #EA0000; font-size: 1.5rem; margin: 0 0 .4rem; }
        h2 { color: #EA0000; font-size: 1rem; margin: 1.75rem 0 .4rem; }
        p, li { color: rgba(255,255,255,.62); font-size: .9rem; }
        a { color: rgba(255,255,255,.88); }
        form { display: flex; gap: .5rem; margin: 1.25rem 0; flex-wrap: wrap; }
        input { flex: 1 1 16rem; padding: .6rem; background: #000; color: inherit; border: 1px solid #3a0000; font: inherit; }
        button { padding: .6rem 1.1rem; background: #EA0000; color: #000; border: 0; font: inherit; font-weight: 700; cursor: pointer; }
        footer { padding-bottom: 2rem; }
        footer p { font-size: .78rem; }
    </style>
</head>
<body>
    <main>
        <h1>URL Expander</h1>
        <p>Paste a shortened link to see where it ends up, without opening it yourself.</p>
        <form action="/expand" method="post">
            <input type="text" name="short_url" aria-label="Shortened URL" placeholder="https://bit.ly/example" required>
            <button type="submit" data-umami-event="url-expand">Expand</button>
        </form>

        <h2>Why expand a short link?</h2>
        <p>Short links hide their destination, which makes them useful for phishing. Expanding one shows the final address so you can decide whether to trust it. Our server makes the request rather than your browser, so the destination sees our server and not your IP address.</p>

        <h2>No logging</h2>
        <p>Plenty of link checkers keep what you submit, and you have no way of knowing where it ends up. This one has no database and does not write the URLs you enter anywhere. Analytics are cookieless and count visits and button presses, never the URL. The <a href="https://github.com/Sec-Dan/expaaander">source code is public</a>, so you can check for yourself.</p>

        <h2>What it follows</h2>
        <p>It sends an HTTP HEAD request and follows standard HTTP redirects to the end of the chain. It does not run JavaScript or meta refresh redirects, and sites that reject HEAD requests may return an error. The destination is not checked for safety, so to investigate it further try <a href="https://explorer.dansec.red/">OSINT Explorer</a>.</p>
    </main>
    <footer><p>More free tools from <a href="https://dansec.red/">DanSec</a>: <a href="https://decode.dansec.red/">Safelinks Decoder</a> &middot; <a href="https://agent.dansec.red/">User-Agent Parser</a> &middot; <a href="https://explorer.dansec.red/">OSINT Explorer</a> &middot; <a href="https://worldrisk.dansec.red/">WorldRisk</a> &middot; <a href="https://reports.dansec.red/about">Report Builder</a> &middot; <a href="https://blog.dansec.red/">DanSec Daily</a></p></footer>
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
    <script defer src="https://analytics.swiftworks.dev/script.js" data-website-id="ee822acf-51a1-4199-935f-5cf15cb0e761"></script>
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
    <script defer src="https://analytics.swiftworks.dev/script.js" data-website-id="ee822acf-51a1-4199-935f-5cf15cb0e761"></script>
</head>
<body style="text-align: center; margin-top: 20%;">
    <h2>Error expanding URL: {{error_message}}</h2>
    <form action="/" style="margin-bottom: 20px;">
        <button type="submit">Try Another URL</button>
    </form>
</body>
</html>
        """, error_message=str(e))

@app.route('/robots.txt')
def robots_txt():
    return Response("User-agent: *\nAllow: /\nSitemap: https://expaaander.dansec.red/sitemap.xml\n", mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap_xml():
    return Response('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                    '<url><loc>https://expaaander.dansec.red/</loc></url></urlset>\n', mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True)
