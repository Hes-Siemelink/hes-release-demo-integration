# xlr-container-python-template

This project serves as a template for developing a Python-based container plugin.

## SDK Project

This sample project is based on the SDK base defined here:  

https://github.com/xebialabs/xlr-container-python-sdk

The SDK is available for testing at test.pypi.org:  

https://test.pypi.org/project/digitalai

## How to create your own project

Create a duplicate of this project to start developing your own container-based integration. 

Use the [instructions from GitHub](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository). Note: this creates a duplicate, not a fork.

This should also work for other flavors of Git.


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

Run the build script 

Unix/macOS

* Builds the jar, image and pushes the image to the configured registry  
``` sh build.sh ``` 
* Builds the jar  
``` sh build.sh --jar ``` 
* Builds the image and pushes the image to the configured registry  
 ```  sh build.sh --image ``` 

Windows

* Builds the jar, image and pushes the image to the configured registry  
``` build.bat ``` 
* Builds the jar  
``` build.bat --jar ``` 
* Builds the image and pushes the image to the configured registry  
``` build.bat --image ```

### 7. Install plugin into Release

In Release UI, use the Plugin Manager interface to upload the jar from `build/libs`

Then:
   * Restart Release container
   * Refresh the UI by pressing Reload in the browser.


### 8. Test it!
Create a template with the task **Container Template: API Example** and run it!

### 9. Run the unit test

Unix/macOS

    python3 -m unittest tests/test_tasks.py

Windows

    py -m unittest tests\test_tasks.py




