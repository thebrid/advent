from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from math import lcm, prod

from pytest import mark


class PulseType(IntEnum):
    HIGH = 0
    LOW = 1


@dataclass
class Pulse:
    source: str
    type: PulseType
    dest: str


class Module(ABC):
    def __init__(self, name: str, outputs: list[str]) -> None:
        self.name = name
        self.inputs = list[str]()
        self.outputs = outputs

    @abstractmethod
    def __call__(self, pulse: Pulse) -> list[Pulse]:
        pass


class FlipFlop(Module):
    is_on: bool = False

    def __call__(self, pulse: Pulse) -> list[Pulse]:
        if pulse.type != PulseType.LOW:
            return []

        self.is_on = not self.is_on
        return [Pulse(self.name, PulseType.HIGH if self.is_on else PulseType.LOW, output) for output in self.outputs]


class Conjunction(Module):
    def __init__(self, name: str, outputs: list[str]) -> None:
        super().__init__(name, outputs)
        self.source_values = defaultdict[str, PulseType](lambda: PulseType.LOW)

    def __call__(self, pulse: Pulse) -> list[Pulse]:
        self.source_values[pulse.source] = pulse.type

        output_type = (
            PulseType.LOW
            if all(self.source_values[input_name] == PulseType.HIGH for input_name in self.inputs)
            else PulseType.HIGH
        )
        return [Pulse(self.name, output_type, output) for output in self.outputs]


class Broadcast(Module):
    def __init__(self, name: str, outputs: list[str]) -> None:
        super().__init__(name, outputs)

    def __call__(self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(self.name, pulse.type, output) for output in self.outputs]


Network = dict[str, Module]


def pulses(input_string: str) -> int:
    network = _parse_input(input_string)
    pulses = _count_pulses(network, 1000)
    return prod(pulses.values())


def _count_pulses(network: Network, press_count: int) -> dict[PulseType, int]:
    output = {PulseType.HIGH: 0, PulseType.LOW: 0}

    for _ in range(press_count):
        current_round = [Pulse("button", PulseType.LOW, "broadcaster")]
        next_round = []

        while current_round:
            for pulse in current_round:
                output[pulse.type] += 1

                if pulse.dest in network:
                    next_round.extend(network[pulse.dest](pulse))

            current_round = next_round
            next_round = []

    return output


# rx receives from ql only which is a conjunction so outputs LOW only when all inputs are HIGH.
def cycles_to_low_on_rx(network: Network) -> int:
    input_nodes = {node.name for node in network.values() if "ql" in node.outputs}
    prev_high_pulse = dict[str, int]()
    cycle_time = dict[str, int]()
    round_index = 0

    while True:
        current_round = [Pulse("button", PulseType.LOW, "broadcaster")]
        next_round = []

        while current_round:
            for pulse in current_round:
                if pulse.dest in network:
                    next_round.extend(network[pulse.dest](pulse))

            current_round = next_round
            next_round = []

            for pulse in current_round:
                if pulse.dest == "ql" and pulse.type == PulseType.HIGH:
                    if pulse.source not in prev_high_pulse:
                        prev_high_pulse[pulse.source] = round_index
                    elif pulse.source not in cycle_time:
                        cycle_time[pulse.source] = round_index - prev_high_pulse[pulse.source]

                        if all(node_name in cycle_time for node_name in input_nodes):
                            return lcm(*cycle_time.values())

        round_index += 1


def _parse_input(input_string: str) -> Network:
    network = Network()
    for line in input_string.splitlines():
        module = _parse_line(line)
        network[module.name] = module

    for name, module in network.items():
        for output in module.outputs:
            if output in network:
                network[output].inputs.append(name)

    return network


def _parse_line(line: str) -> Module:
    arrow_loc = line.find(" -> ")
    output_modules = line[arrow_loc + 4 :].split(", ")
    name_with_prefix = line[:arrow_loc]
    if name_with_prefix[0] == "%":
        return FlipFlop(name=name_with_prefix[1:], outputs=output_modules)
    elif name_with_prefix[0] == "&":
        return Conjunction(name=name_with_prefix[1:], outputs=output_modules)
    else:
        return Broadcast(name=name_with_prefix, outputs=output_modules)


EXAMPLE_INPUT1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

EXAMPLE_INPUT2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

PUZZLE_INPUT = """%fl -> tf, gz
%xb -> hl, tl
%mq -> tf, fl
%px -> hl, tm
%dp -> xv
broadcaster -> js, ng, lb, gr
&ql -> rx
%gk -> hm
%vp -> vf, sn
%fp -> xb
&lr -> ss, rm, dc, js, gk, dp, bq
%xl -> gx, lr
%xx -> hb
%cb -> jg
&hl -> nj, lb, tl, xx, hb, fp, mf
%vr -> tf, hq
%bq -> gk
%jg -> qn
%hb -> qk
%qk -> hs, hl
%gz -> tf
%rm -> hj
&tf -> cb, jg, fz, gr, zj, qn, kb
%qn -> td
%js -> lr, dc
%qb -> nc
%zj -> vr
%td -> tf, zj
%tl -> kg
%gx -> lr
%hm -> lr, rd
&fh -> ql
%nj -> xx
%hq -> kb, tf
%kg -> px, hl
%dc -> dp
%vf -> th, sn
&mf -> ql
%tm -> hl
&fz -> ql
%xd -> tn, sn
%ng -> vp, sn
%th -> qb
%rd -> xl, lr
%bt -> xd, sn
%tv -> sn
%nl -> bt
%hs -> fp, hl
%xv -> rm, lr
%tn -> sn, tv
%hj -> lr, bq
&ss -> ql
%sd -> nl
&sn -> sd, fh, th, qb, nl, ng, nc
%kb -> mq
%lb -> nj, hl
%gr -> tf, cb
%nc -> sd"""


@mark.parametrize(
    ("input_string", "expected_output"),
    [(EXAMPLE_INPUT1, 32000000), (EXAMPLE_INPUT2, 11687500), (PUZZLE_INPUT, 787056720)],
)
def test_pulses(input_string: str, expected_output: int) -> None:
    assert pulses(input_string) == expected_output


def test_cycles_to_low_on_rx() -> None:
    network = _parse_input(PUZZLE_INPUT)
    assert cycles_to_low_on_rx(network) == 212986464842911
