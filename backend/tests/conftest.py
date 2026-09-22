import pytest


@pytest.fixture
def sample_resume_dir(tmp_path):
    root = tmp_path / "resume"
    (root / "projects").mkdir(parents=True)

    (root / "about.md").write_text(
        """---
type: about
title: Summary
---

Dylan is a software engineer who builds cat-related simulations.
""",
        encoding="utf-8",
    )

    (root / "projects" / "cat-sim.md").write_text(
        """---
type: project
title: Cat Simulator
tech: [Python]
---

A simulator where cats chase lasers using reinforcement learning.
""",
        encoding="utf-8",
    )

    return root
