from betaflight.simulator_l2f import L2F
from betaflight.gamepad import Gamepad
import asyncio
import os


gamepad_mapping = os.path.join(os.path.dirname(__file__), "gamepad_mapping.json")

async def main():
    simulator = L2F()
    gamepad = Gamepad(gamepad_mapping, simulator.set_rc_channels)

    await asyncio.gather(simulator.run(), gamepad.run())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
