# pytorch-gmm

## Usage

```py
import torch
from torch_gmm import GMM

x = torch.randn(50000, 16)
gmm, llh = GMM.init_and_train(x, 64, verbose=True)
```
