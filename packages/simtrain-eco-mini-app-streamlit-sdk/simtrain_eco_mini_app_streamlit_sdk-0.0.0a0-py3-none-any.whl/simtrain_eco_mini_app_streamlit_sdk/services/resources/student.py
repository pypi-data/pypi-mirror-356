from streamlit_javascript import st_javascript
from ..helper import Helper
from typing import Optional
from ..api_option import ApiOption
from streamlit.components.v1 import html


class Student:
    _resource_name = "student"

    def list(self, options: Optional[ApiOption] = {}):
        action = "list"
        request_key = Helper.get_api_key(
            "request", resource=self._resource_name, action=action, options=options
        )

        st_javascript(
            "window.parent.callApi('student', 'list')",
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

        st_javascript(
            f"""
            window.parent.callApi('student', 'detail', {{
                id: '{id}'
            }})
            """,
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
