"""Linear algebra utilities for symmetric vector spaces with known group representations."""

import torch
from escnn.group import Representation
from torch import Tensor


def isotypic_signal2irreducible_subspaces(x: Tensor, rep_x: Representation):
    r"""Given a random variable in an isotypic subspace, flatten the r.v. into G-irreducible subspaces.

    Given a signal of shape :math:`(n, m_x \cdot d)` where :math:`n` is the number of samples, :math:`m_x` the
    multiplicity of the irrep in :math:`X`, and :math:`d` the dimension of the irrep.

    :math:`X = [x_1, \ldots, x_n]` and :math:`x_i = [x_{i_{11}}, \ldots, x_{i_{1d}}, x_{i_{21}}, \ldots, x_{i_{2d}},
    \ldots, x_{i_{m_x1}}, \ldots, x_{i_{m_xd}}]`

    This function returns the signal :math:`Z` of shape :math:`(n \cdot d, m_x)` where each column represents the
    flattened signal of a G-irreducible subspace.

    :math:`Z[:, k] = [x_{1_{k1}}, \ldots, x_{1_{kd}}, x_{2_{k1}}, \ldots, x_{2_{kd}}, \ldots, x_{n_{k1}}, \ldots,
    x_{n_{kd}}]`

    Args:
        x (Tensor): Shape :math:`(..., n, m_x \cdot d)` where :math:`n` is the number of samples and :math:`m_x` the
         multiplicity of the irrep in :math:`X`.
        rep_x (escnn.nn.Representation): Representation in the isotypic basis of a single type of irrep.

    Returns:
        Tensor:

    Shape:
        :math:`(n \cdot d, m_x)`, where each column represents the flattened signal of an irreducible subspace.
    """
    assert len(rep_x._irreps_multiplicities) == 1, "Random variable is assumed to be in a single isotypic subspace."
    irrep_id = rep_x.irreps[0]
    irrep_dim = rep_x.group.irrep(*irrep_id).size
    mk = rep_x._irreps_multiplicities[irrep_id]  # Multiplicity of the irrep in X

    Z = x.view(-1, mk, irrep_dim).permute(0, 2, 1).reshape(-1, mk)

    assert Z.shape == (x.shape[0] * irrep_dim, mk)
    return Z


