import streamlit as st
from ..constants.common import API_REQ_KEY_PREFIX
from typing import TypedDict, Optional, Any, Dict
from .api_option import ApiOption


class Helper:
    @staticmethod
    def get_api_key(
        type: str, resource: str, action: str, options: Optional[ApiOption] = {}
    ):
        key = type.upper()

        if options.get("api_key"):
            return f"{API_REQ_KEY_PREFIX}_{resource.upper()}_{action.upper()}_{options.get("api_key")}_{key}"

        return f"{API_REQ_KEY_PREFIX}_{resource.upper()}_{action.upper()}_{key}"

    @staticmethod
    def get_api_response(resource: str, action: str, options: Optional[ApiOption] = {}):
        response_key = Helper.get_api_key("response", resource, action, options)
        return st.session_state.get(response_key)

    @staticmethod
    def set_api_response(resource: str, action: str, options: Optional[ApiOption] = {}):
        request_key = Helper.get_api_key("request", resource, action, options)
        raw_data = st.session_state[request_key]
        if raw_data:
            response_key = Helper.get_api_key("response", resource, action, options)
            st.session_state[response_key] = raw_data
