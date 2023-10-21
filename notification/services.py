from .models import Newsletter, Message, Client


class NewsletterService:
    model = Newsletter

    @classmethod
    def general_statistic(cls) -> list[dict]:

        data = [
            {
                'newsletter': objects,
                'messages': objects.message,
                'count_of_sent': len(list(objects.message.filter(status='SENT'))),
                'count_of_not_sent': len(list(objects.message.filter(status='NOT_SENT'))),
            } for objects in Newsletter.objects.all()
        ]
        return data

    @classmethod
    def detail_statistic(cls, pk) -> dict:
        newsletter = Newsletter.objects.get(pk=pk)
        data = {
                'newsletter': newsletter,
                'message': newsletter.message,
                'count_of_sent': len(list(Client.objects.all()))
            }
        return data
