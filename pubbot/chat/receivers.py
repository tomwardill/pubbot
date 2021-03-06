# Copyright 2008-2013 the original author or authors
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

import random

from pubbot.conversation import chat_receiver
from pubbot.chat.writing import reply
from pubbot.chat.brain import brain


@chat_receiver(r'^(?P<sentence>.*)$')
def mutter(sender, sentence, **kwargs):
    if not kwargs.get('direct', False) or random.random() < 0.005:
        return

    return {
        'content': reply(sentence),
        'weight': -999,
    }


@chat_receiver(r'^(?P<sentence>.*)$')
def learn(sender, sentence, **kwargs):
    if kwargs.get('direct', False):
        return
    brain.store_string(sentence)
