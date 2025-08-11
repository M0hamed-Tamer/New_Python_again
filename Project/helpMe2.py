import importlib
import inspect
import io
import sys
from textwrap import wrap
from typing import Any, Dict, List, Tuple, Optional

class LibraryExplorer:
    """
    An interactive tool to explore Python libraries, modules, and objects with detailed documentation.
    Features include:
    - Module/object inspection
    - Categorized member listing
    - Detailed help viewing
    - Search functionality
    - Navigation history
    - Color output
    """
    
    def __init__(self):
        self.history = []
        self.current_object = None
        self.current_path = ""
        
        # ANSI color codes
        self.COLORS = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'bold': '\033[1m',
            'underline': '\033[4m',
            'end': '\033[0m'
        }

    def color_text(self, text: str, color: str) -> str:
        """Return colored text using ANSI codes."""
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['end']}"

    def get_help_text(self, obj: Any) -> str:
        """Capture the output of help() for an object."""
        help_output = io.StringIO()
        sys.stdout = help_output
        try:
            help(obj)
        except Exception as e:
            sys.stdout = sys.__stdout__
            return f"{self.color_text('Error getting help:', 'red')}\n{str(e)}"
        finally:
            sys.stdout = sys.__stdout__
        return help_output.getvalue()

    def short_doc(self, obj: Any) -> str:
        """Get a shortened version of an object's docstring."""
        doc = inspect.getdoc(obj)
        if not doc:
            return self.color_text("No description available.", 'yellow')
        
        # Clean up docstring and get first meaningful line
        lines = [line.strip() for line in doc.split('\n') if line.strip()]
        if not lines:
            return self.color_text("No description available.", 'yellow')
        
        first_line = lines[0]
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."
        return first_line

    def classify_members(self, obj: Any) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]], List[Tuple[str, str]]]:
        """Categorize members of an object into functions, classes, and attributes."""
        members = inspect.getmembers(obj)
        functions = []
        classes = []
        attributes = []

        for name, member in members:
            if name.startswith("_"):
                continue  # Skip private members
            
            try:
                if inspect.isfunction(member) or inspect.isbuiltin(member):
                    functions.append((name, self.short_doc(member)))
                elif inspect.ismethoddescriptor(member) or inspect.isbuiltin(member):
                    functions.append((name, self.short_doc(member)))
                elif inspect.isclass(member):
                    classes.append((name, self.short_doc(member)))
                elif inspect.ismodule(member):
                    # Skip submodules to keep output clean
                    continue
                else:
                    if not callable(member):
                        attributes.append((name, self.short_doc(member)))
            except Exception:
                # Skip problematic members
                continue

        # Sort each category alphabetically
        functions.sort(key=lambda x: x[0])
        classes.sort(key=lambda x: x[0])
        attributes.sort(key=lambda x: x[0])

        return functions, classes, attributes

    def load_object(self, path: str) -> Optional[Any]:
        """Load a module or object from a dotted path."""
        parts = path.split('.')
        try:
            obj = importlib.import_module(parts[0])
            self.history.append((self.current_path, self.current_object))
            
            for attr in parts[1:]:
                obj = getattr(obj, attr)
            
            self.current_object = obj
            self.current_path = path
            return obj
        except (ModuleNotFoundError, AttributeError) as e:
            print(self.color_text(f"\nError: {str(e)}", 'red'))
            return None

    def display_members(self, obj: Any, obj_path: str) -> None:
        """Display categorized members of an object with formatting."""
        print(f"\n{self.color_text('=== Exploring:', 'header')} {self.color_text(obj_path, 'cyan')}\n")
        
        try:
            functions, classes, attributes = self.classify_members(obj)
        except Exception as e:
            print(self.color_text(f"Could not inspect members: {e}", 'red'))
            return

        # Display counts
        print(self.color_text(f"Members: {len(functions)} functions, {len(classes)} classes, {len(attributes)} attributes\n", 'bold'))

        if functions:
            print(self.color_text("Functions:", 'green'))
            for name, desc in functions:
                print(f"  {self.color_text(name, 'blue')}: {desc}")

        if classes:
            print(self.color_text("\nClasses:", 'green'))
            for name, desc in classes:
                print(f"  {self.color_text(name, 'blue')}: {desc}")

        if attributes:
            print(self.color_text("\nAttributes:", 'green'))
            for name, desc in attributes:
                print(f"  {self.color_text(name, 'blue')}: {desc}")

    def show_help(self, member_name: str) -> None:
        """Show detailed help for a member."""
        if not hasattr(self.current_object, member_name):
            print(self.color_text(f"Member '{member_name}' not found.", 'red'))
            return
            
        member_obj = getattr(self.current_object, member_name)
        print(f"\n{self.color_text('=== Help for:', 'header')} {self.color_text(f'{self.current_path}.{member_name}', 'cyan')}\n")
        
        # Show signature if available
        try:
            sig = str(inspect.signature(member_obj))
            print(self.color_text("Signature:", 'green'))
            print(f"  {sig}\n")
        except (ValueError, TypeError):
            pass
        
        # Show full help
        print(self.color_text("Documentation:", 'green'))
        help_text = self.get_help_text(member_obj)
        print(help_text if help_text else self.color_text("No documentation available.", 'yellow'))

    def search_members(self, query: str) -> None:
        """Search members of the current object."""
        if not self.current_object:
            print(self.color_text("No object loaded to search.", 'yellow'))
            return
            
        functions, classes, attributes = self.classify_members(self.current_object)
        all_members = functions + classes + attributes
        results = [(name, desc) for name, desc in all_members if query.lower() in name.lower() or query.lower() in desc.lower()]
        
        if not results:
            print(self.color_text(f"No members found matching '{query}'.", 'yellow'))
            return
            
        print(f"\n{self.color_text('Search results:', 'header')} {len(results)} matches for '{query}'\n")
        for name, desc in results:
            print(f"  {self.color_text(name, 'blue')}: {desc}")

    def go_back(self) -> bool:
        """Navigate back in history."""
        if not self.history:
            print(self.color_text("No history to go back to.", 'yellow'))
            return False
            
        self.current_path, self.current_object = self.history.pop()
        return True

    def show_history(self) -> None:
        """Display navigation history."""
        if not self.history:
            print(self.color_text("No navigation history.", 'yellow'))
            return
            
        print(self.color_text("\nNavigation History:", 'header'))
        for i, (path, _) in enumerate(reversed(self.history), 1):
            print(f"  {i}. {path}")
        print(f"  Current: {self.current_path}")

    def interactive_loop(self) -> None:
        """Main interactive loop."""
        print(self.color_text("\n=== Python Library & Object Explorer ===", 'header'))
        print("Enter library/module/object paths to explore")
        print("Special commands: back, history, search, exit\n")

        while True:
            try:
                if not self.current_object:
                    path = input("Enter path to explore (e.g., 'os.path'): ").strip()
                    if path.lower() == 'exit':
                        break
                    if not path:
                        continue
                        
                    obj = self.load_object(path)
                    if obj is None:
                        continue
                    self.display_members(obj, path)
                else:
                    cmd = input(f"\n{self.current_path}> ").strip()
                    
                    if not cmd:
                        continue
                    elif cmd.lower() == 'exit':
                        break
                    elif cmd.lower() == 'back':
                        if self.go_back():
                            self.display_members(self.current_object, self.current_path)
                        continue
                    elif cmd.lower() == 'history':
                        self.show_history()
                        continue
                    elif cmd.lower().startswith('search '):
                        query = cmd[7:].strip()
                        if query:
                            self.search_members(query)
                        continue
                    elif cmd.lower() == 'help':
                        self.display_members(self.current_object, self.current_path)
                        print("\nAvailable commands:")
                        print("  <member_name> - Show help for member")
                        print("  back          - Go back to previous object")
                        print("  history       - Show navigation history")
                        print("  search <term> - Search members")
                        print("  exit          - Quit the explorer")
                        continue
                        
                    # Check if it's a member name
                    if hasattr(self.current_object, cmd):
                        self.show_help(cmd)
                    else:
                        # Try to navigate to sub-object
                        new_path = f"{self.current_path}.{cmd}"
                        obj = self.load_object(new_path)
                        if obj is not None:
                            self.display_members(obj, new_path)
                        else:
                            print(self.color_text(f"'{cmd}' is not a valid member or command.", 'red'))
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit or 'back' to go up.")
            except Exception as e:
                print(self.color_text(f"\nError: {str(e)}", 'red'))

        print(self.color_text("\nGoodbye!", 'header'))

def main():
    explorer = LibraryExplorer()
    explorer.interactive_loop()

if __name__ == "__main__":
    main()