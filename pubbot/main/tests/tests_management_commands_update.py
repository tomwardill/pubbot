from django.test import TestCase
from django.core.management import call_command


class TestUpdateCommand(TestCase):

    def test_run(self):
        call_command("update")