import reflex as rx
from chattum_ui.utils import backend_controller as bc

from .state import State


class SourcesState(State):
    sources: list[dict] = []
    source_id: str = None
    source: dict = {}

    # source_file: bytes = None

    def load_sources(self) -> None:
        self.sources = bc.get_sources(self.bot_id)

    def load_source(self, source_id: str) -> None:
        self.source_id = source_id
        self.source = bc.get_source(self.bot_id, source_id)
        print(self.source)

    def download_source(self) -> None:
        file_url = bc.get_source_file(self.bot_id, self.source_id)["file_url"]
        return rx.redirect(str(file_url), external=True)

    def delete_source(self) -> None:
        bc.delete_source(self.bot_id, self.source_id)
        self.load_sources()
        self.source_id = None


class NewSourceState(State):
    modal_opened: bool = False
    valid_file_types: list[str] = ["pdf", "url", "pdf", "xls", "txt"]

    source_type: str = "pdf"
    source_name: str = None
    source_url: str = None
    _source_file: bytes = None

    adding_in_progress: bool = False

    def change_modal_state(self) -> None:
        self.modal_opened = not self.modal_opened

    def set_source_type(self, source_type: str) -> None:
        self.source_type = source_type
        print(self.source_type_valid)

    async def set_source_file(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            self._source_file = await file.read()
        print(self.source_file_valid)

    def set_source_name(self, source_name: str) -> None:
        self.source_name = source_name
        print(self.source_name_valid)

    def add_new_source(self, form_data: dict) -> None:
        self.adding_in_progress = True
        print(self.form_valid)
        bc.create_new_source(
            self.source_name,
            self.source_type,
            self.bot_id,
            self._source_file,
            self.source_url,
        )
        self.adding_in_progress = False
        self.modal_opened = False
        SourcesState.load_sources()

    @rx.var
    def source_type_valid(self) -> bool:
        return self.source_type in self.valid_file_types

    @rx.var
    def source_file_valid(self) -> bool:
        return self._source_file is not None

    @rx.var
    def source_name_valid(self) -> bool:
        return self.source_name is not None

    @rx.var
    def source_url_valid(self) -> bool:
        return self.source_url is not None

    @rx.var
    def form_valid(self) -> bool:
        if self.source_type == "url":
            return (
                self._source_file is None
                and self.source_type_valid
                and self.source_name_valid
                and self.source_url_valid,
            )
        else:
            return (
                self.source_url is None
                and self.source_type_valid
                and self.source_file_valid
                and self.source_name_valid,
            )
