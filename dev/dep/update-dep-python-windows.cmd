
:: Update dependencies

:: make sure pip is up to date
python -m pip install --upgrade pip

:: pull phue
pip install --target="%~dp0\python" numpy
pip install --target="%~dp0\python" scipy
pip install --target="%~dp0\python" cv2
pip install --target="%~dp0\python" sklearn
