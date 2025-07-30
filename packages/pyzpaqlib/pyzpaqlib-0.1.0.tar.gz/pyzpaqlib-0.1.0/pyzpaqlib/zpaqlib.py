import subprocess
import shutil
import re
from dataclasses import dataclass
from datetime import datetime
import glob
import os

try:
    import importlib.resources as importlib_resources
except ImportError:
    import importlib_resources


@dataclass
class FileInfo:
    filename: str
    size: int
    mtime: datetime
    status: str | None = None
    attributes: str | None = None


class ZpaqError(Exception):
    """Custom exception for errors during zpaq execution"""
    
    def __init__(self, message, exit_code=None, stderr_output=None, command=None):
        """
        Initialize ZpaqError
        
        Args:
            message (str): Error message
            exit_code (int, optional): Exit code of the zpaq process
            stderr_output (str, optional): Error output from stderr
            command (list, optional): The zpaq command that was executed
        """
        super().__init__(message)
        self.exit_code = exit_code
        self.stderr_output = stderr_output
        self.command = command
    
    def __str__(self):
        """String representation including error details"""
        parts = [super().__str__()]
        
        if self.exit_code is not None:
            parts.append(f"Exit code: {self.exit_code}")
        
        if self.stderr_output:
            parts.append(f"stderr: {self.stderr_output}")
        
        if self.command:
            parts.append(f"Command: {' '.join(self.command)}")
        
        return " | ".join(parts)
    
    def __repr__(self):
        """Debug string representation"""
        return f"ZpaqError(message='{super().__str__()}', exit_code={self.exit_code}, command={self.command})"

