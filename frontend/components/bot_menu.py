"""Bot menu component."""
import streamlit as st
from streamlit_option_menu import option_menu
from utils import query_params


class BotMenu:
    """Bot menu component."""

    def __init__(self, pages: dict) -> None:
        """Initialize the navbar."""
        self.pages = pages
        self.saved_page = query_params.get_form_url("page") or list(pages.keys())[0]
        st.session_state.page = self.saved_page

    def __display_logo(self) -> None:
        """Display the logo."""
        st.image("img/logo.png", width=200)

    def __display_bot_info(self, current_bot: str) -> None:
        """Display the bot info."""
        st.markdown(f"bot:```{current_bot}```")
        st.button(
            "Change bot",
            key="change_bot",
            use_container_width=True,
            on_click=self.__clear_bot_id,
        )

    def __display_menu(self) -> None:
        """Display the menu."""
        option_menu(
            "Bot Menu",
            list(self.pages.keys()),
            icons=[p["icon"] for p in self.pages.values()],
            default_index=list(self.pages.keys()).index(self.saved_page),
            # manual_select=list(self.pages.keys()).index(self.saved_page),
            on_change=self.__change_page,
            key="page",
        )

    def __clear_bot_id(self) -> None:
        """Clear the bot id."""
        query_params.set_to_url(bot_id=None)
        query_params.set_to_url(page=None)
        st.session_state.current_bot = None

    def __call__(self, current_bot: str) -> None:
        """Render the navbar."""
        with st.sidebar:
            if current_bot is not None:
                self.__display_logo()
                self.__display_bot_info(current_bot)
                self.__display_menu()

    def __change_page(self, key: str) -> None:
        """Change the page."""
        query_params.set_to_url(page=st.session_state[key])
