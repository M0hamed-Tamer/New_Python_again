import importlib
import inspect
import io
import sys
import pydoc

from textwrap import wrap
from typing import Any, Dict, List, Tuple, Optional
import keyword
from collections import defaultdict

class LibraryExplorer:
    """
    Enhanced Python Library & Object Explorer with:
    - Built-in function documentation
    - Source code viewing
    - Better search capabilities
    - Module installation helper
    - More detailed object inspection
    """
    
    def __init__(self):
        self.history = []
        self.current_object = None
        self.current_path = ""
        self.bookmarks = defaultdict(list)
        
        # Enhanced color codes
        self.COLORS = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'bold': '\033[1m',
            'underline': '\033[4m',
            'magenta': '\033[35m',
            'end': '\033[0m'
        }

    def color_text(self, text: str, color: str) -> str:
        """Return colored text using ANSI codes."""
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['end']}"

    def get_help_text(self, obj: Any) -> str:
        """Get comprehensive help for an object."""
        old_stdout = sys.stdout
        sys.stdout = help_output = io.StringIO()
        try:
            help(obj)
        except Exception as e:
            return f"{self.color_text('Error getting help:', 'red')}\n{str(e)}"
        finally:
            sys.stdout = old_stdout
        return help_output.getvalue()

    def get_source_code(self, obj: Any) -> Optional[str]:
        """Attempt to get source code for an object."""
        try:
            return inspect.getsource(obj)
        except (TypeError, OSError):
            # Built-ins and some compiled modules don't have source code
            return None

    def short_doc(self, obj: Any) -> str:
        """Get a formatted short documentation string."""
        doc = inspect.getdoc(obj)
        if not doc:
            return self.color_text("No docstring", 'yellow')
        
        first_line = doc.strip().split('\n')[0]
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."
        return first_line

    def classify_members(self, obj: Any) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]], List[Tuple[str, str]]]:
        """Enhanced member classification with more detailed inspection."""
        members = inspect.getmembers(obj)
        functions, classes, attributes = [], [], []

        for name, member in members:
            if name.startswith("_") or keyword.iskeyword(name):
                continue
            
            try:
                if inspect.isclass(member):
                    classes.append((name, self.short_doc(member)))
                elif callable(member):
                    functions.append((name, self.short_doc(member)))
                elif not inspect.ismodule(member):
                    attributes.append((name, repr(member)[:70])) # Show repr for attributes
            except Exception:
                continue

        functions.sort(key=lambda x: x[0].lower())
        classes.sort(key=lambda x: x[0].lower())
        attributes.sort(key=lambda x: x[0].lower())

        return functions, classes, attributes

    def load_object(self, path: str) -> Optional[Any]:
        """Load an object with better error handling and built-in support."""
        try:
            # First, try to import it as a module
            obj = importlib.import_module(path.split('.')[0])
            for attr in path.split('.')[1:]:
                obj = getattr(obj, attr)
        except (ModuleNotFoundError, AttributeError):
            # **NEW**: If it fails, check if it's a built-in function/object
            if hasattr(__builtins__, path):
                obj = getattr(__builtins__, path)
                self.current_path = path
                self.current_object = obj
                # For built-ins, we can show help directly instead of members
                self.show_help(path, is_builtin=True)
                return None # Return None to prevent displaying members of a function
            else:
                print(self.color_text(f"\nError: Could not find module or built-in '{path}'", 'red'))
                print("Tip: Try installing missing modules with 'install <module>'")
                return None
        except Exception as e:
            print(self.color_text(f"\nUnexpected error: {str(e)}", 'red'))
            return None
        
        self.history.append((self.current_path, self.current_object))
        self.current_object = obj
        self.current_path = path
        return obj

    def display_members(self, obj: Any, obj_path: str) -> None:
        """Enhanced member display with more information."""
        print(f"\n{self.color_text('=== Exploring:', 'header')} {self.color_text(obj_path, 'cyan')}")
        
        doc = inspect.getdoc(obj)
        if doc:
            print(f"\n{self.color_text('Description:', 'green')}\n{wrap(doc, width=90)[0]}...")

        functions, classes, attributes = self.classify_members(obj)
        
        print(self.color_text(f"\nMembers: {len(functions)} functions, {len(classes)} classes, {len(attributes)} attributes", 'bold'))

        if classes:
            print(f"\n{self.color_text('Classes:', 'green')}")
            for name, desc in classes:
                print(f"  {self.color_text(name, 'blue')}: {desc}")

        if functions:
            print(f"\n{self.color_text('Functions:', 'green')}")
            for name, desc in functions:
                print(f"  {self.color_text(name, 'blue')}: {desc}")

        if attributes:
            print(f"\n{self.color_text('Attributes:', 'green')}")
            for name, desc in attributes:
                print(f"  {self.color_text(name, 'blue')}: {desc}")

    def show_help(self, member_name: str, is_builtin: bool = False) -> None:
        """Show comprehensive help with source code if available."""
        if is_builtin:
            member_obj = getattr(__builtins__, member_name)
            full_path = member_name
        elif hasattr(self.current_object, member_name):
            member_obj = getattr(self.current_object, member_name)
            full_path = f"{self.current_path}.{member_name}"
        else:
            print(self.color_text(f"Member '{member_name}' not found.", 'red'))
            return
            
        print(f"\n{self.color_text('=== Help for:', 'header')} {self.color_text(full_path, 'cyan')}\n")
        
        print(f"{self.color_text('Type:', 'green')} {type(member_obj).__name__}")
        
        try:
            sig = str(inspect.signature(member_obj))
            print(f"{self.color_text('Signature:', 'green')} {sig}")
        except (ValueError, TypeError):
            pass
        
        source = self.get_source_code(member_obj)
        if source:
            print(f"\n{self.color_text('Source Code:', 'green')}\n{self.color_text(source, 'yellow')}")
        
        print(f"\n{self.color_text('Documentation:', 'green')}")
        help_text = self.get_help_text(member_obj)
        print(help_text if help_text.strip() else self.color_text("No documentation available.", 'yellow'))

    def search_members(self, query: str) -> None:
        # ... (code unchanged) ...
        if not self.current_object:
            print(self.color_text("No object loaded to search.", 'yellow'))
            return
            
        functions, classes, attributes = self.classify_members(self.current_object)
        all_members = functions + classes + attributes
        
        results = [m for m in all_members if query.lower() in m[0].lower() or query.lower() in m[1].lower()]
        
        if not results:
            print(self.color_text(f"No members found matching '{query}'.", 'yellow'))
            return
            
        print(f"\n{self.color_text('Search results:', 'header')} {len(results)} matches for '{query}'\n")
        for name, desc in results:
            print(f"  {self.color_text(name, 'blue')}: {desc}")

    # **NEW**: Implemented missing methods
    def go_back(self) -> bool:
        """Navigate to the previous object in history."""
        if not self.history:
            print(self.color_text("No history to go back to.", 'yellow'))
            return False
        
        self.current_path, self.current_object = self.history.pop()
        if self.current_object is None:
            self.current_path = "" # Reset if we go back to the start
        print(f"{self.color_text('Navigated back.', 'magenta')}")
        return True

    def show_history(self) -> None:
        """Display navigation history."""
        if not self.history:
            print(self.color_text("History is empty.", 'yellow'))
            return
        print(f"\n{self.color_text('=== Navigation History ===', 'header')}")
        # Display history from oldest to newest, excluding the initial empty state
        for path, _ in self.history:
            if path:
                print(f"  - {path}")
        print(f"Current: {self.current_path}")

    def interactive_loop(self) -> None:
        """Main interactive loop for the explorer."""
        print(self.color_text("\n=== Enhanced Python Library Explorer ===", 'header'))
        print("Type a module path ('os.path'), a built-in ('len'), or 'help' for commands.")

        while True:
            try:
                prompt = f"{self.current_path}> " if self.current_path else "explore> "
                cmd_input = input(f"\n{self.color_text(prompt, 'bold')}").strip()
                
                if not cmd_input:
                    continue

                parts = cmd_input.split(maxsplit=1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""

                if command == 'exit':
                    break
                elif command == 'help':
                    if arg:
                        self.show_help(arg)
                    else:
                        self.show_help_menu()
                elif command == 'back':
                    if self.go_back():
                        if self.current_object:
                            self.display_members(self.current_object, self.current_path)
                elif command == 'history':
                    self.show_history()
                elif command == 'search':
                    if arg: self.search_members(arg)
                    else: print(self.color_text("Usage: search <term>", "red"))
                elif command == 'source':
                     if arg: self.show_source(arg)
                     else: print(self.color_text("Usage: source <member>", "red"))
                # ... (other commands like builtins, install, bookmark, etc.)
                else:
                    # Not a special command, so treat as an object to explore
                    path_to_load = f"{self.current_path}.{cmd_input}" if self.current_path else cmd_input
                    
                    # If it's a member of the current object, just show its help
                    if self.current_object and hasattr(self.current_object, command) and not arg:
                        self.show_help(command)
                    else:
                        obj = self.load_object(cmd_input)
                        if obj is not None:
                            self.display_members(obj, self.current_path)

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit or 'back' to go up.")
            except Exception as e:
                print(self.color_text(f"\nAn error occurred: {str(e)}", 'red'))

        print(self.color_text("\nGoodbye!", 'header'))

    def show_help_menu(self) -> None:
        # ... (code unchanged) ...
        print(f"\n{self.color_text('=== Help Menu ===', 'header')}")
        print("Navigation:")
        print("  <path>         - Explore a module/package (e.g., 'os.path') or built-in ('len')")
        print("  <member>       - Inspect a member of the current object")
        print("  back           - Go back to the previous object")
        print("  history        - Show navigation history")
        print("\nDocumentation:")
        print("  help <member>  - Show detailed help for a member")
        print("  source <member>- Show source code for a member")
        print("  search <term>  - Search members by name or docs")
        # ... rest of help menu

    # The rest of the methods (show_bookmarks, install_module, etc.) are omitted for brevity
    # but are assumed to be present and correct from your original code. I will add them back
    # for completeness in the final block.
    
    def show_builtins(self) -> None:
        """Show Python built-in functions."""
        print(f"\n{self.color_text('=== Python Built-ins ===', 'header')}")
        
        builtin_funcs = sorted([name for name in dir(__builtins__) if not name.startswith('_') and callable(getattr(__builtins__, name))])
        
        cols = 4
        col_width = 20
        rows = (len(builtin_funcs) + cols - 1) // cols
        
        for i in range(rows):
            row_items = []
            for j in range(cols):
                index = i + j * rows
                if index < len(builtin_funcs):
                    row_items.append(self.color_text(builtin_funcs[index].ljust(col_width), 'blue'))
            print(' '.join(row_items))
        
        print("\nType a built-in name (e.g. 'len') to get help.")

    def install_module(self, module_name: str) -> None:
        """Guide for installing missing modules."""
        print(f"\n{self.color_text('=== Module Installation ===', 'header')}")
        print(f"To install '{module_name}', you can typically run one of these in your terminal:")
        print(self.color_text(f"  pip install {module_name}", 'cyan'))
        print(self.color_text(f"  python -m pip install {module_name}", 'cyan'))

    def bookmark_location(self, name: str) -> None:
        """Bookmark the current location."""
        if not self.current_path:
            print(self.color_text("No current location to bookmark.", 'yellow'))
            return
            
        self.bookmarks[name].append((self.current_path, self.current_object))
        print(self.color_text(f"Bookmarked '{self.current_path}' as '{name}'", 'green'))

    def goto_bookmark(self, name: str) -> None:
        """Navigate to a bookmarked location."""
        if name not in self.bookmarks or not self.bookmarks[name]:
            print(self.color_text(f"No bookmark found with name '{name}'.", 'yellow'))
            return
            
        path, obj = self.bookmarks[name][-1]
        self.current_path = path
        self.current_object = obj
        self.display_members(obj, path)

    def show_bookmarks(self) -> None:
        """Show all bookmarks."""
        if not self.bookmarks:
            print(self.color_text("No bookmarks saved.", 'yellow'))
            return
            
        print(f"\n{self.color_text('=== Bookmarks ===', 'header')}")
        for name, locations in self.bookmarks.items():
            print(f"  {self.color_text(name, 'blue')}:")
            # Show up to 3 most recent for this bookmark name
            for path, _ in locations[-3:]:
                print(f"    - {path}")
                
    def show_source(self, member_name: str) -> None:
        """Show source code for a member."""
        if not hasattr(self.current_object, member_name):
            print(self.color_text(f"Member '{member_name}' not found.", 'red'))
            return
            
        member_obj = getattr(self.current_object, member_name)
        source = self.get_source_code(member_obj)
        
        if source:
            print(f"\n{self.color_text('=== Source for:', 'header')} {self.color_text(f'{self.current_path}.{member_name}', 'cyan')}\n")
            print(self.color_text(source, 'yellow'))
        else:
            print(self.color_text(f"No source code available for {member_name}", 'red'))


def main():
    explorer = LibraryExplorer()
    explorer.interactive_loop()

if __name__ == "__main__":
    main()
