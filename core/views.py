import asyncio

from django.http import HttpResponse

# Create your views here.
from django.utils.decorators import classonlymethod
from django.views import View
from django.views.generic import TemplateView


class AsyncView(View):
    """Async CBV"""

    @classonlymethod
    async def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, request, *args, **kwargs):
        await asyncio.sleep(2)
        return HttpResponse('This was run asynchronously')


class IndexView(TemplateView):
    template_name = "about.html"


async def websocket_view(socket):
    await socket.accept()
    while True:
        message = await socket.receive_text()
        await socket.send_text(message)
