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

This section describes the quickest way to get a setup with Release to test containerized plugins. This is not a production setup. For production, please use the [Remote Runner](doc/remote-runner-quickstart.md) to run container tasks.

The Quickstart assumes you have the following installed:

* Git
* Docker

For detailed installation instructions, refer to the [Setup document](doc/setup.md).

You can do this quickstart on this template repository, or [create your own repository](#how-to-create-your-own-project) first. 

### 1. Start Release

We will run Release within a local Docker environment. Release will take care of running the containerized tasks in Docker. For production, you would use the Remote Runner inside Kubernetes to manage that.

Start the Release environment with the following command 

    docker compose up -d --build

### 2. Configure your `hosts` file

The Release server needs to be able to find the container images of the integration you are creating. In order to do so the Development setup has a registry running inside Docker. Add the address of the registry to your local machine's `hosts` file.

Add the following entries to `/etc/hosts`:

    127.0.0.1 digitalai.release.local
    127.0.0.1 xlr-registry

XXX Add: instructions for Linux / MacOS and Windows and mention that you need sudo privileges to edit

### 3. Build & publish the plugin

Run the build script 

Unix/macOS

* Builds the jar, image and pushes the image to the configured registry  
``` sh build.sh ``` 

Windows

* Builds the jar, image and pushes the image to the configured registry  
``` build.bat ``` 

### 4. Install plugin into Release

In Release UI, use the Plugin Manager interface to upload the jar from `build`.
The jar takes the name of the project, for example `release-integration-template-python-1.0.0.jar`.

Then:
   * Restart Release container and wait for it to come up
   * Refresh the UI by pressing Reload in the browser.

### 5. Test it!
Create a template with the task **Example: Hello** and run it!

### 6. Clean up

Stop the development environment with the following command:

    docker compose down


## How to create your own project

Create a **duplicate** of this project to start developing your own container-based integration. Note: Please do _not_ create a fork.

### Create a new repository

Before you duplicate the contents of this repository, you already need the new repository to push to.

Use the following naming convention:

    [company]-release-[target]-integration

For example: `acme-release-jenkins-integration`

Now initialize the Git repository with this name and note the url.

* Instructions to [create a repository on GitHub](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)

### Clone and duplicate

1. Open Terminal.
2. Create a bare clone of this repository.

```commandline
git clone --bare https://github.com/xebialabs/release-integration-template-python.git release-integration-temp
```

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