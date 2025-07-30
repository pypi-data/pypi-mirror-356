"""State and event handlers for the IDE."""

import asyncio
import logging
import time
from pathlib import Path
from uuid import uuid4

import aiofiles
import reflex as rx
from reflex.event import EventCallback, KeyInputInfo, key_event
from reflex.utils import imports
from typing_extensions import Unpack, override
from watchfiles import Change, awatch

from pycodium.models.files import FilePath
from pycodium.models.tabs import EditorTab
from pycodium.utils.detect_encoding import decode
from pycodium.utils.detect_lang import detect_programming_language

logger = logging.getLogger(__name__)


class EditorState(rx.State):
    """Global state of the IDE."""

    # UI state variables
    sidebar_visible: bool = True
    panel_visible: bool = True
    active_sidebar_tab: str = "explorer"

    # Editor state
    tabs: list[EditorTab] = []
    active_tab_id: str | None = None
    active_tab_history: list[str] = []

    # Explorer state
    project_root: Path = Path.cwd()
    expanded_folders: set[str] = set()
    file_tree: FilePath | None = None

    @rx.event
    async def toggle_sidebar(self) -> None:
        """Toggle the sidebar visibility."""
        logger.debug(f"Sidebar visibility changed to {not self.sidebar_visible}")
        self.sidebar_visible = not self.sidebar_visible

    @rx.event
    async def set_active_sidebar_tab(self, tab: str) -> None:
        """Set the active sidebar tab."""
        logger.debug(f"Active sidebar tab changed to {tab}")
        self.active_sidebar_tab = tab

    @rx.event
    async def toggle_folder(self, folder_path: str) -> None:
        """Toggle the expanded state of a folder.

        Args:
            folder_path: The path of the folder to toggle.
        """
        logger.debug(f"Toggling folder {folder_path}")
        if folder_path in self.expanded_folders:
            self.expanded_folders.remove(folder_path)
        else:
            self.expanded_folders.add(folder_path)

    def _stop_updating_active_tab(self) -> None:
        if not (active_tab := self.active_tab):
            logger.warning("No active tab to stop updating")
            return
        active_tab.on_not_active.set()  # Signal to stop watching the file for changes

    @rx.event
    async def open_file(self, file_path: str) -> rx.Component | EventCallback[Unpack[tuple[()]]] | None:
        """Open a file in the editor.

        Args:
            file_path: The path to the file to open.
        """
        logger.debug(f"Opening file {file_path}")

        tab = next((tab for tab in self.tabs if tab.path == file_path), None)

        # Add to open files if not already open
        if not tab:
            async with aiofiles.open(self.project_root.parent / file_path, "rb") as f:
                file_content = await f.read()

            # PEP3120 suggests using UTF-8 as the default encoding for Python source files
            default_encoding = "utf-8" if file_path.endswith((".py", ".pyw", ".ipy", ".pyi")) else None
            decoded_file_content, encoding = decode(file_content, default_encoding=default_encoding)
            if encoding.endswith("-guessed"):
                return rx.toast.error("The file is either binary or uses an unsupported text encoding.")
            logger.debug(f"Detected encoding for {file_path}: {encoding}")

            tab = EditorTab(
                id=str(uuid4()),
                title=file_path,
                language=detect_programming_language(file_path).lower(),
                content=decoded_file_content,
                encoding=encoding,
                path=file_path,
                on_not_active=asyncio.Event(),
            )
            self.tabs.append(tab)
            logger.debug(f"Created tab {tab.id}")

        if self.active_tab_id:
            self.active_tab_history.append(self.active_tab_id)
            self._stop_updating_active_tab()

        self.active_tab_id = tab.id
        return EditorState.keep_active_tab_content_updated

    async def _save_current_file(self) -> None:
        """Save the content of the currently active tab to its file."""
        active_tab = self.active_tab
        if not active_tab:
            logger.warning("No active tab to save")
            return

        logger.debug(f"Saving content of tab {active_tab.id} to {active_tab.path}")
        async with aiofiles.open(self.project_root.parent / active_tab.path, "w", encoding=active_tab.encoding) as f:
            await f.write(active_tab.content)
        logger.debug(f"Content of tab {active_tab.id} saved successfully")

    @rx.event
    async def close_tab(self, tab_id: str) -> None:
        """Close a tab by its ID.

        Args:
            tab_id: The ID of the tab to close.
        """
        logger.debug(f"Closing tab {tab_id}")
        self._stop_updating_active_tab()
        self.tabs = [tab for tab in self.tabs if tab.id != tab_id]
        self.active_tab_history = [tab for tab in self.active_tab_history if tab != tab_id]

        if self.active_tab_id == tab_id and self.active_tab_history:
            previous_tab_id = self.active_tab_history.pop()
            logger.debug(f"Switching to previous tab {previous_tab_id}")
            self.active_tab_id = previous_tab_id
        elif self.active_tab_id != tab_id:
            logger.debug("Active tab is not the one being closed, no switch needed")
        else:
            logger.debug("No previous tab to switch to, setting active tab to None")
            self.active_tab_id = None

    @rx.event
    async def set_active_tab(self, tab_id: str) -> EventCallback[Unpack[tuple[()]]] | None:
        """Set the active tab by its ID.

        Args:
            tab_id: The ID of the tab to set as active.
        """
        if tab_id not in {tab.id for tab in self.tabs}:
            logger.warning(f"Tab {tab_id} not found in open tabs")
            return
        if self.active_tab_id == tab_id:
            logger.debug(f"Tab {tab_id} is already active, no change needed")
            return
        logger.debug(f"Setting active tab {tab_id}")
        if self.active_tab_id is not None:
            self.active_tab_history.append(self.active_tab_id)
            self._stop_updating_active_tab()
        self.active_tab_id = tab_id
        self.active_tab.on_not_active.clear()  # type: ignore[reportOptionalMemberAccess]
        return EditorState.keep_active_tab_content_updated

    @rx.var
    def active_tab(self) -> EditorTab | None:
        """Get the currently active tab as a computed variable.

        Returns:
            The active `EditorTab` instance, or None if no tab is active.
        """
        return next((tab for tab in self.tabs if tab.id == self.active_tab_id), None)

    @rx.var
    def editor_content(self) -> str:
        """Get the content of the currently active tab.

        Returns:
            The content of the active tab as a string.
        """
        active_tab = self.active_tab
        if not active_tab:
            return ""
        return active_tab.content

    @rx.var
    def current_file(self) -> str | None:
        """Get the path of the currently active tab.

        Returns:
            The path of the active tab as a string.
        """
        active_tab = self.active_tab
        if not active_tab:
            return None
        return active_tab.path

    @rx.event
    async def update_tab_content(self, tab_id: str, content: str) -> None:
        """Update the content of a specific tab.

        Args:
            tab_id: The ID of the tab to update.
            content: The new content for the tab.
        """
        logger.debug(f"Updating content of tab {tab_id}")
        for tab in self.tabs:
            if tab.id == tab_id:
                tab.content = content
                break

    def _build_file_tree(self, path: Path) -> FilePath:
        """Build the file tree for a given path.

        Args:
            path: The path to the file to build.

        Returns:
            FilePath: The file tree for the given path.
        """
        file_tree = FilePath(name=path.name)

        for file_path in path.iterdir():
            if file_path.is_dir():
                sub_tree = self._build_file_tree(file_path)
                file_tree.sub_paths.append(sub_tree)
            else:
                file_tree.sub_paths.append(FilePath(name=file_path.name, is_dir=False))

        return file_tree

    def _sort_file_tree(self, file_tree: FilePath) -> None:
        """Sort the file tree by name with directories first.

        Args:
            file_tree: The file tree to sort.

        """
        file_tree.sub_paths.sort(key=lambda x: (not x.is_dir, x.name))
        for sub_path in file_tree.sub_paths:
            if sub_path.is_dir:
                self._sort_file_tree(sub_path)

    @rx.event
    def open_project(self) -> None:
        """Open a project in the editor."""
        logger.debug(f"Opening project {self.project_root}")
        start_time = time.perf_counter()
        self.file_tree = self._build_file_tree(self.project_root)
        self._sort_file_tree(self.file_tree)
        self.expanded_folders.add(self.project_root.name)
        logger.debug(f"File tree built in {time.perf_counter() - start_time:.2f} seconds")

    @rx.event
    async def open_settings(self) -> None:
        """Open the settings tab."""
        logger.debug("Opening settings tab")
        settings_tab = next((tab for tab in self.tabs if tab.id == "settings"), None)
        if not settings_tab:
            settings_tab = EditorTab(
                id="settings",
                title="Settings",
                language="json",
                content="{}",
                encoding="utf-8",
                path="settings.json",
                on_not_active=asyncio.Event(),
                is_special=True,
                special_component="settings",
            )
            self.tabs.append(settings_tab)
        await self.set_active_tab(settings_tab.id)

    @rx.event
    async def on_key_down(self, key: str, key_info: KeyInputInfo) -> None:
        """Handle global key down events."""
        logger.debug(f"Key pressed: {key}, Key Info: {key_info}")
        # TODO: make this work in pywebview
        if key_info["meta_key"] and key.lower() == "s":
            await self._save_current_file()
        elif key_info["meta_key"] and key.lower() == "w" and self.active_tab_id:
            await self.close_tab(self.active_tab_id)

    @rx.event(background=True)
    async def keep_active_tab_content_updated(self) -> None:
        """Keep the content of the active tab updated by watching its file for changes."""
        active_tab = self.active_tab
        if not active_tab:
            logger.warning("No active tab to watch for changes")
            return
        file_path = self.project_root.parent / active_tab.path
        logger.debug(f"Starting to watch tab {active_tab.id} for changes from file {file_path}")
        async for changes in awatch(file_path, stop_event=active_tab.on_not_active):
            for change in changes:
                if change[0] == Change.modified:
                    async with aiofiles.open(file_path, encoding=active_tab.encoding) as f, self:
                        active_tab.content = await f.read()

                        # workaround for https://github.com/orgs/reflex-dev/discussions/1644
                        self.tabs = self.tabs
                    logger.debug(f"Updated content of tab {active_tab.id} from file {file_path}")
        logger.debug(f"Stopped watching tab {active_tab.id} for changes from file {file_path}")


class GlobalHotkeyWatcher(rx.Fragment):
    """A component that listens for key events globally.

    Copied from https://reflex.dev/docs/api-reference/browser-javascript/#using-react-hooks
    """

    on_key_down: rx.EventHandler[key_event]

    @override
    def add_imports(self) -> imports.ImportDict:
        """Add the imports for the component."""
        return {
            "react": [imports.ImportVar(tag="useEffect")],
        }

    @override
    def add_hooks(self) -> list[str | rx.Var[str]]:
        """Add the hooks for the component."""
        return [
            """
            useEffect(() => {
                const handle_key = %s;
                document.addEventListener("keydown", handle_key, false);
                return () => {
                    document.removeEventListener("keydown", handle_key, false);
                }
            })
            """  # noqa: UP031
            % str(rx.Var.create(self.event_triggers["on_key_down"]))
        ]
