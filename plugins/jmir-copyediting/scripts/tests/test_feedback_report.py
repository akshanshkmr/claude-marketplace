import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
sys.path.insert(0, str(SCRIPTS))
import report  # noqa: E402

SAMPLE = HERE / "sample.txt"


def gen():
    return report.build(SAMPLE, None, None)


def test_paragraph_anchors():
    h = gen()
    assert "data-pidx=" in h, "paragraphs must carry data-pidx"
    assert "data-section=" in h, "paragraphs must carry data-section"


def test_rule_id_on_edit_spans():
    h = gen()
    assert "data-rule-id=" in h, "edit spans must carry data-rule-id"


def main():
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("ok   ", name)
            except AssertionError as e:
                failures += 1
                print("FAIL ", name, "-", e)
    if failures:
        print(f"\n{failures} test(s) failed")
        sys.exit(1)
    print("\nALL PASS")


if __name__ == "__main__":
    main()
