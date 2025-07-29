# src/airoh/datalad.py
from invoke import task
import os
import shlex
import shutil
from pathlib import Path

@task
def get_data(c, name):
    """
    Ensure a Datalad subdataset is installed and retrieved.

    Parameters:
        name (str): Name of the dataset as defined in invoke.yaml under 'datasets'.
    """
    datasets = c.config.get("datasets", {})
    if name not in datasets:
        raise ValueError(f"❌ Dataset '{name}' not found in invoke.yaml under 'datasets'.")

    path = datasets[name]
    print(f"📦 Checking dataset '{name}' at: {path}")

    if not os.path.exists(path):
        print(f"📥 Installing subdataset '{name}'...")
        c.run(f"datalad install --recursive {path}")

    print(f"📥 Retrieving data for '{name}'...")
    c.run(f"datalad get {path}")
    print("✅ Done.")

@task
def import_file(c, name):
    """
    Download a file using its name from invoke.yaml -> files.<name>.

    Parameters:
        name (str): Key from the 'files' section in invoke.yaml.
    """
    files = c.config.get("files", {})
    if name not in files:
        raise ValueError(f"❌ No file config found for '{name}' in invoke.yaml.")

    entry = files[name]
    url = entry.get("url")
    output_file = entry.get("output_file")

    if not url or not output_file:
        raise ValueError(f"❌ Entry for '{name}' must define both 'url' and 'output_file'.")

    output_path = Path(output_file)
    if output_path.exists():
        print(f"🫧 Skipping {name}: {output_file} already exists.")
        return

    c.run(f"datalad download-url -O {shlex.quote(output_file)} {shlex.quote(url)}")
    print(f"✅ Downloaded {name} to {output_file}")

@task
def import_archive(c, url, archive_name=None, target_dir=".", drop_archive=False):
    """
    Download a remote archive (e.g. from Zenodo or Figshare) and extract its content with Datalad.

    Parameters:
        url (str): URL to the archive (e.g. .zip, .tar.gz). For Figshare-style links, explicitly provide
                   `archive_name` if the URL does not end with the actual filename.
        archive_name (str): Optional filename (default: basename of URL).
        target_dir (str): Directory to extract into (default: current dir).
        drop_archive (bool): Whether to drop the original archive from annex after extraction.
    """
    archive_name = archive_name or os.path.basename(url)
    archive_path = os.path.join(target_dir, archive_name)

    import_file(c, url, archive_path)

    archive_exts = ['.zip', '.tar', '.tar.gz', '.tgz', '.tar.bz2', '.7z']
    if not any(archive_path.endswith(ext) for ext in archive_exts):
        print("⚠️ Skipping extraction — file does not appear to be a supported archive.")
        return

    print(f"📦 Extracting archive content into {target_dir}...")
    c.run(f"datalad add-archive-content --delete --extract {shlex.quote(archive_path)} -d {shlex.quote(target_dir)}")

    if drop_archive:
        print(f"🧹 Dropping archive from annex: {archive_path}")
        c.run(f"datalad drop {shlex.quote(archive_path)}")

    print("✅ Archive import complete.")
