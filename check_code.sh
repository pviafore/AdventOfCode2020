#! /bin/bash
mypy ./*.py common/*.py && pylint ./*.py common/*.py && py.test
