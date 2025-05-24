from mitmproxy import http
import json
from urllib.parse import urlparse, parse_qs

JSON_FILE_PATH = "moddeditems.json"

def response(flow: http.HTTPFlow):
    if "/fortnite/api/v2/versioncheck/IOS" in flow.request.url:
        flow.response = http.Response.make(
            200,
            json.dumps({"type": "NO_UPDATE"}),
            {"Content-Type": "application/json"}
        )
        return

    target_url = "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/"
    if target_url in flow.request.url:
        parsed_url = urlparse(flow.request.url)
        query_params = parse_qs(parsed_url.query)

        if query_params.get("profileId") == ["athena"]:
            try:
                with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
                    custom_response = json.load(f)

                flow.response.text = json.dumps(custom_response)
                flow.response.headers["Content-Type"] = "application/json"
            except Exception:
                pass
