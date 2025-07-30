from cleo.commands.command import Command
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option
from poetry.plugins.application_plugin import ApplicationPlugin


NAME = 'aws-login'


class LoginCommand(Command):

    name = NAME

    arguments = [
        Argument(
            'source',
            description='The repository source to authenticate with. This will '
                        'be the <c2>"name"</c2> field of the <c2>"tool.poetry.source"</c2> entry.',
        ),
    ]

    options = [
        Option(
            'domain',
            flag=False,
            description='The AWS CodeArtifact <c2>domain</c2> to authenticate with.',
        ),
        Option(
            'repository',
            flag=False,
            description='The AWS CodeArtifact <c2>repository</c2> to authenticate with.',
        ),
        Option(
            'profile',
            flag=False,
            description='The AWS <c2>profile</c2> to use for authentication.',
        ),
        Option(
            'region',
            flag=False,
            description='The AWS <c2>region</c2> to use for authentication.',
        ),
        Option(
            'duration',
            flag=False,
            default=43200,
            description='The time, in seconds, that the generated authorization token is valid.\n'
        ),
        Option(
            'default',
            description='Whether to configure the source as the default.\n'
                        'See <c2>https://python-poetry.org/docs/repositories/'
                        '#default-package-source</c2>',
        ),
        Option(
            'secondary',
            description='Whether to configure the source as secondary.\n'
                        'See <c2>https://python-poetry.org/docs/repositories/'
                        '#secondary-package-sources</c2>',
        ),

    ]

    help = ('For most use cases, the CodeArtifact source will already be configured in the '
            'project file. In this case, you can\nsimply log in by providing the '
            '<info>source</info> argument with an optional <info>--profile</info> selection.\n\n'
            'However, if you want to create a new or update an existing CodeArtifact source '
            'entry, you can also provide\nthe <info>--domain</inf> and <info>--repository</info> '
            'arguments. When these options are provided, a new source entry will be created\nif '
            'one does not already exist for the provided <info>source</info>, otherwise it will '
            'ask if you want to update the\nexisting entry.\n\n'
            'By default, the authenticated session is valid for 12 hours. This duration can be '
            'adjusted by providing\nthe <info>--duration</info> argument. Valid values are '
            '<comment>0</comment> and any number between <comment>900</comment> (15 minutes) '
            'and <comment>43200</comment> (12 hours).\nA value of <comment>0</comment> will set '
            'the expiration of the authorization token to the same expiration of the user\'s '
            'role\'s\ntemporary credentials.')

    def handle(self) -> int:
        import re
        from typing import cast

        import boto3
        from poetry.poetry import Poetry

        poetry = cast(Poetry, self.application.poetry)  # type: ignore

        source_name: str = self.argument('source')
        domain: str | None = self.option('domain')
        repository: str | None = self.option('repository')
        profile: str | None = self.option('profile')
        region: str | None = self.option('region')
        duration: int = int(self.option('duration'))
        secondary: bool = self.option('secondary')
        default: bool = self.option('default')

        session = boto3.Session(profile_name=profile, region_name=region)
        ca_client = session.client('codeartifact')
        sts_client = session.client('sts')

        if domain:
            msg = '"--repository" must be provided when using the --domain" option.'
            assert repository is not None, msg

        if repository:
            msg = '"--domain" must be provided when using the --repository" option.'
            assert domain is not None, msg

        existing_sources = poetry.get_sources()
        existing_sources_names = [source.name for source in existing_sources]

        # Configure source if domain/repository are provided
        if domain:
            resp = ca_client.get_repository_endpoint(
                domain=domain,
                repository=repository,
                format='pypi',
            )
            endpoint = cast(str, resp['repositoryEndpoint']) + 'simple'

            requires_update = False
            requires_new = True

            # If a source already exists for the provided name, check whether it needs to be
            # overwritten
            if source_name in existing_sources_names:
                s, = [s for s in existing_sources if s.name == source_name]

                if s.url != endpoint or s.default != default or s.secondary != secondary:
                    overwrite = self.confirm(
                        f'Source entry exists for source "{source_name}", do you want to overwrite?'
                    )

                    if not overwrite:
                        self.line('Cancelled.')
                        return 0

                    # Remove existing source entry
                    source_remove_command = self.application.find('source remove')

                    self.io.input._definition.add_arguments(source_remove_command.definition.arguments)
                    self.io.input.set_argument('name', source_name)

                    source_remove_command.execute(self.io)

                    requires_update = True
                    requires_new = False
                else:
                    self.line('Source entry already exists with matching config. '
                              'Leaving sources unmodified.')

                    requires_update = False
                    requires_new = False

            if requires_update or requires_new:
                # Add new source entry
                source_add_command = self.application.find('source add')

                if not self.io.input._definition.has_argument('name'):
                    self.io.input._definition.add_argument(source_add_command.definition.argument('name'))

                self.io.input._definition.add_argument(source_add_command.definition.argument('url'))

                self.io.input.set_argument('name', source_name)
                self.io.input.set_argument('url', endpoint)

                source_add_command.execute(self.io)

                action = 'updated' if requires_update else 'created'

                self.line(f'Succesfully {action} source: {source_name}')

        # If domain/repository are not provided, log in using existing source
        if not domain:
            source = None

            for existing_source in existing_sources:
                if source_name == existing_source.name:
                    source = existing_source

            if not source:
                raise ValueError(f'No source configured for name: {source_name}')

            match = re.match(r'https://(\w+)-.*', source.url)

            if not match:
                raise ValueError(f'The URL for "{source_name}" is formatted incorrectly.')

            domain = match.group(1)

        resp = ca_client.get_authorization_token(domain=domain, durationSeconds=duration)

        username = 'aws'
        token = resp['authorizationToken']
        expiration = resp['expiration']

        config_command = self.application.find('config')

        self.io.input._definition.add_arguments(config_command.definition.arguments)
        self.io.input.set_argument('key', f'http-basic.{source_name}')
        self.io.input.set_argument('value', [username, token])

        config_command.execute(self.io)

        resp = sts_client.get_caller_identity()
        identity = {'id': resp['UserId'], 'account': resp['Account'], 'arn': resp['Arn']}

        self.line(f'Successfully logged in to {source_name}')

        if self.io.is_verbose():
            self.line(f'Identity: {identity}')
            self.line(f'Expiration: {expiration}')

        return 0


def factory():
    return LoginCommand()


class CodeArtifactPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory(NAME, factory)