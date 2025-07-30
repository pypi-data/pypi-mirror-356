import ipaddress
import pytest
import pytest_asyncio

import turbobt
from turbobt.neuron import AxonInfo, NeuronLite, PrometheusInfo
from turbobt.subnet import SubnetReference
from turbobt.substrate.transports.mock import MockTransport

@pytest.mark.asyncio
async def test_chain(substrate):
    block_header = await substrate.chain.getHeader()

    assert block_header == {
        "digest": {
            "logs": [],
        },
    }


@pytest_asyncio.fixture
async def patch_get_encrypted_commit(monkeypatch):
    def get_encrypted_commit(
        uids,
        weights,
        version_key,
        tempo,
        current_block,
        netuid,
        subnet_reveal_period_epochs,
        block_time,
    ):
        import base64
        import json

        return (
            base64.b64encode(json.dumps({
                "uids": uids,
                "weights": weights,
            }).encode()),
            123,
        )

    monkeypatch.setattr(
        "bittensor_commit_reveal.get_encrypted_commit",
        get_encrypted_commit,
    )

    yield


@pytest_asyncio.fixture
async def bittensor(subtensor, patch_get_encrypted_commit):
    async with turbobt.Bittensor(
        "ws://127.0.0.1:9944",
        transport=MockTransport(subtensor),
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_client(bittensor, subtensor, alice_wallet):
    subnet = bittensor.subnet(12)
    hyperparameters = await subnet.get_hyperparameters()

    assert hyperparameters == {
        "activity_cutoff": 5000,
        "adjustment_alpha": 0,
        "adjustment_interval": 100,
        "alpha_high": 58982,
        "alpha_low": 45875,
        "bonds_moving_avg": 900000,
        "commit_reveal_period": 1,
        "commit_reveal_weights_enabled": False,
        "difficulty": 10000000,
        "immunity_period": 4096,
        "kappa": 32767,
        "liquid_alpha_enabled": False,
        "max_burn": 100000000000,
        "max_difficulty": 4611686018427387903,
        "max_regs_per_block": 1,
        "max_validators": 64,
        "max_weights_limit": 1.0,
        "min_allowed_weights": 0,
        "min_burn": 500000,
        "min_difficulty": 10000000,
        "registration_allowed": True,
        "rho": 10,
        "serving_rate_limit": 50,
        "target_regs_per_interval": 2,
        "tempo": 100,
        "weights_rate_limit": 100,
        "weights_version": 0,
    }

    neurons = await subnet.list_neurons()

    assert neurons == []

    await subnet.neurons.register(alice_wallet.hotkey, wallet=alice_wallet)

    neurons = await subnet.list_neurons(block_hash="new")

    assert neurons == [
        NeuronLite(
            active=True,
            axon_info=AxonInfo(
                ip=ipaddress.IPv4Address("0.0.0.0"),
                port=0,
                protocol=0,
            ),
            coldkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
            consensus=0,
            dividends=0,
            emission=0,
            hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
            incentive=0,
            last_update=0,
            prometheus_info=PrometheusInfo(
                ip=ipaddress.IPv4Address("0.0.0.0"),
                port=0,
            ),
            pruning_score=65535,
            rank=0,
            stake=0,
            subnet=SubnetReference(
                client=bittensor,
                netuid=12,
            ),
            trust=0,
            uid=0,
            validator_permit=True,
            validator_trust=0,
        ),
    ]

    weights = await subnet.weights.fetch()

    assert weights == {}

    await subnet.weights.commit(
        {
            0: 0.9,
        },
        wallet=alice_wallet,
    )

    weights = await subnet.weights.fetch()

    controller = Controller(
        subtensor,
        # TODO better param names
        block_time=12,
        epoch_size=100,
    )

    await controller.pause()

    assert weights == {}

    await controller.wait_for_epoch()

    # main things:
    with controller.pause(50):
        with controller.delay(blocks=3):
            subnet.commitments.set("bla")

        subnet.commitments.get("bla")
        pass

    with controller.pause_block(300):
        pass

    controller.wait_for_block(300)

    controller.advance_block(100)   # advance_by
    controller.advance_epoch()

    weights = await subnet.weights.fetch()

    assert weights == {
        0: {
            0: 1.0,
        },
    }
