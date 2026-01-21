"""
TODO File Handler Module
Handles reading and managing TODO list from a text file
"""
import os
from typing import List, Dict
from datetime import datetime

class TodoHandler:
    """Manages TODO file operations."""

    def __init__(self, todo_path: str = 'todos.txt'):
        """
        Initialize the TODO handler.

        Args:
            todo_path: Path to the TODO file
        """
        # Resolve path relative to project root (parent of backend directory)
        if not os.path.isabs(todo_path):
            # Get the directory containing this file (backend/)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to project root
            project_root = os.path.dirname(current_dir)
            # Join with todo path
            self.todo_path = os.path.join(project_root, todo_path)
        else:
            self.todo_path = todo_path

    def read_todos(self) -> Dict[str, any]:
        """
        Read TODO items from the file.

        Returns:
            Dictionary containing:
            {
                'items': List of TODO items (strings),
                'count': Number of TODO items,
                'last_modified': Last modification timestamp
            }

        Raises:
            FileNotFoundError: If the TODO file doesn't exist
        """
        if not os.path.exists(self.todo_path):
            raise FileNotFoundError(f"TODO file not found: {self.todo_path}")

        if not os.path.isfile(self.todo_path):
            raise ValueError(f"Path is not a file: {self.todo_path}")

        try:
            with open(self.todo_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split into lines and filter out empty lines
            items = [line.strip() for line in content.split('\n') if line.strip()]

            # Get last modified time
            last_modified = os.path.getmtime(self.todo_path)
            last_modified_iso = datetime.fromtimestamp(last_modified).isoformat()

            return {
                'items': items,
                'count': len(items),
                'last_modified': last_modified_iso,
                'raw': content
            }

        except PermissionError as e:
            raise PermissionError(f"Permission denied reading TODO file: {self.todo_path}") from e
        except UnicodeDecodeError as e:
            raise ValueError(f"Invalid file encoding (expected UTF-8): {self.todo_path}") from e

    def get_todo_count(self) -> int:
        """
        Get the count of TODO items.

        Returns:
            Number of TODO items, or 0 if file doesn't exist
        """
        try:
            todos = self.read_todos()
            return todos['count']
        except (FileNotFoundError, ValueError, PermissionError):
            return 0

    def file_exists(self) -> bool:
        """
        Check if the TODO file exists.

        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(self.todo_path) and os.path.isfile(self.todo_path)
