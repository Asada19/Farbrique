from .models import Newsletter, Message, Client


class NewsletterService:
    model = Newsletter

    @classmethod
    def get(cls) -> model:
        return cls.model.objects.all()

    @classmethod
    def general_statistic(cls):
        ...

    @classmethod
    def detail_statistic(cls):
        ...


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

