# xlr-container-python-template

This project serves as a template for developing a Python-based container plugin.

## SDK Project

This sample project is based on the SDK base defined here:  
https://github.com/xebialabs/xlr-container-python-sdk

The SDK is available for testing at test.pypi.org:  
https://test.pypi.org/project/dai-release-sdk/


## How to run 

_**Work in progress:** these notes reflect the current state for developing plugins internally in Digital.ai_


### 1. Install / start K3s
Follow instructions here: https://github.com/xebialabs/xlr-remote-runner/wiki/Local-k3d-setup

### 2. Configure registry in Docker

Start k3d with registry: 

   k3d cluster create xlrcluster --volume <local path>:/kube --registry-create xlr-registry:5050

Add to `/etc/hosts`:

    127.0.0.1 xlr-registry
     
### 3. Set up the runner

Manually build and publish from `xebialabs/xlr-remote-runner` repo

    ./gradlew clean build jib -Pregistry=k3d

Make a note of the current version number of the image.

Copy `xlr-remote-runner/doc/docker-setup/docker-compose.yaml` to a local folder and set correct image, for example

```yaml
xlr-remote-runner:
  image: xlr-registry:5050/digitalai/xlr-remote-runner:0.1.22
```

### 4. Run Release

Start the Release application

    docker run --name xl-release -e ADMIN_PASSWORD=admin -e ACCEPT_EULA=Y -p 5516:5516 xebialabsunsupported/xl-release:23.1

### 5. Conect Remote Runner to Release 

Create PAT token for admin in Release under user settings.

Configure the PAT token as an environment variable:

    export REMOTE_RUNNER_TOKEN=rpa...

Start the Remote Runner with

    docker compose up

Check the remote runner logs to see if it started correctly and is able to connect to Release.
  
In the Release UI, check the **Connections** page for Remote Runner connections.

### 6. Create plugin container

On the plugin project, run the build with 

    ./gradlew clean build

This will create the plugin jar and publish the image to `xlr-registry:5050`.

### 7. Install plugin into Release

In Release UI, use the Plugin Manager interface to upload the jar from `build/libs`

Then:
   * Restart Release container
   * Refresh the UI by pressing Reload in the browser.


### 8. Test it!
Create a template with the task **Container Template: API Example** and run it!


