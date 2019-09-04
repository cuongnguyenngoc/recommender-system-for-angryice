import argparse
import time
from collections import deque
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
MSG = ''
MSGPlus = ''

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, args):
        irc.bot.SingleServerIRCBot.__init__(self, [(args.server, args.port)], args.nickname, args.nickname)
        self.args = args
        self.channel = args.channel
        self.inputs = {
            '1': deque([0] * args.length),
            '2': deque([0] * args.length)
        }
        self.messages = []

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + '_')

    def on_join(self, c, e):
        print 'Joined %s' % self.channel

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        pass

    # Nick Name:Chat Message
    def on_pubmsg(self, c, e):
        collectedMsg=e.arguments[0]
        rstring = ''
        mark = 0
        #collectedMsg=collectedMsg.decode('utf-8')
        #collectedMsg=zenhan.z2h(collectedMsg)
        for uchar in collectedMsg:
            inside_code=ord(uchar)
            if inside_code == 12288:
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):
                inside_code -= 65248
            rstring += unichr(inside_code)
        
        for tchar in rstring:
            inside_code=ord(tchar)
            if not (inside_code >= 32 and inside_code <= 126):
                mark=1

        #for tchar in rstring:
        #    if not ((tchar >= u'\u0030' and tchar<=u'\u0039') or (tchar >= u'\u0041' and tchar<=u'\u005a') or (tchar >= u'\u0061' and tchar<=u'\u007a') or tchar==' ' or tchar=='?' or tchar=='!'):
        #        mark=1

        if mark==0:
            self.messages.append(irc.client.NickMask(e.source).nick + ':' + rstring) # store messages
        #print irc.client.NickMask(e.source).nick + ':' + e.arguments[0]

    def on_dccmsg(self, c, e):
        pass

    def on_dccchat(self, c, e):
        pass

    def process_messages(self):
        # get all of Message as global var
        global MSG
        global MSGPlus
        for s in self.messages:
          MSG = s+'\n'

        MSGPlus+=MSG;
        MSG = ''
        # write inputs to file
        with open(self.args.outfile, 'a') as f:
          f.write(MSGPlus)
          print '%s %s' % (time.strftime('%X'),MSGPlus)
          MSGPlus = ''

        # reset
        self.messages[:] = []

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--server',
                        help='chat server',
                        default='chat.freenode.net')
    parser.add_argument('-p', '--port',
                        type=int,
                        help='chat server\'s port',
                        default=6667)
    parser.add_argument('-c', '--channel',
                        help='chat channel',
                        default='#iceEggs') # channel name should start with #
    parser.add_argument('-n', '--nickname',
                        help='bot\'s nickname',
                        default='bot')
    parser.add_argument('-i', '--interval',
                        type=int,
                        help='interval for getting messages (seconds)',
                        default=1)
    parser.add_argument('-l', '--length',
                        type=int,
                        help='length of outputs',
                        default=10)
    parser.add_argument('-o', '--outfile',
                        help='output file',
                        default='chat.txt')

    args = parser.parse_args()

    bot = TestBot(args)
    bot.reactor.scheduler.execute_every(args.interval, bot.process_messages) # execute "process_messages" every "interval" second
    bot.start()

if __name__ == '__main__':
    main()
