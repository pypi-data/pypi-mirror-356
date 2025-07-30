"""Model Jacket CLI - build and serve models easily."""
import argparse
import subprocess
import pathlib
import shutil
import sys
from textwrap import dedent

from jacket_cli.utils import build_docker_image


def _parse_args():
    parser = argparse.ArgumentParser("jacket")
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="Build a container for a model")
    build.add_argument("--framework", required=True, choices=["torch", "onnx", "sklearn"], help="Model framework")
    build.add_argument("--model-path", required=True, help="Path to model artifact")
    build.add_argument("--tag", default="latest", help="Image tag")
    build.add_argument("--repo", default="model-jacket", help="Image repository")

    serve = sub.add_parser("serve", help="Run locally for testing")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--model-path", required=True)

    return parser.parse_args()

    return parser.parse_args()

def cmd_build(args):
    model_path = pathlib.Path(args.model_path).resolve()
    build_dir = pathlib.Path("build").absolute()
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)

    # copy runtime and model
    shutil.copytree(pathlib.Path(__file__).parent.parent / "runtime", build_dir / "runtime")
    (build_dir / "models").mkdir()
    shutil.copy(model_path, build_dir / "models" / model_path.name)

    # write Dockerfile
    dockerfile = build_dir / "Dockerfile"
    dockerfile.write_text(dedent(f"""
        FROM python:3.10-slim

        WORKDIR /app
        COPY runtime runtime
        COPY models /models
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt

        ENV MODEL_PATH=/models/{model_path.name}
        ENV MODEL_FRAMEWORK={args.framework}

        CMD [\"uvicorn\", \"runtime.api.main:app\", \"--host=0.0.0.0\", \"--port=8000\"]
    """))

    # copy requirements
    shutil.copy(pathlib.Path(__file__).parent.parent / "requirements.txt", build_dir / "requirements.txt")

    build_docker_image(str(build_dir), f"{args.repo}:{args.tag}")

def cmd_serve(args):
    subprocess.run([
        sys.executable,
        "-m",
        "uvicorn",
        "runtime.api.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(args.port),
    ])

def main():
    args = _parse_args()
    if args.command == "build":
        cmd_build(args)
    elif args.command == "serve":
        cmd_serve(args)


if __name__ == "__main__":
    main()