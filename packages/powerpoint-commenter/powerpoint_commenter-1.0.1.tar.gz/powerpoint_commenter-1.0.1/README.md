# PowerPoint Comment Adder

A Python package for adding comments to PowerPoint presentations using Microsoft's OpenXML SDK.

## Features

- Add comments to specific slides in PowerPoint presentations
- Cross-platform support (Windows, Linux, macOS)
- Modern Office 2021 comment system support
- Simple Python API
- Command-line interface

## Requirements

- .NET 9.0 Runtime (for the underlying comment engine)
- Python 3.7+

## Installation

### From Source

1. Clone or download this repository
2. Install the package in development mode:

```bash
pip install -e .
```

### From PyPI (when published)

```bash
pip install powerpoint-commenter
```

## Usage

### Python API

```python
from powerpoint_commenter import PowerPointCommenter

# Initialize the commenter
commenter = PowerPointCommenter()

# Add a comment to slide 1
success = commenter.add_comment(
    file_path="presentation.pptx",
    slide_number=1,
    author_name="John Doe",
    author_initials="JD",
    comment_text="This slide needs revision"
)

if success:
    print("Comment added successfully!")
else:
    print("Failed to add comment")
```

### Command Line

```bash
# Add a comment via command line
python -m powerpoint_commenter.cli "presentation.pptx" 1 "John Doe" "JD" "This slide needs revision"
```

## Platform Support

### Windows
- Requires .NET 9.0 Runtime
- Fully supported

### Linux
- Requires .NET 9.0 Runtime (`sudo apt install dotnet-runtime-9.0` on Ubuntu)
- Fully supported

### macOS
- Requires .NET 9.0 Runtime (`brew install dotnet`)
- Fully supported

## Development

1. Build the .NET component:
```bash
dotnet build -c Release
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run tests:
```bash
pytest
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### .NET Runtime Not Found
If you get errors about .NET runtime not being found, install .NET 9.0:

- **Windows**: Download from [Microsoft .NET](https://dotnet.microsoft.com/download)
- **Linux**: `sudo apt install dotnet-runtime-9.0` (Ubuntu/Debian)
- **macOS**: `brew install dotnet`

### Permission Errors
If you get permission errors on Linux/macOS, make sure the .NET application has execute permissions:

```bash
chmod +x powerpoint_commenter/bin/PowerPointCommentAdder
``` 