import os

import vcr
from django.conf import settings

CASSETTES_DIR = os.path.join(str(settings.BASE_DIR), "fixtures/cassettes")
my_vcr = vcr.VCR(
    cassette_library_dir=CASSETTES_DIR,
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
    filter_headers=["authorization"],
    record_mode="once",
    match_on=["method", "path", "query"],
)
