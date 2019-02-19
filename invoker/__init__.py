# -*- coding: utf-8 -*-

import importlib
import logging
import logging.config
import os
import re
import sys
from collections.abc import Mapping
from logging import Logger
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import yaml
from injector import Binder, Injector, Key, singleton

from invoker.utils import AliasDict, split_qualified_name

LOGGER = logging.getLogger(__name__)

InvokeConfig = Key('InvokeConfig')  # type: AliasDict
InvokeOptions = Key('InvokeOptions')  # type: Dict


class InvokerContext():

    logger = LOGGER.getChild('InvokerContext')  # type: Logger

    IS_ALREADY_LOADED_LOGGING = False

    @classmethod
    def set_logging_config(cls, logging_config_file: Path):

        if cls.IS_ALREADY_LOADED_LOGGING:
            cls.logger.warning(
                'already initilize logging configuration. skip.')

        else:
            cls.logger.info('initilize logging configuration. start')
            with logging_config_file.open('r', encoding='utf-8') as f:
                config = yaml.load(f)

            logging.config.dictConfig(config)
            cls.IS_ALREADY_LOADED_LOGGING = True
            cls.logger.info(
                'initilize logging configuration. end: \n%s', config)

    def __init__(self, config_file_list: List[Path],
                 logging_config_path: Path = None):

        if logging_config_path:
            self.set_logging_config(logging_config_path)

        # logging default setting.
        config = AliasDict({})
        for c_file in config_file_list:
            cl = AliasDict.load_from_yaml(c_file)
            config.update(cl)

        self.app_config = config
        self.injector = Injector(modules=[self._injector_bind])  # type: Injector
        self.invoke_options = None

    def _injector_bind(self, binder: Binder):
        binder.bind(InvokeConfig, to=self.app_config, scope=singleton)

    def invoke(self, invoke_options: Dict):

        self.invoke_options = invoke_options
        self.injector.binder.bind(InvokeOptions, to=self.invoke_options, scope=singleton)

        _package, _callable = split_qualified_name(invoke_options['invoke'])
        self.logger.debug('calleble: %s, package: %s', _callable, _package)

        self.logger.debug('cwd: %s', os.getcwd())
        sys.path.append(os.getcwd())
        self.logger.debug('sys.path: \n %s', '\n '.join(sys.path))

        _func = getattr(importlib.import_module(_package), _callable)  # type: Callable

        kwargs = invoke_options.get('args', {})
        try:
            return self._invoke(_func, args=[], kwargs=kwargs)
        except Exception as e:
            self.logger.exception('invoke function internal error.')
            sys.exit(10)

    def _invoke(self, func: Callable, args: Tuple, kwargs: Dict) -> any:

        self.logger.info('func: %s  args: %s, kwargs: %s', func, args, kwargs)
        return self.injector.call_with_injection(func,
                                                 args=args,
                                                 kwargs=kwargs)