def lstsq(X: Tensor, Y: Tensor, rep_X: Representation, rep_Y: Representation):
    r"""Computes a solution to the least squares problem of a system of linear equations with equivariance constraints.

    The :math:`\mathbb{G}`-equivariant least squares problem to the linear system of equations
    :math:`\mathbf{Y} = \mathbf{A}\,\mathbf{X}`, is defined as:

    .. math::
        \begin{align}
            &\| \mathbf{Y} - \mathbf{A}\,\mathbf{X} \|_F \\
            & \text{s.t.} \quad \rho_{\mathcal{Y}}(g) \mathbf{A} = \mathbf{A}\rho_{\mathcal{X}}(g) \quad \forall g
            \in \mathbb{G},
        \end{align}

    where :math:`\rho_{\mathcal{Y}}` and :math:`\rho_{\mathcal{X}}` denote the group representations on
    :math:`\mathbf{X}` and :math:`\mathbf{Y}`.

    Args:
        X (Tensor): Realizations of the random variable :math:`\mathbf{X}` with shape :math:`(N, D_x)`, where
         :math:`N` is the number of samples.
        Y (Tensor):
            Realizations of the r andom variable :math:`\mathbf{Y}` with shape :math:`(N, D_y)`.
        rep_X (Representation):
            The finite-group representation under which :math:`\mathbf{X}` transforms.
        rep_Y (Representation):
            The finite-group representation under which :math:`\mathbf{Y}` transforms.

    Returns:
        Tensor:
            A :math:`(D_y \times D_x)` matrix :math:`\mathbf{A}` satisfying the G-equivariance constraint
            and minimizing :math:`\|\mathbf{Y} - \mathbf{A}\,\mathbf{X}\|^2`.

    Shape:
        - X: :math:`(N, D_x)`
        - Y: :math:`(N, D_y)`
        - Output: :math:`(D_y, D_x)`
    """
    from symm_learning.representation_theory import isotypic_decomp_rep

    rep_X = isotypic_decomp_rep(rep_X)
    rep_Y = isotypic_decomp_rep(rep_Y)
    X_iso_reps = rep_X.attributes["isotypic_reps"]
    Y_iso_reps = rep_Y.attributes["isotypic_reps"]
    Qx2iso = torch.tensor(rep_X.change_of_basis_inv, dtype=X.dtype, device=X.device)
    Qy2iso = torch.tensor(rep_Y.change_of_basis_inv, dtype=Y.dtype, device=Y.device)

    x_iso = torch.einsum("ij,nj->ni", Qx2iso, X)
    y_iso = torch.einsum("ij,nj->ni", Qy2iso, Y)

    # Get orthogonal projection to isotypic subspaces.
    dimx, dimy = 0, 0
    X_iso_dims, Y_iso_dims = {}, {}
    for irrep_k_id, rep_X_k in X_iso_reps.items():
        X_iso_dims[irrep_k_id] = slice(dimx, dimx + rep_X_k.size)
        dimx += rep_X_k.size
    for irrep_k_id, rep_Y_k in Y_iso_reps.items():
        Y_iso_dims[irrep_k_id] = slice(dimy, dimy + rep_Y_k.size)
        dimy += rep_Y_k.size

    A_iso = torch.zeros((rep_Y.size, rep_X.size), device=X.device, dtype=X.dtype)
    for irrep_k_id in Y_iso_reps:
        if irrep_k_id not in X_iso_reps:
            continue
        d_k = rep_X.group.irrep(*irrep_k_id).size
        I_d_k = torch.eye(d_k, dtype=X.dtype, device=X.device)
        rep_X_k, rep_Y_k = X_iso_reps[irrep_k_id], Y_iso_reps[irrep_k_id]
        x_k, y_k = x_iso[..., X_iso_dims[irrep_k_id]], y_iso[..., Y_iso_dims[irrep_k_id]]

        # A_k = (Zyx_k @ Zx_k^†) ⊗ I_d_k
        # Cx_k, Zx_k = isotypic_covariance(x=x_k, y=x_k, rep_X=rep_X_k, rep_Y=rep_X_k)
        # Cyx_k, Zyx_k = isotypic_covariance(x=x_k, y=y_k, rep_X=rep_X_k, rep_Y=rep_Y_k)
        # A_k = torch.kron(Zyx_k @ torch.linalg.pinv(Zx_k), torch.eye(d_k, dtype=x.dtype, device=x.device))
        x_sing = isotypic_signal2irreducible_subspaces(x_k, rep_X_k)
        y_sing = isotypic_signal2irreducible_subspaces(y_k, rep_Y_k)
        # (Zyx_k @ Zx_k^†)
        out = torch.linalg.lstsq(x_sing, y_sing)
        A_k = torch.kron(out.solution.T, I_d_k)

        A_iso[Y_iso_dims[irrep_k_id], X_iso_dims[irrep_k_id]] = A_k

    # Change back to the original input output basis sets
    A = Qy2iso.T @ A_iso @ Qx2iso
    return A


def invariant_orthogonal_projector(rep_x: Representation) -> Tensor:
    r"""Computes the orthogonal projection to the invariant subspace.

    The input representation :math:`\rho_{\mathcal{X}}: \mathbb{G} \mapsto \mathbb{G}\mathbb{L}(\mathcal{X})` is
    transformed to the spectral basis given by:

    .. math::
        \rho_\mathcal{X} = \mathbf{Q} \left( \bigoplus_{i\in[1,n]} \hat{\rho}_i \right) \mathbf{Q}^T

    where :math:`\hat{\rho}_i` denotes an instance of one of the irreducible representations of the group, and
    :math:`\mathbf{Q}: \mathcal{X} \mapsto \mathcal{X}` is the orthogonal change of basis from the spectral basis to
    the original basis.

    The projection is performed by:
        1. Changing the basis to the representation spectral basis (exposing signals per irrep).
        2. Zeroing out all signals on irreps that are not trivial.
        3. Mapping back to the original basis set.

    Args:
        rep_x (Representation): The representation for which the orthogonal projection to the invariant subspace is
        computed.

    Returns:
        Tensor: The orthogonal projection matrix to the invariant subspace, :math:`\mathbf{Q} \mathbf{S} \mathbf{Q}^T`.
    """
    Qx_T, Qx = Tensor(rep_x.change_of_basis_inv), Tensor(rep_x.change_of_basis)

    # S is an indicator of which dimension (in the irrep-spectral basis) is associated with a trivial irrep
    S = torch.zeros((rep_x.size, rep_x.size))
    irreps_dimension = []
    cum_dim = 0
    for irrep_id in rep_x.irreps:
        irrep = rep_x.group.irrep(*irrep_id)
        # Get dimensions of the irrep in the original basis
        irrep_dims = range(cum_dim, cum_dim + irrep.size)
        irreps_dimension.append(irrep_dims)
        if irrep_id == rep_x.group.trivial_representation.id:
            # this dimension is associated with a trivial irrep
            S[irrep_dims, irrep_dims] = 1
        cum_dim += irrep.size

    inv_projector = Qx @ S @ Qx_T
    return inv_projector
