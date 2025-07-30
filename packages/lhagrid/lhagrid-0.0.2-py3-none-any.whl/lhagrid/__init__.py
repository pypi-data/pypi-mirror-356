import ast
from dataclasses import dataclass


@dataclass
class LHAGrid:
    @dataclass
    class SubGridBlock:
        x_axis: list[float]
        q_axis: list[float]
        flavour_axis: list[int]
        data: list[list[float]]  # values go q first, then x

        def validate(self) -> None:
            if len(self.flavour_axis) != len(self.data[0]):
                raise ValueError("Flavour axis length must match data row length")
            if len(self.q_axis) * len(self.x_axis) != len(self.data):
                raise ValueError(
                    f"Data rows must match q_axis {len(self.q_axis)} and x_axis {len(self.x_axis)} dimensions"
                )

        @staticmethod
        def from_string(data: str, validate=True) -> "LHAGrid.SubGridBlock":
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

            grid = LHAGrid.SubGridBlock(x_axis, q_axis, flavour_axis, data_rows)
            if validate:
                grid.validate()
            return grid

        def to_string(self, validate=True) -> str:
            if validate:
                self.validate()
            ret = ""
            ret += " ".join(f"{v:.7E}" for v in self.x_axis) + " \n"
            ret += " ".join(f"{v:.7E}" for v in self.q_axis) + " \n"
            ret += " ".join(f"{v}" for v in self.flavour_axis) + " \n"
            for row in self.data:
                ret += " " + " ".join(f"{v: .7E}" for v in row) + "\n"
            return ret

    PdfType: str
    Format: str
    subgrids: list[SubGridBlock]

    def validate(self) -> None:
        if not self.subgrids:
            raise ValueError("At least one subgrid must be present")
        for subgrid in self.subgrids:
            subgrid.validate()
        # Additional validation can be added here if needed

    @staticmethod
    def from_string(data: str, validate=True) -> None:
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
            block_data = LHAGrid.SubGridBlock.from_string(block, validate=validate)
            subgrids.append(block_data)

        grid = LHAGrid(pdftype, format, subgrids)
        if validate:
            grid.validate()
        return grid

    @staticmethod
    def from_file(filename: str, validate=True) -> "LHAGrid":
        with open(filename, "r") as f:
            data = f.read()
        return LHAGrid.from_string(data, validate=validate)

    def to_string(self, validate=True) -> str:
        if validate:
            self.validate()
        ret = ""
        ret += f"PdfType: {self.PdfType}\n"
        ret += f"Format: {self.Format}\n"
        ret += "---\n"
        for subgrid in self.subgrids:
            ret += subgrid.to_string(validate)
            ret += " ---\n"
        return ret

    def to_file(self, filename: str, validate=True) -> None:
        with open(filename, "w") as f:
            f.write(self.to_string(validate=validate))


@dataclass
class LHAInfo:
    SetDesc: str
    SetIndex: int
    Authors: str
    Reference: str
    Format: str
    DataVersion: str
    NumMembers: int
    Particle: int
    Flavors: list[int]
    OrderQCD: int
    FlavorScheme: str
    NumFlavors: int
    ErrorType: str
    XMin: float
    XMax: float
    QMin: float
    QMax: float
    MZ: float
    MUp: float
    MDown: float
    MStrange: float
    MCharm: float
    MBottom: float
    MTop: float
    AlphaS_MZ: float
    AlphaS_OrderQCD: int
    AlphaS_Type: str
    AlphaS_Qs: list[float]
    AlphaS_Vals: list[float]
    AlphaS_Lambda4: float
    AlphaS_Lambda5: float

    @staticmethod
    def from_file(filename: str, validate=True) -> "LHAInfo":
        with open(filename, "r") as f:
            data = f.read()
        return LHAInfo.from_string(data, validate=validate)

    @staticmethod
    def from_string(data: str, validate=True) -> "LHAInfo":
        lines = data.strip().split("\n")
        info = {}
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()

        # Use explicit cases in the info dict access
        return LHAInfo(
            SetDesc=info["SetDesc"],
            SetIndex=int(info["SetIndex"]),
            Authors=info["Authors"],
            Reference=info["Reference"],
            Format=info["Format"],
            DataVersion=info["DataVersion"],
            NumMembers=int(info["NumMembers"]),
            Particle=int(info["Particle"]),
            Flavors=ast.literal_eval(info["Flavors"]),
            OrderQCD=int(info["OrderQCD"]),
            FlavorScheme=info["FlavorScheme"],
            NumFlavors=int(info["NumFlavors"]),
            ErrorType=info["ErrorType"],
            XMin=float(info["XMin"]),
            XMax=float(info["XMax"]),
            QMin=float(info["QMin"]),
            QMax=float(info["QMax"]),
            MZ=float(info["MZ"]),
            MUp=float(info["MUp"]),
            MDown=float(info["MDown"]),
            MStrange=float(info["MStrange"]),
            MCharm=float(info["MCharm"]),
            MBottom=float(info["MBottom"]),
            MTop=float(info["MTop"]),
            AlphaS_MZ=float(info.get("AlphaS_MZ", 0.0)),
            AlphaS_OrderQCD=int(info.get("AlphaS_OrderQCD", 0)),
            AlphaS_Type=info.get("AlphaS_Type", ""),
            AlphaS_Qs=ast.literal_eval(info.get("AlphaS_Qs", "")),
            AlphaS_Vals=ast.literal_eval(info.get("AlphaS_Vals", "")),
            AlphaS_Lambda4=float(info.get("AlphaS_Lambda4", 0.0)),
            AlphaS_Lambda5=float(info.get("AlphaS_Lambda5", 0.0)),
        )
