from .models import Newsletter, Message, Client


class NewsletterService:
    model = Newsletter

    @classmethod
    def get(cls) -> model:
        return cls.model.objects.all()

    @classmethod
    def general_statistic(cls) -> list:

        data = [
            {
                'newsletter': newsletter,
                'message': newsletter.message,
                'count_of_sent': len(list(Client.objects.all()))
            } for newsletter in Newsletter.objects.all()
        ]
        return data

    @classmethod
    def detail_statistic(cls, pk=1) -> dict:
        newsletter = Newsletter.objects.get(pk)
        data = {
                'newsletter': newsletter,
                'message': newsletter.message,
                'count_of_sent': len(list(Client.objects.all()))
            }
        return data


class MessageService:
    model = Message

    @classmethod
    def get(cls) -> model:
        return cls.model.objects.all()


class ClientService:
    model = Client

    @classmethod
    def get(cls) -> model:
        return cls.model.objects.all()

