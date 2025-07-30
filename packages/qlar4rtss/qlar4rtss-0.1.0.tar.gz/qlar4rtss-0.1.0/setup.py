from setuptools import setup, find_packages

setup(
    name='qlar4rtss',
    version='0.1.0',
    keywords='eeg realtime sleep staging analysis',
    description='a python analyse sdk for QLan realtime sleep staging analysis',
    license='MIT License',
    author='scg',
    author_email='shangweb001@gmail.com',
    packages=find_packages(),
    include_package_data=True,  
    package_data={
        "qlar4rtss": ["model/*.csv"],  # 指定要包含的文件类型
    },
    platforms='any',
    install_requires=['qlsdk2', 'scipy', 'numpy', 'lightgbm', 'pandas','PySide6','joblib','pyedflib','mne','scikit-learn'],
)