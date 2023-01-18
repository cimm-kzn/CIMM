Synthesis Planner
========

Download docker image: `download <http://seafile.cimm.site/f/9eb331a8c3d9476a83ab/>`_

Please, contact Timur Gimadiev to get the password: TimRGimadiev@kpfu.ru

**Setup and run:**

1. Loading docker image:

    `cat planner.tar.gz | docker load`

2. SDF file with target molecule (ex: aspirin.sdf) should exist in your workdir.
Run synthesis via python within docker container:

    `sudo docker run -it --rm -e target=aspirin -e steps=3000 -e chromo=5 -e ps=100 -e cpu=4 -v $PWD:/mnt planner:latest`

*Customize settings:*

* target - name of SDF file with target molecule

* steps - number of genetic algorithm iterations

* chromo - length of the chromosome

* ps - population size

* cpu - numper of CPU to use


The process of searching for synthesis paths can be monitored in the log file in current directory.