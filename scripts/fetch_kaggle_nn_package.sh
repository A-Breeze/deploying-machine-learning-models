#!/usr/bin/env bash

kaggle datasets download -d btw78jt/neural-network-package-repo -p packages/neural_network_model/dist/ --unzip
cd packages/neural_network_model/dist/
ls -a
mv neural_network_model-* neural_network_model
ls -a
cd neural_network_model
ls -a
mv * ..
ls -a
cd ..
ls -a
rm -rf neural_network_model
ls -a
