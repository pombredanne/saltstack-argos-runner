# -*- coding: utf8 -*-
'''
Salt Runner to collect fim.checksum data
'''
from __future__ import absolute_import

import logging
import salt.client
from salt.exceptions import SaltClientError

LOG = logging.getLogger(__name__)

__virtualname__ = 'argos'


def __virtual__():
    '''
    Load the fim client
    '''
    return __virtualname__


def _get_targets():
    '''
    Query master config for possible config options
    '''
    targets = []
    if __opts__['fim']['targets']:
        targets = __opts__['fim']['targets']

    return targets


def _get_algo():
    '''
    Query master config for possible config options
    '''
    algo = ''
    if __opts__['fim']['algo']:
        algo = __opts__['fim']['algo']

    return algo


def panoptes(tgt, targets=[], algo='', *args, **kwargs):
    '''
    Too soon!
    '''
    checksum = {}
    if not targets:
        targets = _get_targets()

    if not algo:
        algo = _get_algo()

    client = salt.client.LocalClient()
    try:
        output = client.cmd(tgt, 'fim.checksum', kwarg={'targets': targets, 'algo': algo}, timeout=__opts__['timeout'], expr_form='compound')
        for minion, path in output.iteritems():
            if not minion in checksum:
                checksum.update({minion: {}})
            if not 'files' in checksum[minion]:
                checksum[minion].update({'files': []})
            for key, val in path.iteritems():
                checksum[minion]['files'].append({'filename': key, 'checksum': val, 'algo': algo})

    except SaltClientError as client_error:
        LOG.debug(client_error)
        return ret

    return checksum

