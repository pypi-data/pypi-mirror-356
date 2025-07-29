from setuptools import setup, find_packages

setup(
name='contextual-privacy-guard',
version='0.1.0',
description='A toolkit for safeguarding contextual privacy in LLM prompts',
author='IBM Research',
author_email='you@ibm.com',
url='https://github.com/your-org/contextual-privacy-guard',
packages=find_packages(exclude=['tests']),
include_package_data=True,
package_data={
'contextual_privacy_guard': ['prompts/*/*.txt'],
},
install_requires=[
'requests>=2.0',
'vllm>=0.7.0',
],
entry_points={
'console_scripts': [
'contextual-privacy-guard=contextual_privacy_guard.runner:main',
],
},
python_requires='>=3.8',
)