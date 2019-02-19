# -*- coding: utf-8 -*-

import importlib
import logging
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Callable

import yaml

from invoker.utils import split_qualified_name

LOGGER = logging.getLogger(__name__)


def define_args_parser() -> ArgumentParser:

    parser = ArgumentParser(description="invoke specify function with DI")

    parser.add_argument('log_config', help='specify logging.yaml path', type=Path)
    parser.add_argument('invoke_options', help='specify invoke.yaml path')
    parser.add_argument('--config', help='specify configuration.yaml path', type=Path, action='append', default=[])
    parser.add_argument('--invoke_context_class', help='specify InvokerContext subclass.', type=str, default='invoker.InvokerContext')

    return parser


def execute():

    parser = define_args_parser()  # type* ArgumentParser
    args = parser.parse_args()

    _package, _callable = split_qualified_name(args.invoke_context_class)
    _InvokerClass = getattr(importlib.import_module(_package), _callable)  # type: Callable

    with Path(args.invoke_options).open('r', encoding='utf-8') as f:
        invoke_options = yaml.load(f)

    invoker = _InvokerClass(args.config, args.log_config)
    ret = invoker.invoke(invoke_options)

    LOGGER.info('invoke ret: %s', ret)

    sys.exit(0)


if __name__ == '__main__':
    execute()
