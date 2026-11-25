import env
import run


def test_canonical_tools_correct_before_drift():
    api = env.Api()
    for p in env.PROCS:
        fn = run.build(p["tool"])
        for x in p["inputs"]:
            assert env.correct(fn(api, **x), env.expected(p, x))


def test_breaking_drift_raises_and_is_documented():
    for p, (name, *_ , (new_name, new_key), _s) in zip(env.PROCS, env.SPECS):
        api = env.Api({name: "breaking"})
        assert not hasattr(api, name) and hasattr(api, new_name)
        assert f"api.{new_name}(" in env.docs({name: "breaking"})
        assert new_key in getattr(api, new_name)(**p["inputs"][0])


def test_silent_drift_undocumented_and_caught_by_tests():
    for p in env.PROCS:
        name = p["api"]
        assert env.docs({name: "silent"}) == env.docs()
        fn = run.build(p["tool"])
        api = env.Api({name: "silent"})
        assert any(not env.correct(fn(api, **x), env.expected(p, x)) for x in p["tests"])


def test_schedule_paired_and_30_percent():
    d0, s0 = run.schedule(1)
    d1, s1 = run.schedule(1)
    assert d0 == d1 and s0 == s1
    assert len(d0) == 6 and sorted(d0.values()).count("silent") == 3


def test_test_inputs_not_in_episode_inputs():
    for p in env.PROCS:
        assert not any(x in p["episode_inputs"] for x in p["tests"])
