import argparse
from django.core.management.base import BaseCommand, CommandError
from djangorm.model_to_class import convert_models


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
            help="java or go"
        )
        parser.add_argument("--orm", action="store_false", dest="orm", help="if you want orm tags (only go)")
        parser.add_argument("--valid", action="store_false", dest="valid", help="if you want valid tags (only go)")

    def handle(self, *args, **options):
        apps = options["apps"]
        lang = options["lang"]
        convert_models(apps=apps, lang=lang, for_orm=options["orm"], for_validation=options["valid"])
