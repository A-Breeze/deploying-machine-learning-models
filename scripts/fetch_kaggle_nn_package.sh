#!/usr/bin/env bash

kaggle datasets download -d btw78jt/neural-network-package-repo -p packages/neural_network_model/dist/ --unzip
cd packages/neural_network_model/dist/
mv neural_network_model-* neural_network_model
cd neural_network_model
mv * ..
cd ..
rm -rf neural_network_model
