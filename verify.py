from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions

semi = Options().inline(InlineOptions.semi_automatic())
verify = verify
