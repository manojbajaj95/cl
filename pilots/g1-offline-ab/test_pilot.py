import unittest

import numpy as np

from agent import ACTIONS, CODES, LESSONS, STEPS, rollout
from analysis import SCORE_NAMES, correlations, ess, fitted_dr, ratios, uplift_smoother


class PilotTests(unittest.TestCase):
    def test_rollout_uses_changed_state_and_records_sampled_logp(self):
        calls = []
        logp = np.log([0.2, 0.5, 0.3])

        def score(step, code):
            calls.append((step, code))
            return logp

        states, actions, observed, reward = rollout(0, score, (0.9, 0.1, 0.9))
        self.assertEqual(calls, [(0, 0), (1, 5), (2, 3)])
        self.assertEqual(states, [0, 5, 3])
        self.assertEqual(actions, [2, 0, 2])
        np.testing.assert_allclose(observed, logp[actions])
        self.assertEqual(reward, 1)

    def test_ratios_replay_exact_sampled_tokens(self):
        logging = np.array([0.5, 0.25, 0.25])
        edited = np.array([0.25, 0.5, 0.25])
        shape = (2, STEPS, CODES, len(ACTIONS))
        actions = np.array([[0, 1, 2], [2, 0, 1]])
        log = dict(policy=np.broadcast_to(np.log([logging, edited])[:, None, None], shape),
                   states=np.zeros_like(actions), actions=actions, logp=np.log(logging[actions]))
        delta, weights = ratios(log)
        np.testing.assert_allclose(np.exp(delta[0]), [[0.5, 2, 1], [1, 0.5, 2]])
        np.testing.assert_allclose(weights[0], [[0.5, 1, 1], [1, 0.5, 1]])
        np.testing.assert_allclose(ess(weights), [[1.8, 1.8, 2]])

    def test_dr_recovers_exact_value_in_balanced_single_state_data(self):
        # All 27 action trajectories once per fold under uniform behavior.
        actions = np.indices((3, 3, 3)).reshape(3, -1).T
        actions = np.tile(actions, (3, 1))
        rewards = (actions[:, -1] == 0).astype(float)
        groups = np.repeat(np.arange(3), 27)
        policy = np.broadcast_to([0.7, 0.2, 0.1], (1, STEPS, CODES, len(ACTIONS)))
        weights = np.cumprod(3 * policy[:, 0, 0, actions], axis=-1)
        np.testing.assert_allclose(
            fitted_dr(policy, np.zeros_like(actions), actions, rewards, weights, groups), [0.7],
        )

    def test_uplift_never_uses_labels_in_evaluation_fold(self):
        smoother = uplift_smoother(LESSONS)
        folds = np.arange(len(LESSONS)) % 5
        np.testing.assert_array_equal(smoother[folds[:, None] == folds[None, :]], 0)
        self.assertTrue(np.all(np.any(smoother != 0, axis=1)))

    def test_rank_margins_with_ties(self):
        truth = np.array([1, 2, 2, 3])
        values = {name: truth for name in SCORE_NAMES}
        values["judge"] = -truth
        values["uplift"] = np.ones_like(truth)
        result = correlations(values, truth, np.arange(4))
        np.testing.assert_allclose(result, [1, 1, 1, 1, -1, np.nan, 0, 2, np.nan])


if __name__ == "__main__":
    unittest.main()
