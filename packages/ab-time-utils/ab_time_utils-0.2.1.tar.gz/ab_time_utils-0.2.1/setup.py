from setuptools import setup, find_packages
import pathlib

# 加载README内容
cur_dir = pathlib.Path(__file__).parent
long_desc = (cur_dir / "README.md").read_text(encoding="utf-8")

setup(
    name='ab_time_utils',  
    version='0.2.1',

    long_description=long_desc, 
    long_description_content_type="text/markdown",  

    packages=find_packages(),
    install_requires=[], # # 在此处列出依赖项
    author='ab',  
    author_email='17317591878@163.com',
    description='常用时间库',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 许可证类型
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
