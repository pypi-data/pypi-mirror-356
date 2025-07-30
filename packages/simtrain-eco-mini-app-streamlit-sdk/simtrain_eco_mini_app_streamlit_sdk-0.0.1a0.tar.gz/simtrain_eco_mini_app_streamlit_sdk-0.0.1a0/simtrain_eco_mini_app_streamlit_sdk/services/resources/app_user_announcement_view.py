from streamlit_javascript import st_javascript
from ..helper import Helper
from typing import Optional
from ..api_option import ApiOption
from streamlit.components.v1 import html
import json


class AppUserAnnouncementView:
    _resource_name = "appUserAnnouncementView"

    def list(self, options: Optional[ApiOption] = {}):
        action = "list"
        request_key = Helper.get_api_key(
            "request", resource=self._resource_name, action=action, options=options
        )

        st_javascript(
            f"window.parent.callApi('{self._resource_name}', '{action}')",
            key=request_key,
            on_change=lambda: Helper.set_api_response(
                resource=self._resource_name, action=action, options=options
            ),
        )

    def detail(self, id: str, options: Optional[ApiOption] = {}):
        action = "detail"
        request_key = Helper.get_api_key(
            "request", resource=self._resource_name, action=action, options=options
        )
        payload = json.dumps({"id": id})

        st_javascript(
            f"window.parent.callApi('{self._resource_name}', '{action}', {payload})",
            key=request_key,
            on_change=lambda: Helper.set_api_response(
                resource=self._resource_name, action=action, options=options
            ),
        )

    def autoComplete(self, query: str, data={}, options: Optional[ApiOption] = {}):
        action = "autoComplete"
        request_key = Helper.get_api_key(
            "request", resource=self._resource_name, action=action, options=options
        )

        payload = json.dumps({"query": query, "body": data})
        st_javascript(
            f"window.parent.callApi('{self._resource_name}', '{action}', {payload})",
            key=request_key,
            on_change=lambda: Helper.set_api_response(
                resource=self._resource_name, action=action, options=options
            ),
        )

    def response(self, action: str, options: Optional[ApiOption] = {}):
        return Helper.get_api_response(
            resource=self._resource_name, action=action, options=options
        )

    def openOnScreenForm(self, id: Optional[str] = None):
        id_js = f"'{id}'" if id else "undefined"

        html(
            f"""
          <script>
              window.parent.openOnScreenResourceForm('{self._resource_name}', {{
                  id: {id_js}
              }});
          </script>
          """,
            height=0,
        )
