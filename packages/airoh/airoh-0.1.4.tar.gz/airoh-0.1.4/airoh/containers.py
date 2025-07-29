# src/airoh/containers.py
import os
import shutil
import tempfile
import gzip
from pathlib import Path
from invoke import task

def _set_image(c, image=None):
    """
    Resolve the Docker image name from parameter or invoke.yaml.
    """
    image = image or c.config.get("docker_image")
    if not image:
        raise ValueError("No Docker image specified. Please set docker_image in invoke.yaml or pass it explicitly.")
    return image

@task
def docker_build(c, image=None, no_cache=False):
    """
    Build the Docker image from the Dockerfile in the project root.
    """
    image = _set_image(c, image)
    cache_flag = "--no-cache" if no_cache else "" 
    print(f"🐳 Building Docker image: {image}")
    c.run(f"docker build {cache_flag} -t {image} .")

@task
def docker_archive(c, image=None):
    """
    Save the Docker image to a compressed archive for Zenodo or transport.
    """
    image = _set_image(c, image)
    output = f"{image}.tar.gz"
    print(f"📦 Archiving Docker image '{image}' to {output}...")
    c.run(f"docker save {image} | gzip > {output}")
    print("🪦 Archive complete.")

@task
def docker_setup(c, url=None, image=None):
    """
    Download and load the prebuilt Docker image from Zenodo.
    """
    image = _set_image(c, image)
    if not url:
        url = c.config.get("docker_archive")
        if not url:
            raise ValueError("No archive URL provided. Set docker_archive in invoke.yaml or pass --url.")

    output = f"{image}.tar.gz"
    if not os.path.exists(output):
        print(f"📥 Downloading container from {url}...")
        c.run(f"wget -O {output} '{url}'")
    else:
        print(f"📦 Container archive already exists: {output}")

    print("🐳 Loading Docker image...")
    c.run(f"gunzip -c {output} | docker load")
    print("✨ Container setup complete.")

def _ensure_docker_image_loaded(c, image, image_tar):
    """
    Ensure the specified Docker image is available. If not, try to load it from a .tar or .tar.gz.
    """
    if not shutil.which("docker"):
        raise RuntimeError("❌ Docker is not installed or not in PATH. Please install Docker.")

    result = c.run(f"docker images -q {image}", hide=True, warn=True)
    if result.stdout.strip():
        c.run(f"docker tag {image} {image}:latest", warn=True)
        return

    print(f"📦 Docker image '{image}' not found. Attempting to load from {image_tar}...")

    image_tar = Path(image_tar)
    if not image_tar.exists():
        raise FileNotFoundError(f"❌ Docker image file not found: {image_tar}")

    if image_tar.suffixes[-2:] == ['.tar', '.gz']:
        print(f"🖜️ Extracting {image_tar}...")
        with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as temp_tar:
            with gzip.open(image_tar, "rb") as f_in:
                shutil.copyfileobj(f_in, temp_tar)
            temp_tar_path = temp_tar.name
        c.run(f"docker load -i {temp_tar_path}")
        os.remove(temp_tar_path)
    elif image_tar.suffix == ".tar":
        c.run(f"docker load -i {image_tar}")
    else:
        raise ValueError("❌ Unsupported container format. Use .tar or .tar.gz")

    c.run(f"docker tag {image} {image}:latest", warn=True)

@task
def docker_run(c, task, args=""):
    """
    Run an invoke task inside the Docker container.

    Args:
        task (str): the invoke task to run
        args (str): any additional CLI args to pass to the task
    """
    image = c.config.get("docker_image")
    image_tar = f"{image}.tar.gz"

    _ensure_docker_image_loaded(c, image, image_tar)

    hostdir = os.getcwd()
    workdir = "/home/jovyan/work"
    cmd = f"invoke {task} {args}"
    docker_cmd = f'docker run --rm -v {hostdir}:{workdir} -w {workdir} {image} {cmd}'

    print(f"🐳 Running inside container: {cmd}")
    c.run(docker_cmd)

@task
def apptainer_archive(c, image=None):
    """
    Archive the Apptainer (Singularity) image from a Docker image using Docker daemon.
    Builds the .sif file if not present.
    """
    image = _set_image(c, image)
    sif_path = Path(f"{image}.sif")

    if not shutil.which("apptainer"):
        raise RuntimeError("❌ Apptainer is not installed or not in PATH. Please install it.")

    if sif_path.exists():
        print(f"✅ Apptainer image already exists at {sif_path}. Skipping build.")
        return

    if not shutil.which("docker"):
        raise RuntimeError("❌ Docker is required to build from Docker image. Please install it.")

    _ensure_docker_image_loaded(c, image, f"{image}.tar.gz")
    print(f"🧪 Building Apptainer image {sif_path} from Docker image {image}:latest...")
    c.run(f"apptainer build {sif_path} docker-daemon:{image}:latest")
    print("✅ Apptainer image build complete.")

@task
def apptainer_run(c, task, args=""):
    """
    Run an invoke task inside the Apptainer container.

    Args:
        task (str): the invoke task to run
        args (str): any additional CLI args to pass to the task
    """
    docker_image = c.config.get("docker_image")
    sif_path = Path(f"{docker_image}.sif")

    if not sif_path.exists():
        raise FileNotFoundError(f"❌ Apptainer image not found: {sif_path}")

    hostdir = os.getcwd()
    workdir = "/home/jovyan/work"
    cmd = f"invoke {task} {args}"
    apptainer_cmd = f"apptainer exec --cleanenv --bind {hostdir}:{workdir} {sif_path} {cmd}"

    print(f"🧪 Running inside Apptainer: {cmd}")
    c.run(apptainer_cmd)
