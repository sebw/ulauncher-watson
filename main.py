import json
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

import subprocess

class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        logger.info('preferences %s' % json.dumps(extension.preferences))

        items = []

        response = subprocess.check_output("watson status", shell=True)
        response_task = str(response).split("[")[0]
        response_time = str(response).split("]")[-1]

        stop = subprocess.check_output("watson stop", shell=True)

        items.append(ExtensionResultItem(icon='images/icon.png',
                                            name='%s' % response_task,
                                            description='%s' % response_time,
                                            on_enter=OpenUrlAction(stop)))

        return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
