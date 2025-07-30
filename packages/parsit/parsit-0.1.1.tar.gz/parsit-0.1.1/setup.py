from pathlib import Path 
from setuptools import setup ,find_packages 
from parsit .libs .version import __version__ 
import os

HERE =Path (__file__ ).parent 

def parse_requirements (filename ):
    """Load requirements from a requirements file."""
    requirements =[]
    filepath =os .path .join (os .path .dirname (__file__ ), filename )
    
    if not os .path .isfile (filepath ):
        print (f"Warning: {filename} not found. Using empty requirements.")
        return requirements
        
    with open (filepath )as f :
        lines =f .read ().splitlines ()

    for line in lines :
        line = line .strip ()
        if not line or line .startswith ('#'):
            continue
        if "http"in line :
            pkg_name_without_url =line .split ('@')[0 ].strip ()
            requirements .append (pkg_name_without_url )
        else :
            requirements .append (line )

    return requirements 


if __name__ =='__main__':
# Handle missing README.md
    readme_path =HERE /'README.md'
    if readme_path .exists ():
        with readme_path .open (encoding ='utf-8')as file :
            long_description =file .read ()
    else :
        long_description ="Advanced Document Ingestion Tool"

    setup (
    name ="parsit",
    version =__version__ ,
    license ="AGPL-3.0",
    packages =find_packages (),
    package_data={
        "parsit": [
            "resources/**/*",
            "resources/**/**/*"
        ],
    },
    install_requires =parse_requirements ('requirements.txt'),
    extras_require ={
    "lite":[
    "paddleocr==2.7.3",
    "paddlepaddle==3.0.0b1;platform_system=='Linux'",
    "paddlepaddle==2.6.1;platform_system=='Windows' or platform_system=='Darwin'",
    ],
    "full":[
    "matplotlib>=3.10,<4",
    "ultralytics>=8.3.48,<9",
    "parsit-yolo==0.1.0",# 
    "dill>=0.3.8,<1",# 
    "rapid_table>=1.0.5,<2.0.0",# rapid_table
    "PyYAML>=6.0.2,<7",# yaml
    "ftfy>=6.3.1,<7",# unimernet_hf
    "openai>=1.70.0,<2",# openai SDK
    "shapely>=2.0.7,<3",# imgaug-paddleocr2pytorch
    "pyclipper>=1.3.0,<2",# paddleocr2pytorch
    "omegaconf>=2.3.0,<3",# paddleocr2pytorch
    ],
    "full_old_linux":[
    "matplotlib>=3.10,<=3.10.1",
    "ultralytics>=8.3.48,<=8.3.104",
    "parsit-yolo==0.1.0",# 
    "dill==0.3.8",# 
    "PyYAML==6.0.2",# yaml
    "ftfy==6.3.1",# unimernet_hf
    "openai==1.71.0",# openai SDK
    "shapely==2.1.0",# imgaug-paddleocr2pytorch
    "pyclipper==1.3.0.post6",# paddleocr2pytorch
    "omegaconf==2.3.0",# paddleocr2pytorch
    "albumentations==1.4.20",
    "rapid_table==1.0.3",
    ],
    },
    description ="A practical tool for converting PDF to Markdown",
    long_description =long_description ,
    long_description_content_type ="text/markdown",
    project_urls ={
    "Home":"https://parsit.ai/",
    },
    keywords =["parsit", "document", "processing", "pdf", "markdown"],
    classifiers =[
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    ],
    python_requires =">=3.10,<3.14",
    entry_points ={
        "console_scripts": [
            "parsit=parsit.tools.cli:cli"
        ],
    },
    include_package_data =True ,
    zip_safe =False ,
    )
