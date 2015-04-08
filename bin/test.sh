#!/bin/bash -e

BASEDIR=`dirname $0`/..

cd $BASEDIR
$BASEDIR/env/bin/tox
