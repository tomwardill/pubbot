# Copyright 2014 the original author or authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
import json

from django.utils.functional import SimpleLazyObject
import redis

from pubbot.utils import force_str
from .stemmer import stemmer
from .tokenizer import tokenizer


def group_tokens(tokens):
    a = ""
    b = ""
    c = tokens.next()
    yield (a, b, c)

    while c:
        a = b
        b = c
        try:
            c = tokens.next()
        except StopIteration:
            c = ""
        yield (a, b, c)


class Brain(object):

    TOKEN_KEY = "T_%s"
    GROUP_KEY = "G_%s_%s_%s"
    FORWARD_KEY = "F_%s_%s"
    BACKWARD_KEY = "B_%s_%s"

    def __init__(self):
        self.client = redis.StrictRedis(host='localhost', port=6379, db=10)
        with open(os.path.join(os.path.dirname(__file__), "generate_sentence.lua")) as fp:
            self.generate_sentence = fp.read()

    def store_tokens(self, tokens):
        for a, b, c in group_tokens(tokens):
            self.client.sadd(self.TOKEN_KEY % (stemmer.stem(b), ), self.GROUP_KEY % (a, b, c))
            self.client.sadd(self.FORWARD_KEY % (a, b), c)
            self.client.sadd(self.BACKWARD_KEY % (c, b), a)
            self.client.incr(self.GROUP_KEY % (a, b, c))

    def store_string(self, text):
        try:
            tokens = tokenizer.split(force_str(text))
            return self.store_tokens(tokens)
        except UnicodeError:
            pass

    def get_chains_from_tokens(self, tokens):
        tokens = [stemmer.stem(token) for token in tokens]
        while tokens:
            token = random.choice(tokens)
            try:
                results = json.loads(self.client.eval(self.generate_sentence, 0, token, 10), "utf-8")
            except UnicodeError:
                continue

            if not results:
                tokens.remove(token)
                continue

            for result in results:
                yield result["chain"], result["score"]


brain = SimpleLazyObject(Brain)
