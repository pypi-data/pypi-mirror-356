import torch
from torch import nn, Tensor
from fmot.nn import Loop, GMACv2
from fmot.precisions import int16, int24
import fmot
import pytest
import numpy as np


class i24SumLoop(Loop):
    def __init__(self, n_iter: int, n_channels: int, dim=-1):
        super().__init__(
            n_iter=n_iter, slice_blocksizes=[n_channels], n_recurse=1, dim=dim
        )
        self.gmac = GMACv2(int24, torch.tensor([1, 1]))

    @torch.jit.export
    def step(
        self, x_sliced: list[Tensor], x_recursed: list[Tensor], x_scope: list[Tensor]
    ) -> tuple[list[Tensor], list[Tensor], list[Tensor]]:
        (x_i,) = x_sliced
        (curr_sum,) = x_recursed

        y = self.gmac([], [], [x_i, curr_sum])

        # x_recurse', y_concat, y_final
        return [y], [], [y]


class i24SumModel(nn.Module):
    def __init__(self, n_iter, n_channels):
        super().__init__()
        self.summer = i24SumLoop(n_iter, n_channels)
        self.n_channels = n_channels
        self.s_init = nn.Parameter(torch.zeros(n_channels), requires_grad=False)
        self.cast_up1 = GMACv2(int24, torch.tensor([1]))
        self.cast_up2 = GMACv2(int24, torch.tensor([1]))
        self.cast_down = GMACv2(int16, torch.tensor([1]))

    def forward(self, x):
        x_cast = self.cast_up1([], [], [x])
        s_init_cast = self.cast_up2([], [], [self.s_init])

        (y,) = self.summer([x_cast], [s_init_cast], [])

        y_cast = self.cast_down([], [], [y])
        return y_cast


@pytest.mark.parametrize(["n_iter", "channels"], [[16, 18]])
def test_i24_sum(n_iter: int, channels: int):
    model = i24SumModel(n_iter, channels)
    cmodel = fmot.ConvertedModel(model)
    cmodel.quantize([torch.randn(8, n_iter * channels).abs() for _ in range(4)])

    # print(cmodel)

    x = torch.randn(8, n_iter * channels).abs()
    y0 = model(x)
    y1 = cmodel(x)

    nrmse = (y0 - y1).pow(2).mean().sqrt()
    print(nrmse)

    graph = cmodel.trace()
    print(graph)

    y_fqir = graph.run(x[0].numpy(), dequant=True)
    assert np.array_equal(y_fqir, y1[0].numpy())


if __name__ == "__main__":
    import logging

    # logging.basicConfig(level=logging.DEBUG)
    test_i24_sum(8, 16)
