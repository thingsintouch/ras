from relay.relay_switch import switch_the_relay_after_checks

from common.common import runShellCommand_and_returnOutput

timestamp = runShellCommand_and_returnOutput("date +%s").replace("\n","")
#card_code = "4a338f6a"
card_code = "9d5e50d3"

switch_the_relay_after_checks(card_code, timestamp)
