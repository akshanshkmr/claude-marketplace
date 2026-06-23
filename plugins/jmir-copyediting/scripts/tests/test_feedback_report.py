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


def test_feedback_tab_and_pane():
    h = gen()
    assert 'data-pane="feedback"' in h, "feedback sidebar pane missing"
    assert 'id="fbList"' in h, "feedback list container missing"
    assert 'id="fbCount"' in h, "feedback count badge missing"


def test_summary_globals():
    h = gen()
    assert "window.__SUMMARY__" in h, "structured summary global missing"
    assert "window.__TITLE__" in h, "title global missing"
    assert "window.__SOURCE__" in h, "source global missing"


def test_pill_and_popover_markup():
    h = gen()
    assert 'id="fb-pill"' in h, "feedback pill missing"
    assert 'id="fb-popover"' in h, "feedback popover missing"
    for cat in ("missed-edit", "wrong-edit", "better-suggestion", "general-note"):
        assert f'data-cat="{cat}"' in h, f"category button {cat} missing"
    for el in ('id="fb-repl"', 'id="fb-note"', 'id="fb-save"', 'id="fb-cancel"', 'id="fb-snippet"'):
        assert el in h, f"{el} missing"


def test_capture_js_present():
    h = gen()
    assert "window.__FEEDBACK_GET__" in h, "feedback getter not exposed"
    assert "':feedback'" in h or '":feedback"' in h or ":feedback" in h, \
        "feedback storage key not used"
    assert "getSelection" in h, "selection capture not wired"


def test_export_button_and_handler():
    h = gen()
    assert 'id="fbExport"' in h, "export button id missing"
    assert "Export feedback" in h, "export button label missing"
    assert "jmir-feedback.v1" in h, "export schema string missing"
    assert "Copy insights" not in h, "old Copy insights label should be gone"


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
