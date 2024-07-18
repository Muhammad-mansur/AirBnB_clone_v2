from fabric.api import *
from fabric.contrib.files import exists

env.user = "mansur"
env.hosts = ["52.3.246.184", "100.25.15.100"]

def do_deploy(archive_path):
  """
  Deploys the archive to the web servers.

  Args:
      archive_path: Path to the archive file.

  Returns:
      True if successful, False otherwise.
  """
  if not exists(archive_path):
    print(f"Archive file {archive_path} does not exist.")
    return False

  # Upload archive to /tmp/ on web servers
  with settings(warn_only=True):
    result = put(archive_path, remote="/tmp/")
  if not result.succeeded:
    print("Failed to upload archive.")
    return False

  # Extract archive to release directory
  filename = os.path.basename(archive_path).split(".")[0]
  remote_dir = f"/data/web_static/releases/{filename}"
  run(f"tar -xzf /tmp/{os.path.basename(archive_path)} -C {remote_dir}")

  # Delete archive
  run(f"rm /tmp/{os.path.basename(archive_path)}")

  # Delete existing current symlink
  with settings(warn_only=True):
    run(f"rm /data/web_static/current")

  # Create new symlink to released version
  run(f"ln -s {remote_dir} /data/web_static/current")

  print("Deployment successful!")
  return True

# Example usage with SSH key argument
# fab do_deploy:archive_path=path/to/your/archive.tar.gz

if __name__ == "__main__":
  # You can add additional arguments parsing here if needed
  pass
