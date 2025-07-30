import subprocess

def build_docker_image(build_context: str, image_tag: str):
    cmd = ["docker", "build", "-t", image_tag, build_context]
    subprocess.run(cmd, check=True)
