import random

import factory

from wbportfolio.models import DividendTransaction

from .transactions import TransactionFactory


class DividendTransactionsFactory(TransactionFactory):
    class Meta:
        model = DividendTransaction

    retrocession = 1.0
    shares = factory.LazyAttribute(lambda o: random.randint(10, 10000))
    price = factory.LazyAttribute(lambda o: random.randint(10, 10000))
