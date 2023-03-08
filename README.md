# Template Project for Digital.ai Release Integrations 

This project serves as a template for developing a Python-based container plugin.

## Topics

* [Prerequisites and setup](doc/setup.md)
* [Quickstart](#quickstart) (in this document)
* [How to create your own project](#how-to-create-your-own-project) (in this document)
* [Tutorial](doc/tutorial.md)
* [Reference](doc/reference.md)
* [Guided tour: the Jenkins plugin](doc/jenkins-guided-tour.md)



## Quickstart 

This section describes the quickest way to get a container-based Release task up and running. Refer to the other materials for more in-depth explanations.

The Quickstart assumes you have the following installed already:

* Python 3
* Git
* Docker

For detailed installation instructions, refer to the [Setup document](doc/setup.md).

You can do this quickstart on this template repository, or [create your own repository](#how-to-create-your-own-project) first. 

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
Create a template with the task **Example: Hello** and run it!

### 9. Run the unit test

Unix/macOS

    python3 -m unittest discover tests

Windows

    py -m unittest discover tests


## How to create your own project

Create a duplicate of this project to start developing your own container-based integration. Note: Please do not create a fork.

### Step 1 - Create a new repository

Before you duplicate the contents of this repository, you already need the new repository to push to.

Use the following naming convention:

    [company]-release-[target]-integration

For example:

    acme-release-jenkins-integration

Now initialize the Git repository with this name and note the url.

* Instructions to [create a repository on GitHub](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)

### Step 2 - Clone and duplicate

1. Open Terminal.
2. Create a bare clone of this repository.

    git clone --bare https://github.com/xebialabs/release-integration-template-python.git release-integration-temp

3. Mirror-push to the new repository.

```commandline
cd release-integration-template-python
git push --mirror [URL of your new repo]
```

4. Remove the temporary local repository you created earlier.

```commandline
cd ..
rm -rf release-integration-temp
```


