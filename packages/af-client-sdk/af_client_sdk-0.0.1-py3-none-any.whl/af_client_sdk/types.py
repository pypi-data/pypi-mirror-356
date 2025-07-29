class GuardedResult:
    def __init__(self, blocked: bool, reason: str, final_response: str):
        self.blocked = blocked
        self.reason = reason
        self.final_response = final_response


class AnalysisContext:
    def __init__(
        self,
        session_id: str = None,
        user_id: str = None,
        provider: str = None,
        model_name: str = None,
        model_version: str = None,
        platform: str = None,
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.provider = provider
        self.model = model_name
        self.version = model_version
        self.platform = platform
