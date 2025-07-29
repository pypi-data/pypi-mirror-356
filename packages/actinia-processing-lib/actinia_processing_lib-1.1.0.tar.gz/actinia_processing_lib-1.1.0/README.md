# actinia-processing-lib

This is the processing library for [actinia-core](https://github.com/mundialis/actinia_core).

It is a requirement of actinia-core and some actinia plugins and not meant to be used standalone.


## DEV setup
For a DEV setup integrated with other actinia components, see [here](https://github.com/actinia-org/actinia-docker#local-dev-setup-for-actinia-core-plugins-with-vscode).


### Running tests
You can run the tests in the actinia test docker:

```bash
docker build -f docker/actinia-processing-lib-test/Dockerfile -t actinia-processing-lib-test .
docker run -it actinia-processing-lib-test -i

cd /src/actinia-processing-lib/

# run all tests
make test

# run only integrationtests
make integrationtest

# run only tests which are marked for development with the decorator '@pytest.mark.dev'
make devtest
```
