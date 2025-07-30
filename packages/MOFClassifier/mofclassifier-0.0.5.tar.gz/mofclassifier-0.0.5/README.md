## MOFClassifier: A Machine Learning Approach for Validating Computation-Ready Metal-Organic Frameworks
                                                                                                                                          
[![Static Badge](https://img.shields.io/badge/arXiv.2506.14845v1-brightgreen?style=flat)](https://arxiv.org/abs/2506.14845)
[![Requires Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg?logo=python&logoColor=white)](https://python.org/downloads)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15654431.svg)](https://doi.org/10.5281/zenodo.15654431)
                                                                     
**Developed by:** [Guobin Zhao](https://github.com/sxm13)                                
                                                                                                         
### Installation 
                                     
```sh
pip install MOFClassifier
```

### Examples                                                                                                     
```python
from MOFClassifier import CLscore
cifid, all_score, mean_score = CLscore.predict(root_cif="./example.cif")
```
-  **root_cif**: the path of your structure
-  **cifid**: the name of structure
-  **all_score**: the CLscore predicted by 100 models (bags)
-  **mean_score**: the mean CLscore of **CLscores**
                                                                                
### Citation                                          
**Guobin Zhao**, **Pengyu Zhao** and **Yongchul G. Chung**. 2025. **arXiv.2506.14845**.
