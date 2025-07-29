"""Session store for maintaining client state."""

from .models import ProductConfig, Provider, SessionAPIResponse, SessionState, UserInfo


class SessionStore:
    """Store for session state management."""

    def __init__(self) -> None:
        self.product_key: str | None = None
        self.session_id: str | None = None
        self.user: UserInfo | None = None
        self.config: ProductConfig | None = None
        self.is_blocked: bool = False
        self.providers: Provider = {}
        self.session_state: SessionState = SessionState.NOT_STARTED
        self.session_data: SessionAPIResponse | None = None

    def reset(self) -> None:
        """Reset the store to initial state."""
        self.session_id = None
        self.user = None
        self.config = None
        self.is_blocked = False
        self.session_state = SessionState.NOT_STARTED
        self.session_data = None

    def is_session_active(self) -> bool:
        """Check if there's an active session."""
        return (
            self.session_state == SessionState.SUCCESS
            and self.session_id is not None
            and not self.is_blocked
        )
