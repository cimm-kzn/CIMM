iSynthesis
========

Download docker image: `download <http://seafile.cimm.site/f/9eb331a8c3d9476a83ab/>`_

Please, contact Timur Gimadiev to get the password: TimRGimadiev@kpfu.ru

**Setup and run:**

1. Loading docker image:

    `cat isynthesis.tar.gz | docker load`

2. SDF file with target molecule (ex: bevantolol.sdf) should exist in your workdir.
Run synthesis via python within docker container:

    `sudo docker run -it --rm -e reagents=1000 -e steps=3000 -e target=bevantolol -e cpu=4 -v $PWD:/mnt isynthesis:latest`

*Customize settings:*

* reagents - number of building blocks to start from

* steps - number of MCTS iterations

* target - name of SDF file with target molecule

* cpu - numper of CPU to use


Every 100 iterations the results will be updated to a text file results.txt in the current folder.
The process of searching for synthesis paths can be monitored in the log file in current directory.