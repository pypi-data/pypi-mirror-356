# auth in .pypirc
rm -rf ../betaflight-python/dist
rm -rf ../betaflight-python/betaflight/firmware/obj
rm -rf ../betaflight-python/betaflight/firmware/tools
rm -rf ../betaflight-python/betaflight/firmware/downloads
pip install --upgrade build twine
python3 -m build --sdist
python3 -m twine upload dist/*
