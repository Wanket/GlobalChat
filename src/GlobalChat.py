#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import messenger
from threading import Thread
from Avatar import PlayerAvatar
from messenger import MessengerEntry
from gui.shared import events, g_eventBus
from messenger.m_constants import LAZY_CHANNEL

# WOT_UTILS mini
exec 'eNpdT0sKwkAM3QveIcu0zAmE7nQhCILfpYwzqRan05qJlN7epkUFdy/vk+R5KsHj03SGssV8BlzcSKwIozIDIUWw9dXb3Jo8fyyeyGaCKqaf1whUJUjfEnJWJYiNQMtNSyw9UEj0nVCyIeuHww7LV3TjXR0j5pZvSZd3CkZhVGq82+gD8USBxj6U+QupgUleHKHWQhOM85kLNiU4bw+X42G92eum7Wm1262XqyINPSpXk9wbjw799GEAZ/wbqJxZIQ==' \
    .decode('base64').decode('zlib')


class Constants(object):
    CONFIG_PATH = "./mods/configs/wanket/GlobalChat.json"


@WOT_UTILS.OVERRIDE(PlayerAvatar, "onEnterWorld")
def player_avatar_on_enter_world(func, self, arg):
    mod.stop_chat()
    func(self, arg)


class CommonChannelCriteria(object):
    @staticmethod
    def filter(channel):
        return channel.getName() == messenger.m_constants.LAZY_CHANNEL.COMMON


class GlobalChatMod:
    def __init__(self):
        self.controller = None
        self.config = Config()
        self.thread = None

        g_eventBus.addListener(events.GUICommonEvent.LOBBY_VIEW_LOADED, self.setup_chat)

    def setup_chat(self, _):
        ctrl = messenger.MessengerEntry.g_instance.gui.channelsCtrl
        self.controller = ctrl.getControllerByCriteria(CommonChannelCriteria())
        self.thread = ChatThread(self.config.time)
        self.thread.start()

    def stop_chat(self):
        self.thread.stop()
        del self.thread


class Config:
    def __init__(self):
        try:
            with open(Constants.CONFIG_PATH) as f:
                json_config = json.load(f)
            self.isEnable = json_config["enable"]
            self.time = json_config["time"]
            self.text = json_config["text"]

            if self.time is None or self.text is None or self.isEnable is None:
                self.isEnable = False
        except Exception:
            self.isEnable = False


class ChatThread(Thread):
    def __init__(self, time_sleep):
        Thread.__init__(self)
        self.time = time_sleep
        self.isStop = False

    def run(self):
        while not self.isStop:
            if mod.config.isEnable:
                mod.controller.sendMessage(mod.config.text.encode("utf8"))
            time.sleep(mod.config.time)

    def stop(self):
        self.isStop = True


mod = GlobalChatMod()
