#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2011-2014, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" Server error hierarchy

+ NeoError
|
+--- BadRequest (HTTP 400)
|
+--- NotFound (HTTP 404)
|
+--- Conflict (HTTP 409)
|
+--- BatchError (wraps other NeoError from batch submission)
|
+--- CypherError (returned by classic cypher calls)
|
+--- ClientError
|
+--- DatabaseError
|
+--- TransientError



"""


__all__ = ["GraphError"]


class GraphError(Exception):
    """ Default exception class for all errors returned by the
    Neo4j server.
    """

    __cause__ = None
    exception = None
    fullname = None
    request = None
    response = None
    stacktrace = None

    def __new__(cls, *args, **kwargs):
        try:
            exception = kwargs["exception"]
            try:
                error_cls = type(exception, (cls,), {})
            except TypeError:
                # for Python 2.x
                error_cls = type(str(exception), (cls,), {})
        except KeyError:
            error_cls = cls
        return Exception.__new__(error_cls, *args)

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)
        for key, value in kwargs.items():
            setattr(self, key, value)
