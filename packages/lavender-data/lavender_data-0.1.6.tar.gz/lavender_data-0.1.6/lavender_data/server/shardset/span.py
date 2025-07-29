from lavender_data.server.db import Shardset


def get_main_shardset(shardsets: list[Shardset]) -> Shardset:
    """Pick the main shardset for getting samples from.
    During the iteration, the samples are yielded as the order of the samples in the main shardset.

    The main shardset is the one with the oldest creation date.
    """
    oldest_shardset = shardsets[0]
    oldest_shardset_created_at = shardsets[0].created_at
    for shardset in shardsets:
        if oldest_shardset_created_at > shardset.created_at:
            oldest_shardset_created_at = shardset.created_at
            oldest_shardset = shardset

    return oldest_shardset


def span(index: int, shard_samples: list[int]) -> tuple[int, int]:
    sample_index = index
    shard_index = 0
    for samples in shard_samples:
        if sample_index < samples:
            break
        else:
            sample_index -= samples
            shard_index += 1

    return (shard_index, sample_index)
