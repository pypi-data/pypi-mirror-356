# Poetry AWS CodeArtifact Login
A Poetry plugin for authenticating with AWS CodeArtifact.

## Requirements
- `poetry >= 1.2.0`
Install using the dedicated installation script. See [here](https://python-poetry.org/docs/#installation). 

- `AWS CLI v2`
See [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) for installation guide.


## Intallation
```
poetry self add poetry-codeartifact-login
```

## Usage
AWS credentials will need to be configured on the system prior to usage. Typically this is done using the `aws configure` command and/or directly modifying the configuration files. See [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for more info. They can also be set through [environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html), which will take precedence over any configuration file values.

Once credentials have been configured, you can log in to CodeArtifact:
```
poetry aws-login <source_name>
```

Assuming the credentials are configured properly and the identity they belong to has proper permissions, `poetry` will be configured with a short-lived authentication token that will automatically be used for installation of any packages in the authenticated source. See [here](https://python-poetry.org/docs/repositories/#private-repository-example) for more information on working with private repositories through `poetry`.

If want to log in with a profile other than the default, you can do:
```
poetry aws-login <source_name> --profile <profile_name>
```

## CLI Reference
```
poetry aws-login --help
```
