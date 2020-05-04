# mkc - a tool to Make K8s Charm

This tool will generate a basic k8s charm using the Operator Framework, from a
template.

Some charms simply boil down to, or get started with, a basic pod spec which
turns juju config items into environment variables:

    def configure_pod(self, event):
    [...]
        self.model.pod.set_spec({
            'containers': [{
                'name': self.framework.model.app.name,
                'imageDetails': self.app_image.fetch()
                'ports': [{
                    'containerPort': int(self.framework.model.config['application_port']),
                    'protocol': 'TCP',
                }],
                'config': {
                    'ENV_VAR1': config['env_var1'],
                    'ENV_VAR2': config['env_var2'],
                },
            }]
        })

This tool will implement that, taking as input a yaml file describing only the
things which are specific to each charm.

Example:

```yaml
application: myapp
variables:
    config1:
        envvar: ENV_VAR1
        juju_config: |
            type: boolean
            description: first var
            default: true
    config2:
        envvar: ENV_VAR2
        juju_config: |
            type: int
            description: second var
            default: 42
readme: |
    # MyApp Charm
    The charm deploys myapp, a really cool app, on kubernetes using the Operator Framework.
```

```
$ ./mkc.py -c myapp.yaml -t templates/
Creating skeleton tree ...
../myapp-k8s-charm
../myapp-k8s-charm/hooks
../myapp-k8s-charm/lib
../myapp-k8s-charm/mod
../myapp-k8s-charm/src
Adding submodules ...
Generating symlinks ...
Making initial commit.
Done creating skeleton structure for ../myapp-k8s-charm
Rendering ../myapp-k8s-charm/charm.py ...
Rendering ../myapp-k8s-charm/config.yaml ...
Rendering ../myapp-k8s-charm/metadata.yaml ...
Rendering ../myapp-k8s-charm/README.md ...
Committing generated charm ...
Done.
```

From there, the charm can be improved to add more advanced features such as
relations.
