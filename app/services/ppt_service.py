from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "ppt-engine"
OUTPUT = ROOT / "output"


def build_ppt(markdown: str, filename: str = "report") -> str:
    OUTPUT.mkdir(exist_ok=True)

    md_file = OUTPUT / f"{filename}.md"
    ppt_file = OUTPUT / f"{filename}.pptx"

    md_file.write_text(markdown, encoding="utf-8")

    subprocess.run(
        [
            "node",
            "build.js",
            str(md_file),
            str(ppt_file),
        ],
        cwd=ENGINE,
        check=True,
    )

    return str(ppt_file)