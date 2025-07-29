#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime
from difflib import ndiff

__version__ = "0.1.0"

class Mojito:
    def __init__(self):
        self.divider = "│"
        self.change_marker = "~>"
        self.add_marker = "+"
        self.remove_marker = "-"
        self.terminal_width = self._get_terminal_width()
        self.last_file_size = 0

    def _get_terminal_width(self):
        try:
            if os.name == 'posix':
                import fcntl, termios, struct
                fd = sys.stdout.fileno()
                return struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))[1]
            elif os.name == 'nt':
                from ctypes import windll, create_string_buffer
                h = windll.kernel32.GetStdHandle(-12)
                csbi = create_string_buffer(22)
                windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
                return (csbi[0] + csbi[2] << 8) - (csbi[0] & 0xff)
        except:
            return 80

    def _calculate_widths(self, before, after):
        max_left = max(len(line) for line in before) if before else 20
        max_right = max(len(line) for line in after) if after else 20
        available = max(self.terminal_width - 7, 40)
        left = min(max_left, available // 2)
        right = min(max_right, available - left - 3)
        return left, right

    def _colorize(self, text, color):
        if not sys.stdout.isatty() or os.name == 'nt' and 'ANSICON' not in os.environ:
            return text
        colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'reset': '\033[0m'
        }
        return f"{colors[color]}{text}{colors['reset']}"

    def show_diff(self, before, after, use_colors=True, show_timestamps=True):
        left_width, right_width = self._calculate_widths(before, after)
        separator = "─" * left_width + "┼" + "─" * right_width
        
        print(f"{'BEFORE'.ljust(left_width)} {self.divider} {'AFTER'.ljust(right_width)}")
        print(separator)

        diff = list(ndiff(before, after))
        i = 0
        
        while i < len(diff):
            line = diff[i]
            timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] " if show_timestamps else ""
            
            if line.startswith('  '):
                content = line[2:]
                print(f"{timestamp}{content[:left_width].ljust(left_width)} {self.divider} {content[:right_width].ljust(right_width)}")
                i += 1
                
            elif line.startswith('- '):
                removed = line[2:]
                if i+1 < len(diff) and diff[i+1].startswith('+ '):
                    added = diff[i+1][2:]
                    marker = self._colorize(self.change_marker, 'yellow') if use_colors else self.change_marker
                    print(f"{timestamp}{removed[:left_width].ljust(left_width)} {marker} {added[:right_width].ljust(right_width)}")
                    i += 2
                else:
                    marker = self._colorize(self.remove_marker, 'red') if use_colors else self.remove_marker
                    print(f"{timestamp}{removed[:left_width].ljust(left_width)} {marker} {' ' * right_width}")
                    i += 1
                    
            elif line.startswith('+ '):
                added = line[2:]
                marker = self._colorize(self.add_marker, 'green') if use_colors else self.add_marker
                print(f"{timestamp}{' ' * left_width} {marker} {added[:right_width].ljust(right_width)}")
                i += 1

        print(separator)

    def _read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return [line.rstrip('\n') for line in f.readlines()]
        except UnicodeDecodeError:
            try:
                with open(path, 'r', encoding='latin-1') as f:
                    return [line.rstrip('\n') for line in f.readlines()]
            except Exception as e:
                print(f"Error reading file: {str(e)}", file=sys.stderr)
                return []
        except Exception as e:
            print(f"Error reading file: {str(e)}", file=sys.stderr)
            return []

    def watch_file(self, path, interval=1, use_colors=True, show_timestamps=True):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        last_content = self._read_file(path)
        print(f"\n🍹 Mojito v{__version__} watching '{path}' (Ctrl+C to stop)\n")
        self.show_diff([], last_content, use_colors, False)

        try:
            while True:
                try:
                    current_content = self._read_file(path)
                    if current_content != last_content:
                        self.show_diff(last_content, current_content, use_colors, show_timestamps)
                        last_content = current_content
                    time.sleep(interval)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"\n⚠️  Error: {str(e)}", file=sys.stderr)
                    time.sleep(2)
        except KeyboardInterrupt:
            print("\nClosing time! 🍹")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🍹 Mojito - A beautifully simple, zero dependency, fresh file monitoring tool. Monitor file changes in real time with ease using Mojito🍹!",
        epilog="Example: mojito test.txt 0.5 --no-color"
    )
    parser.add_argument('file', help="File to watch")
    parser.add_argument('interval', nargs='?', type=float, default=1.0,
                      help="Polling interval in seconds (default: 1.0)")
    parser.add_argument('--no-color', action='store_false', dest='colors',
                      help="Disable colored output")
    parser.add_argument('--no-timestamps', action='store_false', dest='timestamps',
                      help="Disable change timestamps")
    parser.add_argument('-v', '--version', action='version', 
                      version=f"%(prog)s {__version__}",
                      help="Show version and exit")

    args = parser.parse_args()
    
    watcher = Mojito()
    try:
        watcher.watch_file(
            path=args.file,
            interval=args.interval,
            use_colors=args.colors,
            show_timestamps=args.timestamps
        )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()