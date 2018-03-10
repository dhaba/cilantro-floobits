from cilantro.nodes.delegate.db.driver_base import DriverBase
from cilantro.utils.constants import SWAP_KEY
from cilantro.utils.utils import RedisSerializer as RS


class SwapsDriver(DriverBase):

    def get_swap_data(self, hash_lock: str) -> tuple:
        """
        Returns the atomic swap data as a tuple
        :param hash_lock: The hash lock key for look up
        :return: A tuple containing (sender, recipient, amount, unix_expiration), or an empty tuple if the hash_lock
                 does not exist in the hash table
        """
        if self.r.hexists(SWAP_KEY, hash_lock):
            return RS.tuple_from_str(self.r.hget(SWAP_KEY, hash_lock))
        else:
            print("Attempted to get hash_lock={} that doesnt exist in table")
            return ()

    def swap_exists(self, hash_lock: str) -> bool:
        """
        Returns true if the hash lock exists in the db, and false otherwise
        :param hash_lock: The hash lock for the swap
        :return: True if the hash lock exists in the db; false otherwise
        """
        return self.r.hexists(SWAP_KEY, hash_lock)

    def set_swap_data(self, hash_lock: str, sender: str, recipient: str, amount: float, unix_expiration: str):
        """
        Sets the atomic swap data in the hash table as a condensed tuple
        :param hash_lock: The hash lock for the swap
        :param sender: The verifying address for the sender's wallet
        :param recipient: The verifying address for the recipient's wallet
        :param amount: The amount for the swap
        :param unix_expiration: The unix expiration for the swap
        """
        self.r.hset(SWAP_KEY, hash_lock, RS.str_from_tuple((sender, recipient, amount, unix_expiration)))

    def remove_swap_data(self, hash_lock: str):
        """
        Removes the data associated with hash_lock
        :param hash_lock: The hash lock for the swap
        """
        self.r.hdel(SWAP_KEY, hash_lock)