class Zpaq:
    def __init__(self, zpaq_executable_path=None, use_64bit=True):
        """
        Args:
            zpaq_executable_path (str, optional): Path or name of the zpaq executable to use. If None, it will be searched automatically.
            use_64bit (bool, optional): If True, prioritize 64-bit (zpaq64.exe), if False, prioritize 32-bit (zpaq.exe). Default is True.
        """
        exe_candidates = []
        exe_order = ["zpaq64.exe", "zpaq.exe"] if use_64bit else ["zpaq.exe", "zpaq64.exe"]
        if zpaq_executable_path:
            exe_candidates.append(zpaq_executable_path)
        for exe_name in exe_order:
            try:
                with importlib_resources.path(__package__ or __name__.split(".")[0], f"bin/{exe_name}") as p:
                    exe_candidates.append(str(p))
            except (FileNotFoundError, ModuleNotFoundError):
                pass
            except Exception as e:
                print(f"Warning: Unexpected error while searching for {exe_name}: {e}")
        for exe_name in exe_order:
            found = shutil.which(exe_name)
            if found:
                exe_candidates.append(found)
        for candidate in exe_candidates:
            if os.path.isfile(candidate):
                self.zpaq_path = candidate
                break
        else:
            raise FileNotFoundError(f"Could not find zpaq executable in package or PATH: {exe_candidates}")

    def _build_command(self, command, archive, files=None, **options):
        """Helper method to build the zpaq command"""
        cmd = [self.zpaq_path, command, archive]

        if files:
            if not isinstance(files, list):
                files = [files]
            
            expanded_files = []
            for file_pattern in files:
                if any(c in file_pattern for c in '*?['):
                    matches = glob.glob(file_pattern, recursive=True)
                    expanded_files.extend(matches)
                else:
                    expanded_files.append(file_pattern)

            cmd.extend(expanded_files)
        
        for key, value in options.items():
            if value is None or value is False:
                continue

            # Handle special option names that need exact formatting
            if key == 'noattributes':
                option = "-noattributes"
            elif key == 'not':
                option = "-not"
            elif key == 'only': 
                option = "-only"
            elif key == 'all':
                option = "-all"
            elif key == 'force':
                option = "-force"
            elif key == 'test':
                option = "-test"
            elif key == 'method':
                option = f"-m{value}"
                cmd.append(option)
                continue
            elif key == 'summary':
                option = f"-s{value}"
                cmd.append(option)
                continue
            elif key == 'threads':
                option = f"-t{value}"
                cmd.append(option)
                continue
            else:
                # Handle other options by removing underscores
                option = f"-{key.replace('_', '')}"
            
            cmd.append(option)
            
            # Add option value if it's not a boolean flag
            if not isinstance(value, bool):
                if isinstance(value, list):
                    cmd.extend(map(str, value))
                else:
                    cmd.append(str(value))
        return cmd

    def _execute(self, cmd, progress_callback=None):
        """Helper method to execute the command and return the result"""
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                bufsize=1,
                shell=False
            )

            stdout_lines = []
            if progress_callback:
                for line in iter(process.stdout.readline, ''):
                    line = line.strip()
                    stdout_lines.append(line)
                    progress_callback(line)
                process.stdout.close()
                stderr_output = process.stderr.read()
                process.wait()
            else:
                stdout_output, stderr_output = process.communicate()
                stdout_lines = stdout_output.strip().split('\n') if stdout_output else []

            if process.returncode != 0:
                raise ZpaqError(
                    f"zpaq execution failed",
                    exit_code=process.returncode,
                    stderr_output=stderr_output,
                    command=cmd
                )
            return stdout_lines
        except FileNotFoundError:            
            raise ZpaqError(
                f"Cannot execute '{self.zpaq_path}'. Please check the path.",
                command=cmd
            )
        except ZpaqError:
            raise
        except Exception as e:
            raise ZpaqError(
                f"Unexpected error occurred: {str(e)}",
                command=cmd
            )


    def add(self, archive, files, key=None, method=1, force=False, index=None, progress_callback=None, **kwargs):
        """
        Adds or updates files in the archive.

        Args:
            archive (str): Path to the archive file.
            files (str or list): List of files or directories to add.
            key (str, optional): Password to create or access an encrypted archive. Default is None.
            method (int, optional): Compression level (0=fastest, 5=best). Default is 1.
            force (bool, optional): Add files if their contents have changed. Default is False.
            index (str, optional): Create and update an index file F for the archive. Default is None.
            progress_callback (callable, optional): Callback function for real-time progress. Default is None.            **kwargs: Other options available for the zpaq 'add' command.
                summary (int): If greater than 0, show brief progress. (s + number, e.g., s1, s2)
                threads (int): Number of threads to use. (t + number, e.g., t4 for 4 threads. Default: 0 = auto detection)
                until (str or int): Roll back the archive to the specified date or version before adding. 
                    Date format: "YYYY-MM-DD HH:MM:SS" (e.g., "2025-06-19 01:30:45")
                    Version: integer (e.g., 3 for 3rd update, -1 for last update)
                to (str or list): Store external files in the archive under a different name.
                noattributes (bool): Don't save file attributes or permissions.
                not (str or list): Exclude files matching the specified pattern(s). e.g., "*.tmp" or ["*.tmp", "*.log", "*.bak"]
                only (str or list): Include only files matching the specified pattern(s). Default is "*". e.g., "*.txt" or ["*.txt", "*.doc"]
        """
        options = {'key': key, 'method': method, 'force': force, 'index': index, **kwargs}
        cmd = self._build_command('a', archive, files, **options)
        self._execute(cmd, progress_callback)


    def extract(self, archive, files=None, key=None, force=False, to=None, test=False, index=None, progress_callback=None, **kwargs):
        """
        Extracts the latest version of files from the archive.

        Args:
            archive (str): Path to the archive file.
            files (str or list, optional): Specific files or directories to extract. If not specified, extract all. Default is None.
            key (str, optional): Password to access an encrypted archive. Default is None.
            force (bool, optional): Overwrite existing files when extracting. Default is False.
            to (str or list, optional): Extract files to a different name or location. Default is None.
            test (bool, optional): Test extraction without writing files to disk to verify data integrity. Default is False.
            index (str, optional): Create an index file F for the archive. Default is None.
            progress_callback (callable, optional): Callback function for real-time progress. Default is None.            **kwargs: Other options available for the zpaq 'extract' command.
                all (int, optional): Extract all versions of files into N-digit directories [default 4].
                summary (int): If greater than 0, show brief progress. (s + number)
                until (str or int): Extract files as of the specified date or version.
                    Date format: "YYYY-MM-DD HH:MM:SS" (e.g., "2025-06-19 01:30:45")
                repack (str): Extract to new archive with optional key (format: "filename [key]").
                threads (int): Number of threads to use. (t + number. Default: 0 = auto detection)
                noattributes (bool): Ignore/don't restore file attributes or permissions.
                not (str or list): Exclude files matching the specified pattern(s).
                only (str or list): Include only files matching the specified pattern(s).
        """
        options = {'key': key, 'force': force, 'to': to, 'test': test, 'index': index, **kwargs}
        cmd = self._build_command('x', archive, files, **options)
        self._execute(cmd, progress_callback)


    def list(self, archive, files=None, key=None, all=False, summary=None, **kwargs):
        """
        Shows the contents of the archive or compares with external files.

        Args:
            archive (str): Path to the archive file.
            files (str or list, optional): Specific files or directories to list. Default is None.
            key (str, optional): Password to access an encrypted archive. Default is None.
            all (bool, optional): Show all stored versions, including deleted files, not just the latest. Default is False.
            summary (int, optional): Show only the top N files/directories by size. -1 shows fragment IDs. Default is None.            **kwargs: Other options available for the zpaq 'list' command.
                force (bool): Compare file contents instead of dates.
                until (str or int): Show archive contents as of the specified date or version.
                    Date format: "YYYY-MM-DD HH:MM:SS" (e.g., "2025-06-19 01:30:45")
                to (str or list): Compare external files under a different name in the archive.
                not (str or list): Exclude files or comparison results matching the specified pattern(s) or result character(s):
                    = (same), + (only in archive), - (only external), # (different), ^ (newer external), ? (newer archive)
                    File patterns: e.g., "*.tmp" or ["*.tmp", "*.log"] 
                    Comparison results: e.g., ["=", "+"] (exclude same and archive-only files)
                only (str or list): Include only files matching the specified pattern(s).
            Returns:
                list[FileInfo]: List of FileInfo objects representing files in the archive.
        """
        options = {'key': key, 'all': all, 'summary': summary, **kwargs}
        cmd = self._build_command('l', archive, files, **options)
        output_lines = self._execute(cmd)

        parsed_files = []
        file_line_re = re.compile(
            r"^\s*([=+\-^?#])?\s*"
            r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+"
            r"([A-Z-]?)\s+"
            r"([\d,]+)\s+"
            r"(.+)"
        )

        for line in output_lines:
            match = file_line_re.match(line.strip())
            if match:
                status, dt_str, attr, size_str, filename = match.groups()
                
                size = int(size_str.replace(',', ''))
                mtime = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                
                parsed_files.append(FileInfo(
                    filename=filename.strip(),
                    size=size,
                    mtime=mtime,
                    status=status,
                    attributes=attr.strip() if attr and attr.strip() else None
                ))
        
        return parsed_files