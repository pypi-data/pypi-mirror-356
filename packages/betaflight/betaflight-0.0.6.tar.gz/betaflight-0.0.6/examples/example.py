from betaflight import Simulator
import asyncio

if __name__ == "__main__":
    simulator = Simulator()
    asyncio.run(simulator.run())