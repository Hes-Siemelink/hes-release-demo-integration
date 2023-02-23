# SDK tutorial outline

## Welcome 

_The tutorial has a welcome section outlining the basic architecture_

_Topics covered:_
* _Tasks are run as containers. This allows you to write Release tasks using any language. We have support for Python3 and Go (soon) in the SDK_
* _SDK provides the tools to create container-based tasks_
* _Architecture: Release instance + Remote Runner_
* _Tasks are developed as container + traditional plugin jar containing metadata_

## Hello World plugin

### Code & test

_Tutorial walks you through setting up a Python 3 project_

_Explains how to create a git project from template_

_(Optional) Explains how to set up IDE_

_Explains how to run local tests_

_(Optional) Explains how to run integration tests in container test framework_

### Build & Run

_Explains how to package a plugin_

_Explains how to install Remote Runner into an existing Kubernetes environment using xl kube install_
* _Configure Release and create token_
* _Launch Remote Runner_
* _Check if it self-registers in Release_

_Explains how to install plugin jar into Release_

_Explains how to publish container to be picked up by Remote Runner_

_Explains how to create a template and run_

_Explains how to troubleshoot if task isn’t picked up_

## Integration plugin

### Jenkins plugin guided tour
* _How to define a Server_
* _How to use secrets and communicate with a third-party server_
* _How to model a long-running task using Python3 constructs_
* _How to do status line updates and task comments_
* _How to use live logging_

### Other features
* _How to access the Release API with bundled endpoints_

## Demo

_Show Release Onboarding flow_

_This highlights the following new tasks_
* _Webhook task with Oauth2 (not a container task but very useful) to interact with Digital.ai Platform API_
* _Create secrets in Vault and use either secrets directly or Vault reference_
* _Kubernetes and Kustomize tasks_
* _Postgresql task_
* _Keytool task_
* _XL apply task_

_Tasks that use API libraries (Kubernetes) or command-line tools (xl-cli, postgres, kustomize) used to be virtually impossible to create._

_Maybe rewrite to install a different Kubernetes app, not Release, to prevent ‘meta-level’ speak of using a “release in Release to create an instance of Release”_
