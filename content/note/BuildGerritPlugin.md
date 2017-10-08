+++
title = "Build Gerrit Plugins"
date = "2016-12-03T14:21:57+08:00"
tags        = ["Gerrit"]
categories  = ["Gerrit"]
+++

Gerrit plugins can be built with both [Buck](https://buckbuild.com/) and [Maven](http://maven.apache.org/).

**NOTE**: Developing Gerrit plugins requires installing JDK first.

# Build by Maven

If plugin contains `pom.xml` file, it can be built with Maven.

* Install Maven, see [Maven Doc about Installing Apache Maven](http://maven.apache.org/install.html)
* Check out plugin source code

```
git clone https://gerrit.googlesource.com/plugins/reviewers
```

* Build with Maven

```
mvn clean package
```

Maven will automatically download all dependencies and build source code. You will be able to find jar file in `$WORKSPACE/target` directory.


# Build by BUCK

BUCK is recommended by Gerrit Community. It's faster. The build artifcat is also smaller than Maven.

## Install BUCK

See [Gerrit Documentation](https://gerrit-review.googlesource.com/Documentation/dev-buck.html#_installation)

## Build via Command Line

Two build modes are supported: *Standalone* and *in Gerrit tree*. The standalone build mode is recommended, as this mode doesn't require the Gerrit tree to exist locally.

### Build standalone

```shell
# clone bucklets library
git clone https://gerrit.googlesource.com/bucklets
# checkout the correct bucklets version: Make sure bucklets/buckversion is same as the gerrit/.buckversion
git checkout SHA-1
# link bucklets to the plugin directory
cd PLUGIN_DIRECTORY
ln -s ../bucklets .
# link to the .buckversion file
ln -s bucklets/buckversion .buckversion
# build the plugin
buck build plugin
# You will be able to find the plugin in buck-out/gen
```

**NOTE**

It's critical to checkout correct bucklets version. You have to travese commit history of bucklets repository and find out the correct version.

For example, we need to build a plugin for Gerrit version stable-2.11.

Go to gerrit source repository, and we can find `.buckversion` which contains the commit SHA-1 `79d36de9f5284f6e833cca81867d6088a25685fb`

Then we will check bucklets repository and find in commit `bdd7f97`, the `bucklets/buckversion` has the same commit SHA-1 `79d36de9f5284f6e833cca81867d6088a25685fb`.

So we need to checkout `bdd7f97` for bucklets repository.

# References

1. [Gerrit Documentation: Building plugins](https://gerrit-review.googlesource.com/Documentation/dev-build-plugins.html)
2. [Gerrit Documentation: Building with Buck](https://gerrit-review.googlesource.com/Documentation/dev-buck.html)
