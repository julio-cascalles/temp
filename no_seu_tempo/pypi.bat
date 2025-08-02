@echo off
echo ======= Montando DIST ...  ===========
python -m setup sdist bdist_wheel
echo ======== Fazendo upload ==============
twine upload dist/*
echo ************************************
echo ****** Processo concluído! *********
echo ************************************
