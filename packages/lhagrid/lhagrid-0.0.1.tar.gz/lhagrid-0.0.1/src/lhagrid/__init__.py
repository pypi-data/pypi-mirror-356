from dataclasses import dataclass


@dataclass
class LHAGrid:
    @dataclass
    class SubGridBlock:
        x_axis: list[float]
        q_axis: list[float]
        flavour_axis: list[int]
        data: list[list[float]]  # values go q first, then x

        def from_string(data: str) -> "LHAGrid.SubGridBlock":
            lines = data.strip().split("\n")
            lines = [line for line in lines if not line.startswith("#")]
            x_axis = list(map(float, lines[0].split()))
            q_axis = list(map(float, lines[1].split()))
            flavour_axis = list(map(int, lines[2].split()))
            data_rows = [list(map(float, line.split())) for line in lines[3:]]

            assert len(flavour_axis) == len(data_rows[0]), (
                "Flavour axis length must match data row length"
            )
            assert len(q_axis) * len(x_axis) == len(data_rows), (
                f"Data rows must match q_axis {len(q_axis)} and x_axis {len(x_axis)} dimensions"
            )

            return LHAGrid.SubGridBlock(x_axis, q_axis, flavour_axis, data_rows)

        def to_string(self) -> str:
            ret = ""
            ret += " ".join(f"{v:.7E}" for v in self.x_axis) + " \n"
            ret += " ".join(f"{v:.7E}" for v in self.q_axis) + " \n"
            ret += " ".join(f"{v}" for v in self.flavour_axis) + " \n"
            for row in self.data:
                ret += " " + " ".join(f"{v: .7E}" for v in row) + "\n"
            return ret

    pdftype: str
    format: str
    subgrids: list[SubGridBlock]

    @staticmethod
    def from_string(data: str) -> None:
        blocks = data.strip().split("---")
        lines = blocks[0].strip().split("\n")
        # remove lines prefixed with '#'
        lines = [line for line in lines if not line.startswith("#")]

        pdftype = lines[0].split(":")[1].strip()
        format = lines[1].split(":")[1].strip()

        subgrids = []
        for block in blocks[1:]:
            if not block.strip():
                continue
            block_data = LHAGrid.SubGridBlock.from_string(block)
            subgrids.append(block_data)

        return LHAGrid(pdftype, format, subgrids)

    @staticmethod
    def from_file(filename: str) -> "LHAGrid":
        with open(filename, "r") as f:
            data = f.read()
        return LHAGrid.from_string(data)

    def to_string(self) -> str:
        ret = ""
        ret += f"PdfType: {self.pdftype}\n"
        ret += f"Format: {self.format}\n"
        ret += "---\n"
        for subgrid in self.subgrids:
            ret += subgrid.to_string()
            ret += " ---\n"
        return ret

    def to_file(self, filename: str) -> None:
        with open(filename, "w") as f:
            f.write(self.to_string())
