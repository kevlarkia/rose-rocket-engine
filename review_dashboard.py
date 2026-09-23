"""Local review desk for the newsletter handoff.

The operator edits the draft, leaves a rating, and approves send.
The process binds to localhost only.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urlparse

from builder_pipeline import (
    acknowledge_escalation,
    append_feedback,
    assert_no_banned_words,
    list_escalations,
    load_packet,
    load_ritual,
    save_packet,
)

SendFn = Callable[[str, str], str]


def _escape(value: object) -> str:
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_review_page(packet: dict, escalations: list, ritual: dict) -> str:
    status = packet.get("status", "ready_for_review")
    approved = bool(packet.get("approved"))
    status_label = "Approved" if approved else status.replace("_", " ")
    touchpoints = packet.get("model_touchpoints") or []
    tier_rows = "".join(
        "<li><code>{id}</code> · {tier} · {model}</li>".format(
            id=_escape(row.get("id", "")),
            tier=_escape(row.get("tier", "")),
            model=_escape(row.get("model", "")),
        )
        for row in touchpoints
    )
    stages = "".join(f"<li>{_escape(stage)}</li>" for stage in packet.get("automated_stages") or [])
    open_items = [item for item in escalations if item.get("status") == "open"]
    if open_items:
        queue = "".join(
            "<li><strong>{stage}</strong> — {error}</li>".format(
                stage=_escape(item.get("stage", "")),
                error=_escape(item.get("error", "")),
            )
            for item in open_items
        )
    else:
        queue = "<li>Queue is clear.</li>"
    ritual_line = (
        f"{ritual.get('weekday', 'Monday')} {ritual.get('time_local', '09:00')}, "
        f"{ritual.get('duration_minutes', 30)} minutes — {ritual.get('title', 'Weekly prompt review')}"
    )
    markdown = packet.get("markdown") or ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Rose Rocket review desk</title>
  <style>
    :root {{
      color-scheme: light;
      --paper: #f3efe4;
      --ink: #1d1a16;
      --muted: #5e584e;
      --line: #d9d0c0;
      --card: #fffaf2;
      --good: #1f6b4a;
      --bad: #8c2f2f;
      --warn: #8a5a12;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font: 16px/1.45 "Iowan Old Style", Palatino, Georgia, serif;
    }}
    main {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 28px 20px 48px;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-end;
      border-bottom: 1px solid var(--line);
      padding-bottom: 16px;
    }}
    h1 {{
      font-size: 2rem;
      font-weight: 600;
      margin: 0;
      letter-spacing: -0.03em;
    }}
    .eyebrow {{
      margin: 0 0 4px;
      color: var(--muted);
      font: 0.78rem/1.2 ui-sans-serif, system-ui, sans-serif;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .status {{
      border: 1px solid var(--line);
      background: var(--card);
      border-radius: 999px;
      padding: 6px 12px;
      font: 0.85rem/1 ui-sans-serif, system-ui, sans-serif;
    }}
    .status.ready_for_review {{ color: var(--warn); }}
    .status.fallback {{ color: var(--bad); }}
    .status.approved {{ color: var(--good); }}
    .rule {{
      margin: 18px 0;
      color: var(--muted);
    }}
    .grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.6fr) minmax(280px, 0.8fr);
      gap: 18px;
    }}
    section {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 16px;
    }}
    h2 {{
      margin: 0 0 10px;
      font-size: 1.05rem;
    }}
    textarea {{
      width: 100%;
      min-height: 420px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 12px;
      font: 0.95rem/1.45 ui-monospace, SFMono-Regular, Menlo, monospace;
      background: #fff;
      color: var(--ink);
    }}
    .row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }}
    button {{
      border: 1px solid var(--ink);
      background: var(--ink);
      color: #fff;
      border-radius: 999px;
      padding: 8px 14px;
      font: 0.92rem/1 ui-sans-serif, system-ui, sans-serif;
      cursor: pointer;
    }}
    button.secondary {{ background: transparent; color: var(--ink); }}
    button.up.is-selected {{ background: var(--good); border-color: var(--good); color: #fff; }}
    button.down.is-selected {{ background: var(--bad); border-color: var(--bad); color: #fff; }}
    label {{ display: block; margin-top: 12px; font: 0.92rem/1.3 ui-sans-serif, system-ui, sans-serif; }}
    #missing-wrap {{ display: none; }}
    #missing {{
      width: 100%;
      min-height: 90px;
      margin-top: 6px;
      font-family: ui-sans-serif, system-ui, sans-serif;
    }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin: 4px 0; }}
    code {{ font: 0.86rem/1 ui-monospace, SFMono-Regular, Menlo, monospace; }}
    #notice {{
      min-height: 1.4em;
      margin-top: 12px;
      font: 0.92rem/1.3 ui-sans-serif, system-ui, sans-serif;
    }}
    footer {{
      margin-top: 16px;
      color: var(--muted);
      font: 0.9rem/1.4 ui-sans-serif, system-ui, sans-serif;
    }}
    @media (max-width: 800px) {{
      .grid {{ grid-template-columns: 1fr; }}
      header {{ flex-direction: column; align-items: flex-start; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <p class="eyebrow">Rose Rocket · human side of the line</p>
        <h1>Review desk</h1>
      </div>
      <div id="status" class="status { _escape('approved' if approved else status) }">{_escape(status_label)}</div>
    </header>
    <p class="rule">{_escape(packet.get("line", ""))}</p>
    <div class="grid">
      <section>
        <h2>{_escape(packet.get("edition", "Edition"))} · {_escape(packet.get("feature", ""))}</h2>
        <label for="draft">Draft</label>
        <textarea id="draft">{_escape(markdown)}</textarea>
        <div class="row">
          <button type="button" id="save" class="secondary">Save edits</button>
          <button type="button" id="approve">Approve / Send</button>
        </div>
        <p id="notice" role="status"></p>
      </section>
      <div>
        <section>
          <h2>Was this helpful?</h2>
          <div class="row">
            <button type="button" id="up" class="secondary up">Yes</button>
            <button type="button" id="down" class="secondary down">No</button>
          </div>
          <div id="missing-wrap">
            <label for="missing">What was missing?</label>
            <textarea id="missing" placeholder="Optional. Say what the draft left out."></textarea>
          </div>
          <div class="row">
            <button type="button" id="rate" class="secondary">Save rating</button>
          </div>
        </section>
        <section style="margin-top:18px">
          <h2>Model tiers</h2>
          <ul>{tier_rows}</ul>
        </section>
        <section style="margin-top:18px">
          <h2>Automated already</h2>
          <ul>{stages}</ul>
        </section>
        <section style="margin-top:18px">
          <h2>Admin queue</h2>
          <ul>{queue}</ul>
        </section>
      </div>
    </div>
    <footer>{_escape(ritual_line)}. Run PROMPT_REVIEW=1 for the digest.</footer>
  </main>
  <script>
    const up = document.getElementById("up");
    const down = document.getElementById("down");
    const missingWrap = document.getElementById("missing-wrap");
    const notice = document.getElementById("notice");
    let rating = "";

    function select(next) {{
      rating = next;
      up.classList.toggle("is-selected", next === "up");
      down.classList.toggle("is-selected", next === "down");
      missingWrap.style.display = next === "down" ? "block" : "none";
      if (next !== "down") document.getElementById("missing").value = "";
    }}
    up.addEventListener("click", () => select("up"));
    down.addEventListener("click", () => select("down"));

    async function post(url, payload) {{
      const response = await fetch(url, {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify(payload)
      }});
      const data = await response.json();
      if (!response.ok || data.ok === false) {{
        throw new Error(data.error || "Request failed");
      }}
      return data;
    }}

    document.getElementById("save").addEventListener("click", async () => {{
      try {{
        await post("/save", {{ markdown: document.getElementById("draft").value }});
        notice.textContent = "Edits saved.";
      }} catch (error) {{
        notice.textContent = error.message;
      }}
    }});

    document.getElementById("rate").addEventListener("click", async () => {{
      if (!rating) {{
        notice.textContent = "Choose Yes or No first.";
        return;
      }}
      try {{
        await post("/feedback", {{
          rating,
          what_was_missing: document.getElementById("missing").value
        }});
        notice.textContent = rating === "down" ? "Rating saved with your note." : "Rating saved.";
      }} catch (error) {{
        notice.textContent = error.message;
      }}
    }});

    document.getElementById("approve").addEventListener("click", async () => {{
      try {{
        const data = await post("/approve", {{
          markdown: document.getElementById("draft").value
        }});
        const status = document.getElementById("status");
        status.textContent = "Approved";
        status.className = "status approved";
        notice.textContent = data.message;
      }} catch (error) {{
        notice.textContent = error.message;
      }}
    }});
  </script>
</body>
</html>
"""


class ReviewHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True

    def __init__(
        self,
        server_address,
        packet_path: Path,
        feedback_path: Path,
        escalation_dir: Path,
        ritual_path: Path,
        send_fn: Optional[SendFn],
        dry_run: bool,
    ):
        super().__init__(server_address, ReviewHandler)
        self.packet_path = Path(packet_path)
        self.feedback_path = Path(feedback_path)
        self.escalation_dir = Path(escalation_dir)
        self.ritual_path = Path(ritual_path)
        self.send_fn = send_fn
        self.dry_run = dry_run


class ReviewHandler(BaseHTTPRequestHandler):
    server: ReviewHTTPServer

    def log_message(self, fmt: str, *args) -> None:
        return

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            packet = load_packet(self.server.packet_path)
            page = render_review_page(
                packet,
                list_escalations(self.server.escalation_dir),
                load_ritual(self.server.ritual_path),
            )
            self._bytes(200, page.encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/packet.json":
            self._bytes(
                200,
                self.server.packet_path.read_bytes(),
                "application/json; charset=utf-8",
            )
            return
        self._json(404, {"ok": False, "error": "Not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
        except json.JSONDecodeError:
            self._json(400, {"ok": False, "error": "Body must be JSON"})
            return
        try:
            if path == "/save":
                self._save(payload)
            elif path == "/feedback":
                self._feedback(payload)
            elif path == "/approve":
                self._approve(payload)
            elif path == "/escalation/ack":
                record = acknowledge_escalation(
                    self.server.escalation_dir, str(payload.get("id", "")).strip()
                )
                self._json(200, {"ok": True, "escalation": record})
            else:
                self._json(404, {"ok": False, "error": "Not found"})
        except (ValueError, FileNotFoundError) as exc:
            self._json(400, {"ok": False, "error": str(exc)})
        except Exception as exc:
            self._json(500, {"ok": False, "error": str(exc)})

    def _save(self, payload: dict) -> None:
        markdown = payload.get("markdown")
        if not isinstance(markdown, str) or not markdown.strip():
            raise ValueError("Draft is empty")
        assert_no_banned_words(markdown)
        packet = load_packet(self.server.packet_path)
        packet["markdown"] = markdown
        save_packet(self.server.packet_path, packet)
        self._json(200, {"ok": True})

    def _feedback(self, payload: dict) -> None:
        record = append_feedback(
            self.server.feedback_path,
            str(payload.get("rating", "")),
            str(payload.get("what_was_missing", "")),
        )
        self._json(200, {"ok": True, "feedback": record})

    def _approve(self, payload: dict) -> None:
        markdown = payload.get("markdown")
        packet = load_packet(self.server.packet_path)
        if isinstance(markdown, str) and markdown.strip():
            assert_no_banned_words(markdown)
            packet["markdown"] = markdown
        elif not str(packet.get("markdown", "")).strip():
            raise ValueError("Draft is empty")
        else:
            assert_no_banned_words(str(packet.get("markdown", "")))
        subject = str(packet.get("subject") or "Rose Rocket Engine")
        if self.server.dry_run or self.server.send_fn is None:
            message = "Approved. Gmail skipped."
            draft_id = ""
        else:
            draft_id = self.server.send_fn(subject, packet["markdown"])
            message = f"Approved and drafted in Gmail: {draft_id}"
        packet["approved"] = True
        packet["send_result"] = draft_id or "skipped"
        save_packet(self.server.packet_path, packet)
        self._json(200, {"ok": True, "message": message, "draft_id": draft_id})

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        data = json.loads(raw.decode("utf-8") or "{}")
        if not isinstance(data, dict):
            raise json.JSONDecodeError("object required", "", 0)
        return data

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self._bytes(status, body, "application/json; charset=utf-8")

    def _bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def start_review_server(
    packet_path: Path,
    *,
    feedback_path: Path,
    escalation_dir: Path,
    ritual_path: Path,
    host: str = "127.0.0.1",
    port: int = 8765,
    send_fn: Optional[SendFn] = None,
    dry_run: bool = True,
) -> ReviewHTTPServer:
    server = ReviewHTTPServer(
        (host, port),
        packet_path,
        feedback_path,
        escalation_dir,
        ritual_path,
        send_fn,
        dry_run,
    )
    return server


def serve_review(server: ReviewHTTPServer) -> None:
    host, port = server.server_address[:2]
    print(f"Review desk: http://{host}:{port}")
    print("Edit the draft, rate it, then Approve / Send. Ctrl-C closes the desk.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nReview desk closed.")
    finally:
        server.server_close()
