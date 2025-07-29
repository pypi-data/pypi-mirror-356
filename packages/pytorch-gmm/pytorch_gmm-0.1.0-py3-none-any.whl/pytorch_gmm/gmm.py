import itertools
import math

import numpy as np
import torch
from tqdm import tqdm

log_2pi = math.log(2 * math.pi)


class GMM:
    def __init__(
        self,
        w: torch.FloatTensor,
        mu: torch.FloatTensor,
        sigma: torch.FloatTensor,
    ):
        if w.ndim != 1:
            raise ValueError("w.ndim != 1")
        if mu.ndim != 2:
            raise ValueError("mu.ndim != 2")
        if sigma.ndim not in (2, 3):
            raise ValueError("sigma.ndim != 2 or 3")

        self.k = w.shape[0]
        self.d = mu.shape[1]

        if mu.shape[0] != self.k:
            raise ValueError("mu.shape[0] != k")
        if sigma.shape[0] != self.k:
            raise ValueError("sigma.shape[0] != k")

        if sigma.ndim == 3 and self.d > 3 and sigma.shape[1] == 3:
            # block-diagonal
            # sigma = [0 | 2]
            #         [2 | 1]
            self.block_diag = True
            if self.d % 2 != 0:
                raise ValueError("d % 2 != 0")
            elif sigma.shape[2] != self.d // 2:
                raise ValueError("sigma.shape[2] != d // 2")
        else:
            self.block_diag = False
            if sigma.shape[1] != self.d:
                raise ValueError("sigma.shape[1] != d")
            if sigma.ndim == 3 and sigma.shape[2] != self.d:
                raise ValueError("sigma.shape[2] != d")

        self.w = w
        self.mu = mu
        self.sigma = sigma
        self.diag = sigma.ndim == 2 or self.block_diag

    @classmethod
    def init(
        cls,
        x: torch.FloatTensor,
        diag: bool = True,
        block_diag: bool = False,
        sigma_eps: float = 1e-6,
    ):
        """
        Create a single-mixture GMM from data x: [N, D].
        """
        if x.ndim != 2:
            raise ValueError("x.ndim != 2")

        w = torch.ones(1, device=x.device, dtype=x.dtype)
        mu = x.mean(dim=0, keepdim=True)
        if block_diag:
            if x.shape[1] % 2 != 0:
                raise ValueError("x.shape[1] % 2 != 0")
            half_d = x.shape[1] // 2
            x1 = x[:, :half_d]  # [N, D // 2]
            x2 = x[:, half_d:]  # [N, D // 2]
            m1 = mu[:, :half_d]  # [1, D // 2]
            m2 = mu[:, half_d:]  # [1, D // 2]
            sigma11 = ((x1 - m1) ** 2).mean(dim=0, keepdim=True)  # [1, D // 2]
            sigma22 = ((x2 - m2) ** 2).mean(dim=0, keepdim=True)  # [1, D // 2]
            sigma12 = ((x1 - m1) * (x2 - m2)).mean(dim=0, keepdim=True)  # [1, D // 2]
            sigma = torch.stack((sigma11, sigma22, sigma12), dim=1)  # [1, 3, D // 2]
            sigma[:, 0:1, :].clamp_min_(sigma_eps)
        elif diag:
            sigma = x.var(correction=0, dim=0, keepdim=True)
            sigma.clamp_min_(sigma_eps)
        else:
            sigma = x.T.cov(correction=0)
            sigma.diagonal().clamp_min_(sigma_eps)
            sigma.unsqueeze_(0)
        return cls(w, mu, sigma)

    @classmethod
    def init_and_train(
        cls,
        x: torch.FloatTensor,  # [N, D]
        k: int,
        w_eps: float = 1e-5,
        sigma_eps: float = 1e-6,
        convergence_threshold: float = 1e-5,
        diag: bool = True,
        block_diag: bool = False,
        n_iter: int = 100,
        last_n_iter: int = 500,
        perturbation: float = 0.2,
        verbose: bool = False,
    ):
        """
        Create and train a GMM from data x: [N, D].
        """
        gmm = cls.init(x, diag, block_diag, sigma_eps)

        n_mix_iter = math.ceil(math.log2(k))
        for i in tqdm(range(n_mix_iter), disable=not verbose):
            gmm.split(perturbation)
            llh = gmm.train(
                x,
                n_iter=last_n_iter if i == n_mix_iter - 1 else n_iter,
                w_eps=w_eps,
                sigma_eps=sigma_eps,
                convergence_threshold=convergence_threshold,
                verbose=verbose,
            )

        return gmm, llh

    def probability(self, x: torch.FloatTensor) -> torch.FloatTensor:
        """
        x: [N, D] -> log_numer: [N, K]

        log-likelihood = log_numer.logsumexp(dim=1)
        """

        # (x - mu): [N, K, D]
        diff = x.unsqueeze(1) - self.mu.unsqueeze(0)

        if self.block_diag:
            a11 = self.sigma[:, 0, :].unsqueeze(0)  # [1, K, D // 2]
            a22 = self.sigma[:, 1, :].unsqueeze(0)  # [1, K, D // 2]
            a12 = self.sigma[:, 2, :].unsqueeze(0)  # [1, K, D // 2]
            log_det = (a11 * a22).sub_(a12.pow(2))  # denominator [1, K, D // 2]

            d1 = diff[:, :, : self.d // 2]  # [N, K, D // 2]
            d2 = diff[:, :, self.d // 2 :]  # [N, K, D // 2]
            upper = (d1 * a22).sub_(d2 * a12).div_(log_det)  # [N, K, D // 2]
            lower = (d2 * a11).sub_(d1 * a12).div_(log_det)  # [N, K, D // 2]
            log_numer = diff.mul_(torch.cat((upper, lower), dim=2)).sum(dim=2)  # [N, K]
            log_det = log_det.squeeze_(0).log_().sum(dim=1)  # [K]
        elif self.diag:
            log_det = self.sigma.log().sum(dim=1)  # [K, D] -> [K]
            # (x - mu)^T @ invΣ @ (x - mu) = sum((x - mu)^2 / diag(Σ))
            log_numer = diff.pow_(2).div_(self.sigma.unsqueeze(0)).sum(dim=2)  # [N, K]
        else:
            log_det = torch.linalg.cholesky(self.sigma)  # Σ = L L*: [K, D, D]
            # (x - mu)^T @ [invΣ @ (x - mu)]
            log_numer = torch.cholesky_solve(diff.unsqueeze(3), log_det)  # [N, K, D, 1]
            log_numer = log_numer.squeeze_(3).mul_(diff).sum(dim=2)  # [N, K]
            # log_det(Σ) = log_det(L L*) = 2 * log_det(L) = 2 * sum(log(diag(L)))
            log_det = log_det.diagonal(dim1=1, dim2=2).log_().sum(dim=1).mul_(2)  # [K]

        log_numer.add_(log_2pi * self.d).add_(log_det.unsqueeze_(0)).mul_(-0.5)
        log_numer.add_(self.w.log().unsqueeze_(0))
        return log_numer

    def split(self, perturbation_depth=0.2):
        if self.block_diag:
            sigma_diag = torch.cat((self.sigma[:, 0, :], self.sigma[:, 1, :]), dim=1)
        elif self.diag:
            sigma_diag = self.sigma
        else:
            sigma_diag = self.sigma.diagonal(dim1=1, dim2=2)
        self.k *= 2
        self.w = (self.w / 2).repeat(2)
        self._w_floor_()
        mu1 = self.mu - sigma_diag.sqrt() * perturbation_depth
        mu2 = self.mu + sigma_diag.sqrt() * perturbation_depth
        self.mu = torch.cat([mu1, mu2], dim=0)
        self.sigma = torch.cat([self.sigma, self.sigma], dim=0)

    def _w_floor_(self, eps: float = 1e-5):
        self.w.clamp_min_(eps)
        self.w.div_(self.w.sum())

    def _sigma_floor_(self, eps: float = 1e-6):
        if self.diag:
            self.sigma.clamp_min_(eps)
        else:
            self.sigma.diagonal(dim1=1, dim2=2).clamp_min_(eps)

    def _em_(self, x: torch.FloatTensor) -> torch.FloatTensor:
        n = x.shape[0]

        r = self.probability(x)
        llh = r.logsumexp(dim=1, keepdim=True)  # [N, 1]
        r.sub_(llh).exp_()  # [N, K]
        r_sum = r.sum(dim=0)  # [K]
        llh = llh.mean()

        self.w.copy_(r_sum / n)

        x = x.unsqueeze(1)  # [N, 1, D]
        r.unsqueeze_(2)  # [N, K, 1]
        r_sum.unsqueeze_(1)  # [K, 1]
        self.mu.copy_((r * x).sum(dim=0)).div_(r_sum)

        diff = x - self.mu.unsqueeze(0)  # [N, K, D]
        if self.block_diag:
            d1 = diff[:, :, : self.d // 2]  # [N, K, D // 2]
            d2 = diff[:, :, self.d // 2 :]  # [N, K, D // 2]
            r.unsqueeze_(2)  # [N, K, 1, 1]
            r_sum.unsqueeze_(2)  # [K, 1, 1]
            diff = torch.stack((d1 * d1, d2 * d2, d1 * d2), dim=2)  # [N, K, 3, D // 2]
            self.sigma.copy_(diff.mul_(r).sum(dim=0)).div_(r_sum)  # [K, 3, D // 2]
        elif self.diag:
            self.sigma.copy_(diff.pow_(2).mul_(r).sum(dim=0)).div_(r_sum)
        else:
            diff = diff.unsqueeze(3) @ diff.unsqueeze(2)  # [N, K, D, D]
            r.unsqueeze_(2)  # [N, K, 1, 1]
            r_sum.unsqueeze_(2)  # [K, 1, 1]
            self.sigma.copy_(diff.mul_(r).sum(dim=0)).div_(r_sum)  # [K, D, D]

        return llh

    def train(
        self,
        x: torch.FloatTensor,
        n_iter: int | None = 20,
        w_eps: float = 1e-5,
        sigma_eps: float = 1e-6,
        convergence_threshold: float | None = 1e-5,
        verbose: bool = False,
    ) -> float:
        if n_iter is None and convergence_threshold is None:
            raise ValueError("n_iter == None && convergence_threshold == None")

        iter = itertools.count() if n_iter is None else range(n_iter)
        pbar = tqdm(iter, disable=not verbose, desc=f"k={self.k},llh=?,diff=?")
        last_llh = None

        for _ in pbar:
            llh = self._em_(x)
            if not torch.isfinite(llh):
                raise RuntimeError("non-finite log-likelihood")

            self._w_floor_(eps=w_eps)
            self._sigma_floor_(eps=sigma_eps)

            diff = math.inf
            if last_llh is not None:
                diff = llh.item() - last_llh
            last_llh = llh.item()
            pbar.set_description(f"k={self.k},llh={llh.item():.4f},diff={diff:.4g}")

            if convergence_threshold is not None and diff < convergence_threshold:
                break

        return last_llh

    def to_sptk(self):
        bin = b""

        for i in range(self.k):
            bin += self.w[i].cpu().double().numpy().tobytes()
            bin += self.mu[i].cpu().double().numpy().tobytes()
            if self.block_diag:
                s11, s22, s12 = self.sigma[i, :, :].cpu().double()
                s = torch.cat(
                    (
                        torch.cat((s11.diag(), s12.diag()), dim=1),
                        torch.cat((s12.diag(), s22.diag()), dim=1),
                    ),
                    dim=0,
                )
                bin += s.numpy().tobytes()
            elif self.diag:
                bin += self.sigma[i].cpu().double().numpy().tobytes()
            else:
                bin += self.sigma[i].cpu().double().numpy().tobytes()

        return bin

    @classmethod
    def from_sptk(cls, bin: bytes, k: int, d: int, block_diag: bool = False):
        np_array = np.frombuffer(bin, dtype=np.float64).copy()
        full = len(np_array) == k * (1 + d + d * d)
        if not full and len(np_array) != k * (1 + 2 * d):
            raise ValueError("invalid buffer length")

        block_size = 1 + d + d * d if full else 1 + 2 * d
        array = torch.from_numpy(np_array.reshape(k, block_size))

        w = array[:, 0]
        mu = array[:, 1 : 1 + d]
        sigma = array[:, 1 + d :]

        if full:
            sigma = sigma.reshape(k, d, d)
            if block_diag:
                if d % 2 != 0:
                    raise ValueError("d % 2 != 0")
                sigma = torch.stack(
                    (
                        sigma[:, : d // 2, : d // 2].diagonal(dim1=1, dim2=2),
                        sigma[:, d // 2 :, d // 2 :].diagonal(dim1=1, dim2=2),
                        sigma[:, : d // 2, d // 2 :].diagonal(dim1=1, dim2=2),
                    ),
                    dim=1,
                )

        return cls(w, mu, sigma)

    ### Utility methods ###

    def to(self, device: torch.device):
        self.w = self.w.to(device)
        self.mu = self.mu.to(device)
        self.sigma = self.sigma.to(device)
        return self

    def cpu(self):
        self.w = self.w.cpu()
        self.mu = self.mu.cpu()
        self.sigma = self.sigma.cpu()
        return self

    def cuda(self, device: torch.device | int = 0):
        self.w = self.w.cuda(device)
        self.mu = self.mu.cuda(device)
        self.sigma = self.sigma.cuda(device)
        return self

    def __call__(self, *args, **kwargs):
        return self.probability(*args, **kwargs)
