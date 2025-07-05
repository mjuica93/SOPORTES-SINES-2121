#!/usr/bin/env python3
"""
Performance Cleanup Script for SINES Support System

This script removes large files, duplicates, and other performance bottlenecks
to optimize the codebase for production deployment.
"""

import os
import shutil
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Set


class PerformanceCleanup:
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.removed_files: List[str] = []
        self.moved_files: List[str] = []
        self.compressed_files: List[str] = []
        self.total_space_saved: int = 0
        
    def get_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except (OSError, IOError):
            return ""
        return hash_md5.hexdigest()
    
    def get_file_size(self, filepath: Path) -> int:
        """Get file size in bytes"""
        try:
            return filepath.stat().st_size
        except (OSError, IOError):
            return 0
    
    def format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable format"""
        size_float = float(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_float < 1024.0:
                return f"{size_float:.1f} {unit}"
            size_float /= 1024.0
        return f"{size_float:.1f} TB"
    
    def find_large_files(self, size_threshold: int = 10 * 1024 * 1024) -> List[Path]:
        """Find files larger than threshold (default 10MB)"""
        large_files = []
        
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file():
                file_size = self.get_file_size(file_path)
                if file_size > size_threshold:
                    large_files.append(file_path)
        
        return large_files
    
    def find_duplicate_files(self) -> Dict[str, List[Path]]:
        """Find duplicate files based on content hash"""
        file_hashes: Dict[str, List[Path]] = {}
        
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                file_hash = self.get_file_hash(file_path)
                if file_hash:
                    if file_hash not in file_hashes:
                        file_hashes[file_hash] = []
                    file_hashes[file_hash].append(file_path)
        
        # Return only files that have duplicates
        return {h: files for h, files in file_hashes.items() if len(files) > 1}
    
    def find_redundant_html_files(self) -> List[Path]:
        """Find HTML files that are likely duplicates or redundant"""
        html_files = list(self.workspace_path.glob("*.html"))
        
        # Define patterns for redundant files
        redundant_patterns = [
            "index_enhanced.html",
            "index_enhanced_robust.html", 
            "index_enhanced_with_templates.html",
            "index_failsafe.html",
            "index_infalible.html",
            "verificar_json.html",
            "SOLUCION_DEFINITIVA.html"
        ]
        
        redundant_files = []
        for pattern in redundant_patterns:
            file_path = self.workspace_path / pattern
            if file_path.exists():
                redundant_files.append(file_path)
        
        return redundant_files
    
    def find_redundant_js_files(self) -> List[Path]:
        """Find JavaScript files that are likely duplicates or redundant"""
        js_files = list(self.workspace_path.glob("*.js"))
        
        # Define patterns for redundant files (keep original app.js and optimized version)
        redundant_patterns = [
            "app_enhanced.js",
            "app_enhanced_robust.js",
            "app_enhanced_with_templates.js"
        ]
        
        redundant_files = []
        for pattern in redundant_patterns:
            file_path = self.workspace_path / pattern
            if file_path.exists():
                redundant_files.append(file_path)
        
        return redundant_files
    
    def find_redundant_json_files(self) -> List[Path]:
        """Find JSON files that are redundant or can be removed"""
        json_files = list(self.workspace_path.glob("*.json"))
        
        # Keep only essential JSON files
        essential_files = {
            "support_data_enhanced.json",
            "support_data.json", 
            "support_pdf_mapping.json",
            "railway.json",
            "field_titles_mapping.json",
            "column_titles_mapping.json"
        }
        
        redundant_files = []
        for json_file in json_files:
            if json_file.name not in essential_files:
                # Check if it's a large file that can be removed
                file_size = self.get_file_size(json_file)
                if file_size > 1024 * 1024:  # Larger than 1MB
                    redundant_files.append(json_file)
        
        return redundant_files
    
    def remove_large_binaries(self) -> int:
        """Remove large binary files that shouldn't be in the repo"""
        large_binaries = [
            "ngrok.exe",
            "*.exe",
            "*.dll",
            "*.so",
            "*.dylib"
        ]
        
        removed_size = 0
        
        for pattern in large_binaries:
            for file_path in self.workspace_path.rglob(pattern):
                if file_path.is_file():
                    file_size = self.get_file_size(file_path)
                    try:
                        file_path.unlink()
                        self.removed_files.append(str(file_path))
                        removed_size += file_size
                        print(f"🗑️  Removed binary: {file_path} ({self.format_size(file_size)})")
                    except (OSError, IOError) as e:
                        print(f"❌ Error removing {file_path}: {e}")
        
        return removed_size
    
    def create_archive_folder(self):
        """Create archive folder for moved files"""
        archive_path = self.workspace_path / "archive"
        archive_path.mkdir(exist_ok=True)
        return archive_path
    
    def move_redundant_files(self) -> int:
        """Move redundant files to archive folder"""
        archive_path = self.create_archive_folder()
        total_moved_size = 0
        
        # Move redundant HTML files
        for file_path in self.find_redundant_html_files():
            dest_path = archive_path / file_path.name
            file_size = self.get_file_size(file_path)
            try:
                shutil.move(str(file_path), str(dest_path))
                self.moved_files.append(str(file_path))
                total_moved_size += file_size
                print(f"📁 Moved HTML: {file_path.name} ({self.format_size(file_size)})")
            except (OSError, IOError) as e:
                print(f"❌ Error moving {file_path}: {e}")
        
        # Move redundant JS files
        for file_path in self.find_redundant_js_files():
            dest_path = archive_path / file_path.name
            file_size = self.get_file_size(file_path)
            try:
                shutil.move(str(file_path), str(dest_path))
                self.moved_files.append(str(file_path))
                total_moved_size += file_size
                print(f"📁 Moved JS: {file_path.name} ({self.format_size(file_size)})")
            except (OSError, IOError) as e:
                print(f"❌ Error moving {file_path}: {e}")
        
        # Move redundant JSON files
        for file_path in self.find_redundant_json_files():
            dest_path = archive_path / file_path.name
            file_size = self.get_file_size(file_path)
            try:
                shutil.move(str(file_path), str(dest_path))
                self.moved_files.append(str(file_path))
                total_moved_size += file_size
                print(f"📁 Moved JSON: {file_path.name} ({self.format_size(file_size)})")
            except (OSError, IOError) as e:
                print(f"❌ Error moving {file_path}: {e}")
        
        return total_moved_size
    
    def clean_duplicate_files(self) -> int:
        """Remove duplicate files (keep the first one)"""
        duplicates = self.find_duplicate_files()
        removed_size = 0
        
        for file_hash, file_list in duplicates.items():
            if len(file_list) > 1:
                # Keep the first file, remove others
                keep_file = file_list[0]
                for dup_file in file_list[1:]:
                    file_size = self.get_file_size(dup_file)
                    try:
                        dup_file.unlink()
                        self.removed_files.append(str(dup_file))
                        removed_size += file_size
                        print(f"🗑️  Removed duplicate: {dup_file.name} (kept {keep_file.name})")
                    except (OSError, IOError) as e:
                        print(f"❌ Error removing {dup_file}: {e}")
        
        return removed_size
    
    def optimize_json_files(self) -> int:
        """Optimize JSON files by removing formatting and comments"""
        json_files = [
            "support_data_enhanced.json",
            "support_data.json",
            "support_pdf_mapping.json"
        ]
        
        optimized_size = 0
        
        for json_filename in json_files:
            json_path = self.workspace_path / json_filename
            if json_path.exists():
                try:
                    # Load and rewrite with compact format
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    original_size = self.get_file_size(json_path)
                    
                    # Write back with compact format
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
                    
                    new_size = self.get_file_size(json_path)
                    saved_size = original_size - new_size
                    optimized_size += saved_size
                    
                    print(f"📦 Optimized JSON: {json_filename} "
                          f"({self.format_size(original_size)} → {self.format_size(new_size)}, "
                          f"saved {self.format_size(saved_size)})")
                          
                except (OSError, IOError, json.JSONDecodeError) as e:
                    print(f"❌ Error optimizing {json_filename}: {e}")
        
        return optimized_size
    
    def run_cleanup(self):
        """Run complete cleanup process"""
        print("🚀 Starting Performance Cleanup")
        print("=" * 50)
        
        # Remove large binaries
        print("\n🗑️  Removing large binary files...")
        removed_binaries = self.remove_large_binaries()
        self.total_space_saved += removed_binaries
        
        # Move redundant files
        print("\n📁 Moving redundant files to archive...")
        moved_size = self.move_redundant_files()
        self.total_space_saved += moved_size
        
        # Clean duplicates
        print("\n🗑️  Removing duplicate files...")
        removed_duplicates = self.clean_duplicate_files()
        self.total_space_saved += removed_duplicates
        
        # Optimize JSON files
        print("\n📦 Optimizing JSON files...")
        optimized_size = self.optimize_json_files()
        self.total_space_saved += optimized_size
        
        # Summary
        print("\n" + "=" * 50)
        print("✅ Cleanup Summary")
        print("=" * 50)
        print(f"Files removed: {len(self.removed_files)}")
        print(f"Files moved to archive: {len(self.moved_files)}")
        print(f"Total space saved: {self.format_size(self.total_space_saved)}")
        
        if self.removed_files:
            print(f"\n🗑️  Removed files:")
            for file in self.removed_files[:10]:  # Show first 10
                print(f"   • {file}")
            if len(self.removed_files) > 10:
                print(f"   ... and {len(self.removed_files) - 10} more")
        
        if self.moved_files:
            print(f"\n📁 Moved files:")
            for file in self.moved_files[:10]:  # Show first 10
                print(f"   • {file}")
            if len(self.moved_files) > 10:
                print(f"   ... and {len(self.moved_files) - 10} more")
        
        # Create cleanup report
        self.create_cleanup_report()
        
        print(f"\n🎉 Cleanup complete! Saved {self.format_size(self.total_space_saved)}")
        print("📋 Detailed report saved to: cleanup_report.json")
    
    def create_cleanup_report(self):
        """Create a detailed cleanup report"""
        report = {
            "cleanup_date": str(Path.cwd()),
            "total_space_saved": self.total_space_saved,
            "total_space_saved_formatted": self.format_size(self.total_space_saved),
            "files_removed": len(self.removed_files),
            "files_moved": len(self.moved_files),
            "removed_files": self.removed_files,
            "moved_files": self.moved_files,
            "recommendations": [
                "Consider implementing database storage for large datasets",
                "Use CDN for static assets in production",
                "Implement proper backup strategy before cleanup",
                "Monitor application performance after cleanup"
            ]
        }
        
        with open("cleanup_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


def main():
    """Main function"""
    print("🧹 SINES Performance Cleanup Tool")
    print("This tool will optimize your workspace by removing large files,")
    print("duplicates, and redundant code.")
    print()
    
    response = input("⚠️  This will modify your workspace. Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cleanup cancelled.")
        return
    
    cleanup = PerformanceCleanup()
    cleanup.run_cleanup()


if __name__ == "__main__":
    main()