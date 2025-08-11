import importlib
import inspect
import io
import sys
import pydoc
from textwrap import wrap
from typing import Any, List, Tuple, Optional
import keyword
from collections import defaultdict
import os
import ast
import json
import readline  # For autocomplete in Unix terminals
import re
from difflib import get_close_matches

class LibraryExplorerPro:
    """
    LibraryExplorer Pro:
    - Interactive Python library & object inspector
    - Autocomplete for commands and module paths
    - Search with regex support
    - Organized tabular display for members
    - Save/load session (history + bookmarks)
    - Colored output by type
    """
    def __init__(self):
        self.history: List[Tuple[str, Any]] = []
        self.current_object: Optional[Any] = None
        self.current_path: str = ""
        self.bookmarks = defaultdict(list)
        self.session_file = "explorer_session.json"
        self.config = {
            'max_history': 50,
            'search_limit': 20,
            'display_width': 90,
        }
        self.aliases = {
            '?': 'help',
            '??': 'source',
            'ls': 'members',
            'cd': 'back',
            'q': 'exit',
        }
        self.commands = [
            'help', 'exit', 'back', 'history', 'search', 'source', 'members',
            'builtins', 'install', 'bookmark', 'goto', 'exec', 'deps', 'clear',
        ]
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
            'gray': '\033[90m',
            'end': '\033[0m',
        }
        self._setup_readline()
        self.load_session()

    def _setup_readline(self):
        # Enable tab completion for commands and modules
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self._autocomplete)

    def _autocomplete(self, text, state):
        buffer = readline.get_line_buffer()
        line = buffer.lstrip()
        split_line = line.split()
        # If first word, autocomplete commands and module names
        if len(split_line) == 0 or (len(split_line) == 1 and not buffer.endswith(' ')):
            options = [cmd for cmd in self.commands + list(self.aliases.keys()) if cmd.startswith(text)]
        else:
            # Autocomplete members of current object or module path
            options = []
            try:
                if self.current_object:
                    for name, _ in self.classify_members(self.current_object)[0] + self.classify_members(self.current_object)[1] + self.classify_members(self.current_object)[2]:
                        if name.startswith(text):
                            options.append(name)
                else:
                    # Autocomplete top-level modules matching text
                    import pkgutil
                    for _, modname, _ in pkgutil.iter_modules():
                        if modname.startswith(text):
                            options.append(modname)
            except Exception:
                pass
        if state < len(options):
            return options[state]
        else:
            return None

    def color_text(self, text: str, color: str) -> str:
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['end']}"

    def save_session(self):
        try:
            data = {
                'history': [(path, None) for path, _ in self.history],
                'bookmarks': {k: [(path, None, ts) for path, _, ts in v] for k, v in self.bookmarks.items()},
                'current_path': self.current_path,
            }
            with open(self.session_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(self.color_text(f"Error saving session: {e}", 'red'))

    def load_session(self):
        if not os.path.exists(self.session_file):
            return
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)
            self.history = [(path, None) for path, _ in data.get('history', [])]
            # Bookmarks only keep path & timestamp
            self.bookmarks = defaultdict(list)
            for k, v in data.get('bookmarks', {}).items():
                for entry in v:
                    self.bookmarks[k].append((entry[0], None, entry[2]))
            self.current_path = data.get('current_path', '')
            if self.current_path:
                self.load_object(self.current_path)
        except Exception as e:
            print(self.color_text(f"Error loading session: {e}", 'red'))

    def get_help_text(self, obj: Any) -> str:
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
        try:
            return inspect.getsource(obj)
        except (TypeError, OSError):
            return None
        except Exception as e:
            return f"{self.color_text('Error getting source:', 'red')}\n{str(e)}"

    def short_doc(self, obj: Any) -> str:
        doc = inspect.getdoc(obj)
        if not doc:
            return self.color_text("No docstring", 'yellow')
        first_line = doc.strip().split('\n')[0]
        return first_line if len(first_line) <= 80 else first_line[:77] + "..."

    def classify_members(self, obj: Any) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]], List[Tuple[str, str]]]:
        try:
            members = inspect.getmembers(obj)
        except Exception:
            return [], [], []
        funcs, classes, attrs = [], [], []
        for name, mem in members:
            if name.startswith("_") or keyword.iskeyword(name):
                continue
            try:
                if inspect.isclass(mem):
                    classes.append((name, self.short_doc(mem)))
                elif callable(mem):
                    funcs.append((name, self.short_doc(mem)))
                elif not inspect.ismodule(mem):
                    val = repr(mem)
                    if len(val) > 50:
                        val = val[:47] + "..."
                    attrs.append((name, f"{type(mem).__name__}: {val}"))
            except Exception:
                continue
        funcs.sort(key=lambda x: x[0].lower())
        classes.sort(key=lambda x: x[0].lower())
        attrs.sort(key=lambda x: x[0].lower())
        return funcs, classes, attrs

    def load_object(self, path: str) -> Optional[Any]:
        try:
            parts = path.split('.')
            obj = importlib.import_module(parts[0])
            for attr in parts[1:]:
                if not hasattr(obj, attr):
                    close = get_close_matches(attr, [m[0] for m in inspect.getmembers(obj)], n=3, cutoff=0.6)
                    sugg = f" Did you mean: {', '.join(close)}?" if close else ""
                    raise AttributeError(f"'{type(obj).__name__}' has no attribute '{attr}'.{sugg}")
                obj = getattr(obj, attr)
        except (ModuleNotFoundError, AttributeError) as e:
            # Builtins fallback
            if hasattr(__builtins__, path):
                obj = getattr(__builtins__, path)
                self.current_path = path
                self.current_object = obj
                self.show_help(path, is_builtin=True)
                return None
            print(self.color_text(f"Error: {str(e)}", 'red'))
            if isinstance(e, ModuleNotFoundError):
                print("Tip: use 'install <module>' to install missing modules.")
            return None
        except Exception as e:
            print(self.color_text(f"Unexpected error: {str(e)}", 'red'))
            return None
        if not self.history or self.history[-1][0] != path:
            self.history.append((self.current_path, self.current_object))
            if len(self.history) > self.config['max_history']:
                self.history.pop(0)
        self.current_path = path
        self.current_object = obj
        return obj

    def display_members(self, obj: Any, path: str) -> None:
        from math import ceil
        print(f"\n{self.color_text('=== Exploring:', 'header')} {self.color_text(path, 'cyan')}")
        print(f"{self.color_text('Type:', 'green')} {type(obj).__name__}")
        if hasattr(obj, '__file__'):
            print(f"{self.color_text('Location:', 'green')} {getattr(obj, '__file__')}")
        doc = inspect.getdoc(obj)
        if doc:
            print(f"\n{self.color_text('Description:', 'green')}")
            print('\n'.join(wrap(doc, width=self.config['display_width'])))
        funcs, classes, attrs = self.classify_members(obj)
        print(self.color_text(f"\nMembers ({len(funcs)} functions, {len(classes)} classes, {len(attrs)} attributes):", 'bold'))
        
        def print_table(items: List[Tuple[str, str]], color_name: str):
            if not items:
                return
            print(self.color_text(f"\n{color_name}:", 'green'))
            cols = 3
            col_width = self.config['display_width'] // cols
            rows = ceil(len(items) / cols)
            table = [[] for _ in range(rows)]
            for i, (name, desc) in enumerate(items):
                table[i % rows].append(f"{self.color_text(name, 'blue')}: {desc}")
            for row in table:
                print(" | ".join(cell.ljust(col_width) for cell in row))
        
        print_table(classes, 'Classes')
        print_table(funcs, 'Functions')
        print_table(attrs, 'Attributes')

    def show_help(self, member_name: str, is_builtin: bool = False) -> None:
        if is_builtin:
            member_obj = getattr(__builtins__, member_name)
            full_path = member_name
        elif self.current_object and hasattr(self.current_object, member_name):
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
        try:
            if hasattr(member_obj, '__annotations__') and member_obj.__annotations__:
                print(f"{self.color_text('Type hints:', 'green')}")
                for k, v in member_obj.__annotations__.items():
                    print(f"  {k}: {v.__name__ if hasattr(v, '__name__') else str(v)}")
        except Exception:
            pass
        source = self.get_source_code(member_obj)
        if source:
            print(f"\n{self.color_text('Source Code:', 'green')}\n{self.color_text(source, 'yellow')}")
        print(f"\n{self.color_text('Documentation:', 'green')}")
        help_text = self.get_help_text(member_obj)
        print(help_text if help_text.strip() else self.color_text("No documentation available.", 'yellow'))

    def search_members(self, query: str) -> None:
        if not self.current_object:
            print(self.color_text("No object loaded to search.", 'yellow'))
            return
        funcs, classes, attrs = self.classify_members(self.current_object)
        all_members = funcs + classes + attrs

        # Regex search support
        try:
            pattern = re.compile(query, re.IGNORECASE)
            results = [m for m in all_members if pattern.search(m[0]) or pattern.search(m[1])]
        except re.error:
            # Fallback to substring if regex invalid
            results = [m for m in all_members if query.lower() in m[0].lower() or query.lower() in m[1].lower()]
        
        if not results:
            print(self.color_text(f"No members found matching '{query}'.", 'yellow'))
            return
        print(f"\n{self.color_text('Search results:', 'header')} {len(results)} matches for '{query}'\n")
        limit = self.config['search_limit']
        for name, desc in results[:limit]:
            print(f"  {self.color_text(name, 'blue')}: {desc}")
        if len(results) > limit:
            print(self.color_text(f"\nShowing first {limit} results. Narrow your search.", 'gray'))

    def go_back(self) -> bool:
        if not self.history:
            print(self.color_text("No history to go back to.", 'yellow'))
            return False
        self.current_path, self.current_object = self.history.pop()
        if self.current_object is None:
            self.current_path = ""
        print(self.color_text("Navigated back.", 'magenta'))
        return True

    def show_history(self) -> None:
        if not self.history:
            print(self.color_text("History is empty.", 'yellow'))
            return
        print(f"\n{self.color_text('=== Navigation History ===', 'header')}")
        for i, (path, _) in enumerate(reversed(self.history), 1):
            if path:
                print(f"  {i}. {path}")
        print(f"Current: {self.current_path}")

    def show_builtins(self) -> None:
        print(f"\n{self.color_text('=== Python Built-ins ===', 'header')}")
        builtins = [n for n in dir(__builtins__) if not n.startswith('_')]
        categories = {'Functions': [], 'Types': [], 'Constants': [], 'Other': []}
        for name in builtins:
            obj = getattr(__builtins__, name)
            if callable(obj):
                if inspect.isclass(obj):
                    categories['Types'].append(name)
                else:
                    categories['Functions'].append(name)
            elif name.isupper():
                categories['Constants'].append(name)
            else:
                categories['Other'].append(name)
        for cat, items in categories.items():
            if items:
                print(f"\n{self.color_text(cat+':', 'green')}")
                items.sort()
                print("  " + ", ".join(self.color_text(i, 'blue') for i in items))
        print("\nType a built-in name (e.g. 'len') to get help.")

    def install_module(self, module_name: str) -> None:
        print(f"\n{self.color_text('=== Module Installation ===', 'header')}")
        print(f"To install '{module_name}', run one of these commands:")
        print(self.color_text(f"  pip install {module_name}", 'cyan'))
        print(self.color_text(f"  python -m pip install {module_name}", 'cyan'))
        print("\nFor specific versions or development versions:")
        print(self.color_text(f"  pip install {module_name}==version", 'cyan'))
        print(self.color_text(f"  pip install git+https://repo.url/{module_name}.git", 'cyan'))

    def bookmark_location(self, name: str) -> None:
        if not self.current_path:
            print(self.color_text("No current location to bookmark.", 'yellow'))
            return
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bookmarks[name].append((self.current_path, self.current_object, timestamp))
        print(self.color_text(f"Bookmarked '{self.current_path}' as '{name}' at {timestamp}", 'green'))
        self.save_session()

    def goto_bookmark(self, name: str) -> None:
        if name not in self.bookmarks or not self.bookmarks[name]:
            print(self.color_text(f"No bookmark named '{name}'.", 'yellow'))
            return
        path, obj, timestamp = self.bookmarks[name][-1]
        self.history.append((self.current_path, self.current_object))
        self.current_path = path
        self.current_object = obj
        print(self.color_text(f"Navigated to bookmark '{name}' (created {timestamp})", 'magenta'))
        self.display_members(obj, path)

    def show_bookmarks(self) -> None:
        if not self.bookmarks:
            print(self.color_text("No bookmarks saved.", 'yellow'))
            return
        print(f"\n{self.color_text('=== Bookmarks ===', 'header')}")
        for name, locs in sorted(self.bookmarks.items()):
            print(f"  {self.color_text(name, 'blue')}:")
            for path, _, timestamp in locs[-3:]:
                print(f"    - {path} ({timestamp})")

    def execute_code(self, code: str) -> None:
        if not self.current_object:
            print(self.color_text("No object loaded for execution.", 'yellow'))
            return
        try:
            ctx = {k: v for k, v in vars(self.current_object).items() if not k.startswith('_') and not inspect.ismodule(v)}
            ctx['self'] = self.current_object
            ctx['explorer'] = self
            ctx['current'] = self.current_object
            ctx['path'] = self.current_path
            print(self.color_text(f"Executing code in context of {self.current_path}:", 'magenta'))
            exec(code, ctx)
        except Exception as e:
            print(self.color_text(f"Error executing code: {e}", 'red'))

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_dependencies(self) -> None:
        if not self.current_object or not hasattr(self.current_object, '__file__'):
            print(self.color_text("Cannot show dependencies - not a module or no file.", 'yellow'))
            return
        try:
            import pkg_resources
            import importlib.util
            spec = importlib.util.find_spec(self.current_object.__name__)
            if not spec or not spec.origin:
                print(self.color_text("Could not determine package.", 'yellow'))
                return
            top_package = self.current_object.__name__.split('.')[0]
            dist = pkg_resources.get_distribution(top_package)


            print(f"Package: {dist.project_name} Version: {dist.version}")
        except Exception as e:
            print(self.color_text(f"Error getting dependencies: {e}", 'red'))