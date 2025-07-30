from streamlit.components.v1 import html


class InitMessageBridge:
    def __init__(self):
        html(
            """
                <script>
                    window.parent.pendingRequests = {};

                    window.parent.navigateTo = function(target, id, query) {
                        const message = {
                            type: 'NAVIGATE',
                            params: { target, id, query }
                        };
                        window.parent.parent.postMessage(message, '*');
                    }

                    window.parent.openOnScreenResourceForm = function(
                        resource,
                        params = {},
                    ) {
                        const message = {
                        type: 'OPEN_ON_SCREEN_RESOURCE_FORM',
                        params: {
                            resource: { name: resource, id: params.id },
                            data: params.data,
                        },
                        };

                        window.parent.parent.postMessage(message, "*");
                    }

                    window.parent.callApi = async function(resource, action, params){
                        const requestId = crypto.randomUUID();
                        
                        const requestMessage = {
                            type: 'API',
                            requestId,
                            params: {
                                resource: { name: resource, id: params?.id },
                                action,
                                query: params?.query,
                                body: params?.body,
                                queryParams: params?.queryParams,
                            },
                        };

                        const promise = new Promise((resolve, reject) => {
                            window.parent.pendingRequests[requestId] = { resolve, reject };
                        });

                        window.parent.parent.postMessage(requestMessage, "*");
                        return promise;
                    }

                    window.addEventListener("message", (event) => {
                        const message = event.data;
                        if (
                            message.type === 'API_RESPONSE' &&
                            message.requestId
                        ) {
                            const handler = window.parent.pendingRequests[message.requestId];
                            if (!handler) return;

                            if (message.success) {
                                handler.resolve(message.data);
                            } else {
                                handler.reject(message.error);
                            }

                            delete window.parent.pendingRequests[message.requestId];
                        }
                    });
                </script>
            """
        )
