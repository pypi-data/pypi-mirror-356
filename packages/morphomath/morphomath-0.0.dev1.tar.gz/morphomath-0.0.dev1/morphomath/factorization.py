#!/usr/bin/env python3

"""Simplify the morphological code on an hypertore."""

import itertools
import numbers
import typing

import tqdm

from morphomath.kernel import Kernel
from morphomath.utils import get_compilation_rules, get_project_root


TYPE_VAR = tuple[str, tuple[int, ...]]


class MorphCode:
    """Represent the code of a morphological operation."""

    def __init__(self, kernel: Kernel):
        """Specific code handeler."""
        assert isinstance(kernel, Kernel), kernel.__class__.__name__
        self._kernel: Kernel = kernel
        self._code: list[tuple[TYPE_VAR, list[TYPE_VAR]]] = []
        self._patch_shape: tuple[int] = None
        self._init_naive_code()

    def _init_naive_code(self, patch_shape: tuple[int] = None):
        """Write the naive morphological code."""
        # preparation
        points = self._kernel.points_array
        # points = points - points.min(axis=0)  # anchor to have only positive shift
        if patch_shape is None:
            n_voxels = 128.0  # arbitrary number of voxels
            fact = 2.0  # penalty coef for memory jump axis, larger is it, smaller the buffer is
            # prod(s_i) = n_voxels
            # s_{i+1} = fact * s_i
            shape = n_voxels**(1.0/self._kernel.dim) / fact**(0.5*(1+self._kernel.dim))
            patch_shape = [shape * fact**(i+1) for i in range(self._kernel.dim)]
            patch_shape = tuple(max(1, round(s)) for s in patch_shape)
        else:
            assert hasattr(patch_shape, "__iter__"), patch_shape.__class__.__name__
            patch_shape = tuple(patch_shape)
            assert len(patch_shape) == self._kernel.dim, patch_shape
            assert all(isinstance(s, numbers.Integral) for s in patch_shape), patch_shape
            assert all(s >= 1 for s in patch_shape), patch_shape
        self._patch_shape = patch_shape

        self._code = []

        # slidind window, iterate in c contiguous order
        for anchor in itertools.product(*(range(s) for s in patch_shape)):
            self._code.append(
                (("dst", anchor), [("src", tuple(idx)) for idx in (points + anchor).tolist()])
            )

    def cse(self) -> typing.Self:
        """Perform common subexpression elimination on the code."""
        # initialisation
        code: list[tuple[TYPE_VAR, set[TYPE_VAR]]] = [
            (alloc, set(comp)) for alloc, comp in self._code
        ]
        subexprs: dict[tuple[int, int], set[tuple[int, ...]]] = {  # all common subexpressions
            (i, j): code[i][1] & code[j][1]
            for i, j in itertools.combinations(range(len(code)), 2)
        }
        buff_counter: int = 0

        # display
        with tqdm.tqdm(desc="cse", total=len(subexprs), unit="expr", dynamic_ncols=True) as bar:

            # iterative simplification
            while subexprs := {lines: s for lines, s in subexprs.items() if len(s) >= 2}:
                bar.update(bar.total-len(subexprs)-bar.n)  # update progress bar

                # select one subgroup with an heuristic that try to minimize the number of comparisons
                # and the memory distance to reduce the cache jump size, in a c contiguous array
                (l_i, l_j), subexpr = max(subexprs.items(), key=lambda ijs: (len(ijs[1]), ijs[0]))
                # replace the sub comparisons in the code
                var = ("buff", (buff_counter,))
                buff_counter += 1
                code[l_i] = (code[l_i][0], (code[l_i][1]-subexpr)|{var})
                code[l_j] = (code[l_j][0], (code[l_j][1]-subexpr)|{var})
                code.insert(l_i, (var, subexpr))  # this position to limmit memory jump

                # remove the no longer valid subexprs
                del subexprs[(l_i, l_j)]
                subexprs = {
                    (i, j): s-subexpr if i in {l_i, l_j} or j in {l_i, l_j} else s
                    for (i, j), s in subexprs.items()
                }
                # update the subexpr line number to fit the new code
                subexprs = {(i+int(i>=l_i), j+int(j>=l_i)): s for (i, j), s in subexprs.items()}
                # compute new subexprs
                subexprs |= {
                    (min(l_i, j), max(l_i, j)): code[l_i][1] & code[j][1]
                    for j in range(len(code)) if l_i != j
                }
            self._code = [(alloc, sorted(comp)) for alloc, comp in code]  # in favor of c contiguous
            bar.update(bar.total-bar.n)
        return self

    def limit_buff(self) -> typing.Self:
        """Reduce the len of the buffer."""
        # searches for positions where variables are used for the last
        released: dict[int, int] = {}  # to each buff idx, associate the line of last used
        for i, ((alloc_symb, alloc_idx), comp) in enumerate(reversed(self._code)):
            for comp_symb, comp_idx in comp:
                if comp_symb == "buff":
                    (idx,) = comp_idx
                    released[idx] = released.get(idx, len(self._code)-i-1)

        # reverse the released var order
        inv_released: dict[int, list[int]] = {}  # line -> indices
        for idx, line in released.items():
            inv_released[line] = inv_released.get(line, [])
            inv_released[line].append(idx)

        # find the replacement table
        subs: dict[int, int] = {}  # correspondance table: old_idx -> new_idx
        used: set(int) = set()  # buffer indices currently used
        for line, ((alloc_symb, alloc_idx), _) in enumerate(self._code):
            if alloc_symb == "buff":
                (idx,) = alloc_idx
                if idx not in subs:  # if it is the first time we meet the indice
                    free = min(set(range(len(used)+1))-used)  # the smallest free index
                    subs[idx] = free
                    used.add(free)
            for idx in inv_released.get(line, []):  # last appearance of the variable
                used.remove(subs[idx])  # we make it available for the suite

        # replace the indices
        self._code = [
            (
                (a_s, a_i if a_s != "buff" else (subs[a_i[0]],)),
                [(s, idx if s != "buff" else (subs[idx[0]],)) for s, idx in comp],
            )
            for (a_s, a_i), comp in self._code
        ]

        return self

    def complexity(self) -> str:
        """Return the code complexity."""
        allocs: set[tuple[int, ...]] = set()
        comps: int = 0
        buff_len: int = 0
        for (alloc_symb, alloc_idx), comp in self._code:
            comps += len(comp) - 1
            match alloc_symb:
                case "dst":
                    allocs.add(alloc_idx)
                case "buff":
                    buff_len = max(buff_len, alloc_idx[0]+1)
        nb_alloc = len(allocs)
        return (
            f"There is {nb_alloc} pixels for {comps} comparisons.\n"
            f"It corresponds to {comps/nb_alloc:.2f} comp/pxl in average.\n"
            f"It requires a buffer of size {buff_len}.\n"
            f"The patch shape is {' x '.join(map(str, self._patch_shape))}."
        )

    def compile_c_patch(self, dtype: str="npy_float") -> str:
        """Return the C function to compute the morpho on a patch."""

        def assign(symb: str, idx: tuple[int]) -> str:
            """C tab assignation."""
            if symb == "buff":
                return f"buff[{idx[0]}]"
            match len(idx):
                case 1:
                    return f"*({dtype} *)PyArray_GETPTR1({symb}, a0+{idx[0]})"
                case 2:
                    return f"*({dtype} *)PyArray_GETPTR2({symb}, a0+{idx[0]}, a1+{idx[1]})"
                case 3:
                    return f"*({dtype} *)PyArray_GETPTR3({symb}, a0+{idx[0]}, a1+{idx[1]}, a2+{idx[2]})"
                case 4:
                    return f"*({dtype} *)PyArray_GETPTR4({symb}, a0+{idx[0]}, a1+{idx[1]}, a2+{idx[2]}, a3+{idx[3]})"
                case _:
                    raise NotImplementedError("only dimension 1, 2, 3 or 4 are supported")

        # header
        dim = self._kernel.dim
        src_field = ",".join(
            f"a{i}-{e1}:a{i}+{s+e2}"
            for i, ((e1, e2), s) in enumerate(zip(self.borders_size(), self._patch_shape))
        )
        dst_field = ",".join(f"a{i}:a{i}+{s}" for i, s in enumerate(self._patch_shape))
        if dim == 1:
            kernel = f"kernel: {''.join(str(e) for e in self._kernel.tensor.tolist())}"
        elif dim == 2:
            kernel = f"kernel: {'\n        '.join(''.join(str(e) for e in l) for l in self._kernel.tensor.tolist())}"
        else:
            kernel = f"kernel points: {self._kernel.points}"
        code = (
            "int morpho_patch(\n"
            f"    PyArrayObject* dst,  // the output {dim}nd array, it can be an alias of src\n"
            f"    PyArrayObject* src,  // the input {dim}nd array\n"
            "    // the absolute patch anchor point\n"
            f"    {',\n    '.join(f'long int a{i}' for i in range(dim))}\n"
            ") {\n"
            "    /*\n"
            "        Perform a fast morphological operation on a "
            f"{' x '.join(map(str, self._patch_shape))} patch of *src*.\n"
            "        Please note that no validity range tests are performed,\n"
            f"        so src[{src_field}] must be reachable and dst[{dst_field}] as well.\n"
            f"        {'\n        '.join(kernel.split('\n'))}\n"
            f"        There are {len(self._code)} assignations "
            f"and {sum(len(e)-1 for _, e in self._code)} comparisons.\n"
            "    */\n"
        )

        # alloc
        buff_max = -1
        for (alloc_symb, alloc_idx), _ in self._code:
            if alloc_symb == "buff":
                buff_max = max(buff_max, alloc_idx[0])
        if buff_max >= 0:
            code += f"    {dtype} buff[{buff_max+1}];\n"
        if any(len(e) >= 3 for _, e in self._code):
            code += f"    {dtype} tmp;\n"

        # main code
        for (alloc_symb, alloc_idx), elements in self._code:
            match len(elements):
                case 1:
                    comp = assign(*elements[0])
                    code += f"    {assign(alloc_symb, alloc_idx)} = {comp};\n"
                case 2:
                    comp = f"OP({assign(*elements[0])}, {assign(*elements[1])})"
                    code += f"    {assign(alloc_symb, alloc_idx)} = {comp};\n"
                case _:
                    code += f"    tmp = OP({assign(*elements[0])}, {assign(*elements[1])});\n"
                    for symb, idx in elements[2:-1]:
                        code += f"    tmp = OP(tmp, {assign(symb, idx)});\n"
                    code += f"    {assign(alloc_symb, alloc_idx)} = OP(tmp, {assign(*elements[-1])});\n"
        # exit
        code += "    return EXIT_SUCCESS;\n"
        code += "}"
        return code

    def compile_c_valid(self, dtype: str="npy_float") -> str:
        """Manage the edges effects."""
        # header
        dim = self._kernel.dim
        code = (
            "int morpho_valid(\n"
            f"    PyArrayObject* dst,  // the output {dim}nd array, it can be an alias of src\n"
            f"    PyArrayObject* src  // the input {dim}nd array\n"
            ") {\n"
        )
        tab = "    "
        for i, (e_min, e_max) in enumerate(self.borders_size()):
            code += (
                f"{tab}for ( long int a{i} = {e_min}; "
                f"a{i} < PyArray_DIM(src, {i}) - {e_max+self._patch_shape[i]}; "
                f"a{i} += {self._patch_shape[i]} ) {{\n"
            )
            tab += "    "
        code += f"{tab}morpho_patch(dst, src, {', '.join(f'a{i}' for i in range(dim))});\n"
        for i in range(dim):
            tab = tab[4:]
            code += f"{tab}}}\n"

        code += "    return EXIT_SUCCESS;\n"
        code += "}"
        return code

    def compile_c_main(self) -> str:
        """Fill the c code template."""
        root = get_project_root()
        with open(root / "template.c", "r", encoding="utf-8") as file:
            code = file.read()
        code = code.replace("{dim}", str(self._kernel.dim))
        code = code.replace("{morpho_valid}", self.compile_c_valid())
        code = code.replace("{morpho_patch}", self.compile_c_patch())

        print(code)

        import tempfile
        import uuid
        import sys
        import pathlib
        import importlib
        import subprocess
        name = f"morpho_{uuid.uuid4().hex}"
        filename = pathlib.Path(tempfile.gettempdir()) / f"{name}.so"
        comp_rules = get_compilation_rules()
        gcc_insructions = [
            "gcc",
            "-o", str(filename),  # output file
            "-xc", "-",  # c language, no link, from stdin
            "-Wall",  # display all warnings
            "-pipe",  # use RAM rather than tempfile
            "-fPIC",  # emit position-independent code
            "-shared",  # produce a shared object which can then be linked with other objects
            f"-L{sys.base_prefix}/lib",
            f"-I{sys.base_prefix}/include/python{sys.version_info.major}.{sys.version_info.minor}",
            *(f"-D{mac_in}={mac_out}" for mac_in, mac_out in comp_rules["define_macros"]),
            *(f"-I{inc}" for inc in comp_rules["include_dirs"]),  # extra include
            *comp_rules["extra_compile_args"],
        ]
        try:
            subprocess.run(
                gcc_insructions, input=code.encode("utf-8"), check=True, capture_output=False
            )
        except subprocess.CalledProcessError as err:
            raise RuntimeError("failed to compile the C code with gcc", code) from err


        # import
        spec = importlib.util.spec_from_file_location("morpho", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # clean
        filename.unlink()

        return module.morpho


    def borders_size(self) -> list[tuple[int, int]]:
        """Return the borders size."""
        edges = [(0, 0) for _ in range(self._kernel.dim)]
        for _, elements in self._code:
            for var, idx in elements:
                if var == "src":
                    edges = [(max(e1, -c), max(e2, c)) for (e1, e2), c in zip(edges, idx)]
        edges = [(e1, max(0, e2-s+1)) for (e1, e2), s in zip(edges, self._patch_shape)]
        return edges

    def __str__(self) -> str:
        """Print the source code close to the numpy style."""
        lines: list[str] = []
        for (alloc_symb, alloc_idx), elements in self._code:
            comp = " | ".join(f"{symb}{list(idx)}" for symb, idx in elements)  # \u2a01
            lines.append(f"{alloc_symb}{list(alloc_idx)} = {comp}")
        return "\n".join(lines)


if __name__ == "__main__":
    n = 51
    d = 2
    ker = [1]*n
    for _ in range(d-1):
        ker = [ker]*n
    # ker = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

    code_obj = MorphCode(Kernel(ker))
    code_obj.cse().limit_buff()
    morpho = code_obj.compile_c_main()

    print("testing...")
    import numpy as np
    src = np.random.rand(720, 1080).astype(np.float32)
    src[500:550, 600:650] = 1.0
    dst = morpho(src)
    print(dst)

    import matplotlib.pyplot as plt
    plt.imshow(src, cmap="gray", vmin=0, vmax=1)
    plt.savefig("src.png")
    plt.show()
    plt.imshow(dst, cmap="gray", vmin=0, vmax=1)
    plt.savefig("dst.png")
    plt.show()



