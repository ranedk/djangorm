import argparse
from django.core.management.base import BaseCommand, CommandError
from d2g.model_to_class import convert_models


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--apps",
            nargs="+",
            required=True,
            help="Apps whose models are converted to java/go classes"
        )
        parser.add_argument(
            "--lang",
            required=True,
            help="Apps whose models are converted to java/go classes"
        )

    def handle(self, *args, **options):
        apps = options["apps"]
        lang = options["lang"]
        convert_models(apps=apps, lang=lang)
