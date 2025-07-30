from setuptools import setup, find_packages
import os

def find_package_files(package_dir, extensions):
    """Find all files with specified extensions in the package directory."""
    file_list = []
    for dirpath, _, filenames in os.walk(package_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.relpath(os.path.join(dirpath, filename), package_dir)
                file_list.append(file_path)
    return file_list

package_name = "bpusdk"
file_extensions = [".py", ".pyc"]  # Include Python and compiled files
package_files = find_package_files(package_name, file_extensions)

setup(
    name=package_name,
    version='2.0',
    license='MIT',
    author="GDIIST",
    author_email='739503445@qq.com',
    packages=find_packages(),
    package_data={package_name: package_files},  # Include .py and .so files
    include_package_data=True,
    install_requires=['brainpy>=2.4.2', 'brainpylib'],
)