import logging
import datetime
from dataclasses import (
    dataclass,
    field,
)
from collections.abc import (
    Sequence,
    Callable,
)

import numpy as np
from numpy.random import Generator as RandomNumberGenerator
from numpy.typing import NDArray

from event import Event
from utils import CooldownTimer


@dataclass
class Level:
    """
    Class representing a level of the game. Manages the level duration
    and event generation.

    :param level_num:
    :type level_num:
    :param level_duration:
    :type level_duration:
    :param challenge_points:
    :type challenge_points:
    :param support_points:
    :type support_points:
    """
    level_num: int
    level_duration: datetime.timedelta
    challenge_points: int
    support_points: int
    seed: int | None = field(default=None)

    # This will be manually initialized in the `__post_init__` method.
    _level_timer: CooldownTimer = field(init=False)

    def __post_init__(self) -> None:
        """
        Initialize additional instance attributes.
        """
        self._rng = np.random.default_rng(seed=self.seed)
        self._level_timer = CooldownTimer(self.level_duration)
        return

    def generate_events(
        self,
        challenge_actions: Sequence[Callable],
        challenge_action_costs: Sequence[int],
        support_actions: Sequence[Callable],
        support_action_costs: Sequence[int],
    ) -> Sequence[Event]:
        """
        Return

        """
        events = []

        # Generate challenge events.
        action_frequencies = self._generate_action_frequencies(
            self._rng,
            challenge_actions,
            challenge_action_costs,
            self.challenge_points,
        )
        # Schedule the generated challenge events.
        #
        # NOTE: For now they will all be queued to start right away.
        for action, frequency in action_frequencies.items():
            events.append(
                Event(
                    datetime.timedelta(seconds=0),
                    action,
                    num_calls=frequency
                )
            )

        # Generate support events.
        action_frequencies = self._generate_action_frequencies(
            self._rng,
            support_actions,
            support_action_costs,
            self.support_points,
        )
        # Schedule the generated support events.
        #
        # NOTE: For now they will all be queued to start right away.
        for action, frequency in action_frequencies.items():
            events.append(
                Event(
                    datetime.timedelta(seconds=0),
                    action,
                    num_calls=frequency
                )
            )
        
        return events

    def get_progress_ratio(self) -> float:
        """
        Return the level progress as a ratio of time elapsed to total
        level duration, with a maximum value of 1.0. If the elapsed
        time exceeds the total level duration the returned value is
        clipped to 1.0.
        """
        return min(
            self._level_timer.get_timedelta_ratio(),
            1.0,
        )

    def get_time_elapsed(self) -> datetime.timedelta:
        """
        Return the time elapsed since the level began.
        """
        return self._level_timer.get_timedelta()

    def next_level(
        self,
        level_duration: datetime.timedelta,
        challenge_points: int,
        support_points: int,
    ) -> None:
        """
        
        """
        self.level_num += 1
        self.level_duration = level_duration
        self.challenge_points = challenge_points
        self.support_points = support_points
        return

    def start(self) -> None:
        """
        Start the level.
        """
        self._level_timer.start()
        return

    def get_is_complete(self) -> bool:
        """
        Return `True` if the level is complete, otherwise return
        `False`.
        """
        return self._level_timer.get_is_ready()

    @staticmethod
    def _generate_action_frequencies(
        rng: RandomNumberGenerator,
        actions: NDArray | Sequence[Callable],
        action_costs: NDArray | Sequence[int],
        points: int,
    ) -> dict[Callable, int]:
        """
        Generate a sequence of events produced from the available
        actions.

        This is done by iteratively spending some amount of points to
        select an action until all points are spent or there aren't
        enough points to purchase any available actions.
        """
        logger = logging.getLogger(f'root.{__name__}')

        # Convert to numpy arrays.
        if not isinstance(actions, np.ndarray):
            actions = np.array(actions)
        if not isinstance(action_costs, np.ndarray):
            action_costs = np.array(action_costs)

        logger.debug('Starting points:', points)

        # Sort the actions so they're in ascending order of highest
        # cost to lowest cost.
        actions_order = action_costs.argsort(descending=True)
        actions = actions[actions_order]
        action_costs = action_costs[actions_order]

        # Iterate backwards through the actions and their max
        # quantities, selecting a random (valid) number of each action
        # until we're out of points. Do not select a random number of
        # the cheapest action so we can just spend all remaining points
        # on it.
        current_points = points
        action_frequencies = {}
        logger.debug('Selecting actions...')
        for action_i in range(0, len(actions) - 1):
            action = actions[action_i]
            action_cost = int(action_costs[action_i])
            max_action_quantity = int(current_points / action_cost)

            if max_action_quantity < 1:
                continue

            logger.debug(f'{action = }')
            logger.debug(f'{action_cost = }')
            logger.debug(f'{max_action_quantity = }')

            # Choose how many of the action to use to create events.
            action_quantity = rng.choice(max_action_quantity)
            action_frequencies[action] = action_quantity

            logger.debug(f'{action_quantity = }')

            # Adjust the current points remaining by how many were just
            # spent purchasing the chosen quantity of the action above.
            current_points -= action_cost * action_quantity

        # Choose as many of the cheapest action as possible using the
        # remaining points.
        action = actions[-1]
        action_cost = action_costs[-1]
        max_action_quantity = int(current_points / action_cost)
        action_frequencies[action] = max_action_quantity
        current_points -= action_cost * max_action_quantity

        logger.debug('Remaining points:', current_points)
        return action_frequencies


if __name__ == '__main__':
    LEVEL_NUMBER = 1
    LEVEL_DURATION = datetime.timedelta(seconds=30)
    CHALLENGE_POINTS = 10
    SUPPORT_POINTS = 10
    # SEED = 2

    level = Level(
        LEVEL_NUMBER,
        LEVEL_DURATION,
        CHALLENGE_POINTS,
        SUPPORT_POINTS,
    )

    valid_actions = np.array(['spawn small asteroid', 'spawn medium asteroid', 'spawn large asteroid'])
    valid_action_costs = np.array([1, 2, 4])

    # rng = np.random.default_rng(seed=SEED)
    rng = np.random.default_rng()
    events = level._generate_action_frequencies(
        rng,
        valid_actions,
        valid_action_costs,
        CHALLENGE_POINTS,
    )

    print(events)
