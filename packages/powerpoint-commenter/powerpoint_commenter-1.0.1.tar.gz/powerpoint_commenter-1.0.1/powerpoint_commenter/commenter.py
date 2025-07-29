#!/usr/bin/env python3
"""
PowerPoint Comment Adder - Python Wrapper
A Python interface for adding comments to PowerPoint presentations using OpenXML SDK.
"""

import subprocess
import os
import sys
import json
from pathlib import Path
from typing import Optional, Union

class PowerPointCommenter:
    """
    A Python wrapper for adding comments to PowerPoint presentations.
    
    This class provides a Python interface to the .NET-based PowerPoint comment
    functionality, making it easy to integrate into Python workflows.
    """
    
    def __init__(self, dotnet_app_path: Optional[str] = None):
        """
        Initialize the PowerPoint commenter.
        
        Args:
            dotnet_app_path: Path to the .NET application. If None, looks for it in common locations.
        """
        self.dotnet_app_path = dotnet_app_path or self._find_dotnet_app()
        self._verify_dotnet_available()
    
    def _find_dotnet_app(self) -> str:
        """Find the .NET application in common locations."""
        # First check if we're in a package installation
        package_dir = os.path.dirname(__file__)
        package_dll = os.path.join(package_dir, "bin", "PowerPointCommentAdder.dll")
        
        possible_paths = [
            package_dll,  # Bundled with package
            "./bin/Debug/net9.0/PowerPointCommentAdder.dll",
            "./bin/Release/net9.0/PowerPointCommentAdder.dll",
            "PowerPointCommentAdder.dll",
            "./PowerPointCommentAdder.dll"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError(
            "PowerPointCommentAdder.dll not found. Please build the .NET application first or specify the path."
        )
    
    def _verify_dotnet_available(self):
        """Verify that .NET runtime is available."""
        try:
            result = subprocess.run(["dotnet", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError("dotnet command failed")
        except FileNotFoundError:
            raise RuntimeError(
                ".NET runtime not found. Please install .NET 9.0 or later from https://dotnet.microsoft.com/download"
            )
    
    def add_comment(self, 
                   file_path: Union[str, Path], 
                   slide_number: int, 
                   author_name: str, 
                   author_initials: str, 
                   comment_text: str) -> bool:
        """
        Add a comment to a PowerPoint slide.
        
        Args:
            file_path: Path to the PowerPoint file (.pptx)
            slide_number: Slide number (1-based)
            author_name: Name of the comment author
            author_initials: Initials of the author
            comment_text: Text content of the comment
            
        Returns:
            bool: True if comment was added successfully, False otherwise
            
        Raises:
            FileNotFoundError: If the PowerPoint file doesn't exist
            ValueError: If parameters are invalid
            RuntimeError: If the .NET application fails
        """
        # Validate inputs
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"PowerPoint file not found: {file_path}")
        
        if slide_number < 1:
            raise ValueError("Slide number must be 1 or greater")
        
        if not author_name.strip():
            raise ValueError("Author name cannot be empty")
        
        if not author_initials.strip():
            raise ValueError("Author initials cannot be empty")
        
        if not comment_text.strip():
            raise ValueError("Comment text cannot be empty")
        
        # Prepare command
        cmd = [
            "dotnet", 
            self.dotnet_app_path,
            str(file_path.absolute()),
            str(slide_number),
            author_name,
            author_initials,
            comment_text
        ]
        
        try:
            # Run the .NET application
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30  # 30 second timeout
            )
            
            if result.returncode == 0:
                print(f"✓ Successfully added comment to slide {slide_number}")
                return True
            else:
                print(f"❌ Error adding comment: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Operation timed out after 30 seconds")
        except Exception as e:
            raise RuntimeError(f"Failed to execute .NET application: {e}")
    
    def add_multiple_comments(self, comments_data: list) -> dict:
        """
        Add multiple comments to a PowerPoint presentation.
        
        Args:
            comments_data: List of dictionaries with comment information.
                          Each dict should have keys: file_path, slide_number, 
                          author_name, author_initials, comment_text
                          
        Returns:
            dict: Summary of results with success/failure counts
        """
        results = {
            "total": len(comments_data),
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        for i, comment_data in enumerate(comments_data):
            try:
                success = self.add_comment(
                    comment_data["file_path"],
                    comment_data["slide_number"],
                    comment_data["author_name"],
                    comment_data["author_initials"],
                    comment_data["comment_text"]
                )
                
                if success:
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(f"Comment {i+1}: Failed to add comment")
                    
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Comment {i+1}: {str(e)}")
        
        return results


def main():
    """Command-line interface for the PowerPoint commenter."""
    if len(sys.argv) < 6:
        print("Usage: python powerpoint_commenter.py <file_path> <slide_number> <author_name> <author_initials> <comment_text>")
        print("\nExample:")
        print('python powerpoint_commenter.py "presentation.pptx" 1 "John Doe" "JD" "Great slide!"')
        sys.exit(1)
    
    try:
        commenter = PowerPointCommenter()
        success = commenter.add_comment(
            file_path=sys.argv[1],
            slide_number=int(sys.argv[2]),
            author_name=sys.argv[3],
            author_initials=sys.argv[4],
            comment_text=sys.argv[5]
        )
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 