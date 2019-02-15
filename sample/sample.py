# -*- coding: utf-8 -*-

import logging
from injector import inject
from invoker import InvokeConfig

LOGGER = logging.getLogger(__name__)


@inject
def sample_function(config: InvokeConfig,
                    key: str):

    LOGGER.info('key: %s, value: %s', key, config.get(key))
    LOGGER.info('config: %s', config)
