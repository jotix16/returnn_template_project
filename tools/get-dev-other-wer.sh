#!/bin/bash

grep "dev-other: " $1 | sed "s/dev-other: //"
