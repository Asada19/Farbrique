from .models import Mailing, Message, Client


class MailingService:
    model = Mailing

    @classmethod
    def general_statistic(cls) -> list[dict]:

        data = [
            {
                'mailing': mailing,
                'count_of_sent': len(list(mailing.messages.filter(status='SENT'))),
                'count_of_not_sent': len(list(mailing.messages.filter(status='NOT_SENT'))),
            } for mailing in Mailing.objects.all()
        ]
        return data

    @classmethod
    def detail_statistic(cls, pk) -> dict:
        mailing = Mailing.objects.get(pk=pk)
        data = {
                'mailing': mailing,
                'count_of_sent': len(list(mailing.messages.filter(status='SENT'))),
                'count_of_not_sent': len(list(mailing.messages.filter(status='NOT_SENT'))),
            }
        return data
