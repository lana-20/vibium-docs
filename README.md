# vibium-docs

An independent, complete command reference for the
[Vibium](https://github.com/VibiumDev/vibium) browser automation CLI, built with
Docusaurus.

**→ [lana-20.github.io/vibium-docs](https://lana-20.github.io/vibium-docs/)**

The official documentation covers 16 of the CLI's 67 commands. This site covers
all 67, plus their 37 subcommands.

> Community-maintained and not affiliated with the Vibium project. Where this
> site disagrees with upstream, upstream wins.

## Artefacts

| | |
| --- | --- |
| Live site | https://lana-20.github.io/vibium-docs/ |
| Repository | https://github.com/lana-20/vibium-docs |
| Introduction | https://lana-20.github.io/vibium-docs/docs/intro |
| Command reference | https://lana-20.github.io/vibium-docs/docs/commands |
| Global flags | https://lana-20.github.io/vibium-docs/docs/global-flags |
| Playground fixture | https://lana-20.github.io/vibium-docs/fixtures/playground.html |
| Second page (navigation demos) | https://lana-20.github.io/vibium-docs/fixtures/playground2.html |
| Fixture logo | https://lana-20.github.io/vibium-docs/fixtures/logo.svg |
| Annotate example image | https://lana-20.github.io/vibium-docs/img/annotate-example.png |
| Deploy workflow | [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) |
| Page generator | [`scripts/gen_pages.py`](scripts/gen_pages.py) |

### The playground fixture

Every example on a verified page runs against
[`static/fixtures/playground.html`](static/fixtures/playground.html), served by
this site. That is deliberate: output captured against a third-party page rots
silently when someone else's markup changes, and this fixture only changes when
this repo does.

It carries a nav, a form (labelled email input, select, checkbox, search field,
submit and icon buttons), an interactions section (a counter, a **disabled**
button, a button whose effect is delayed by one second, a link to a second
page), and filler content tall enough that `--full-page` is demonstrable.
New elements are added **after** the existing ones so element references
`@e1`–`@e9` stay stable; anything added shows up as `@e10` and beyond.

## Two tiers of page

The reference is explicit about where each page's content comes from, because
the two kinds are not equally trustworthy:

| Tier | Source |
| --- | --- |
| **Verified** | Real terminal output captured from a live browser, against the fixture above. |
| **Generated** | The binary's own help text, via `scripts/gen_pages.py`. Accurate on syntax and flags; the examples are the binary's built-in samples. |

Every page states its tier at the top. Promoting a page means writing real
captured output into it and adding its name to `CURATED` in the generator, after
which the generator will never overwrite it.

## Command status

<!-- BEGIN COMMAND STATUS -->

**11 of 67 verified** — 56 still generated from `--help`. Measured against `vibium v26.8.21`.

<details open>
<summary><strong>Navigation</strong> — 5/6 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [ ] | [`go`](https://lana-20.github.io/vibium-docs/docs/commands/go) | Go to a URL and print page info |
| [x] | [`back`](https://lana-20.github.io/vibium-docs/docs/commands/back) | Navigate back in browser history |
| [x] | [`forward`](https://lana-20.github.io/vibium-docs/docs/commands/forward) | Navigate forward in browser history |
| [x] | [`reload`](https://lana-20.github.io/vibium-docs/docs/commands/reload) | Reload the current page |
| [x] | [`url`](https://lana-20.github.io/vibium-docs/docs/commands/url) | Get the current page URL |
| [x] | [`title`](https://lana-20.github.io/vibium-docs/docs/commands/title) | Get the current page title |

</details>

<details open>
<summary><strong>Mapping & references</strong> — 1/2 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [x] | [`map`](https://lana-20.github.io/vibium-docs/docs/commands/map) | Map interactive page elements with @refs |
| [ ] | [`diff`](https://lana-20.github.io/vibium-docs/docs/commands/diff) | Compare current state vs previous |

</details>

<details open>
<summary><strong>Finding elements</strong> — 1/4 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [x] | [`find`](https://lana-20.github.io/vibium-docs/docs/commands/find) | Find elements by CSS selector or semantic locator |
| [ ] | [`frame`](https://lana-20.github.io/vibium-docs/docs/commands/frame) | Find a frame by name or URL substring |
| [ ] | [`frames`](https://lana-20.github.io/vibium-docs/docs/commands/frames) | List all child frames (iframes) on the page |
| [ ] | [`count`](https://lana-20.github.io/vibium-docs/docs/commands/count) | Count matching elements |

</details>

<details open>
<summary><strong>Interacting</strong> — 2/16 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [x] | [`click`](https://lana-20.github.io/vibium-docs/docs/commands/click) | Click an element (optionally navigate to URL first) |
| [ ] | [`dblclick`](https://lana-20.github.io/vibium-docs/docs/commands/dblclick) | Double-click an element |
| [x] | [`fill`](https://lana-20.github.io/vibium-docs/docs/commands/fill) | Clear an input field and type new text |
| [ ] | [`type`](https://lana-20.github.io/vibium-docs/docs/commands/type) | Type text into an element (optionally navigate to URL first) |
| [ ] | [`press`](https://lana-20.github.io/vibium-docs/docs/commands/press) | Press a key on a specific element or the focused element |
| [ ] | [`keys`](https://lana-20.github.io/vibium-docs/docs/commands/keys) | Press a key or key combination |
| [ ] | [`check`](https://lana-20.github.io/vibium-docs/docs/commands/check) | Check a checkbox or radio button |
| [ ] | [`uncheck`](https://lana-20.github.io/vibium-docs/docs/commands/uncheck) | Uncheck a checkbox |
| [ ] | [`select`](https://lana-20.github.io/vibium-docs/docs/commands/select) | Select an option in a &lt;select&gt; element |
| [ ] | [`hover`](https://lana-20.github.io/vibium-docs/docs/commands/hover) | Hover over an element by CSS selector |
| [ ] | [`focus`](https://lana-20.github.io/vibium-docs/docs/commands/focus) | Focus an element |
| [ ] | [`drag`](https://lana-20.github.io/vibium-docs/docs/commands/drag) | Drag from one element to another |
| [ ] | [`upload`](https://lana-20.github.io/vibium-docs/docs/commands/upload) | Set files on an input[type=file] element |
| [ ] | [`scroll`](https://lana-20.github.io/vibium-docs/docs/commands/scroll) | Scroll the page or an element |
| [ ] | [`mouse`](https://lana-20.github.io/vibium-docs/docs/commands/mouse) | Mouse control (click, move, down, up) |
| [ ] | [`highlight`](https://lana-20.github.io/vibium-docs/docs/commands/highlight) | Highlight an element with a red outline for 3 seconds |

</details>

<details>
<summary><strong>Reading page state</strong> — 0/7 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [ ] | [`text`](https://lana-20.github.io/vibium-docs/docs/commands/text) | Get text content of the page or an element |
| [ ] | [`html`](https://lana-20.github.io/vibium-docs/docs/commands/html) | Get HTML content of the page or an element |
| [ ] | [`attr`](https://lana-20.github.io/vibium-docs/docs/commands/attr) | Get an HTML attribute value from an element |
| [ ] | [`value`](https://lana-20.github.io/vibium-docs/docs/commands/value) | Get the current value of a form element |
| [ ] | [`a11y-tree`](https://lana-20.github.io/vibium-docs/docs/commands/a11y-tree) | Get the accessibility tree of the current page |
| [ ] | [`is`](https://lana-20.github.io/vibium-docs/docs/commands/is) | Check element state (visible, enabled, checked, actionable) |
| [ ] | [`content`](https://lana-20.github.io/vibium-docs/docs/commands/content) | Replace the page HTML content |

</details>

<details open>
<summary><strong>Capture</strong> — 1/4 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [x] | [`screenshot`](https://lana-20.github.io/vibium-docs/docs/commands/screenshot) | Capture a screenshot (optionally navigate to URL first) |
| [ ] | [`pdf`](https://lana-20.github.io/vibium-docs/docs/commands/pdf) | Save page as PDF |
| [ ] | [`eval`](https://lana-20.github.io/vibium-docs/docs/commands/eval) | Evaluate a JavaScript expression (optionally navigate to URL first) |
| [ ] | [`record`](https://lana-20.github.io/vibium-docs/docs/commands/record) | Record browser sessions (screenshots and snapshots) |

</details>

<details open>
<summary><strong>Waiting</strong> — 1/2 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [x] | [`wait`](https://lana-20.github.io/vibium-docs/docs/commands/wait) | Wait for an element, URL, text, page load, or JS condition |
| [ ] | [`sleep`](https://lana-20.github.io/vibium-docs/docs/commands/sleep) | Pause execution for a number of milliseconds |

</details>

<details>
<summary><strong>Browser & session</strong> — 0/16 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [ ] | [`start`](https://lana-20.github.io/vibium-docs/docs/commands/start) | Start a browser session. Without arguments, launches a local browser. |
| [ ] | [`stop`](https://lana-20.github.io/vibium-docs/docs/commands/stop) | Stop the browser session |
| [ ] | [`daemon`](https://lana-20.github.io/vibium-docs/docs/commands/daemon) | Manage the vibium daemon (background browser process) |
| [ ] | [`page`](https://lana-20.github.io/vibium-docs/docs/commands/page) | Manage browser pages (new, close, switch) |
| [ ] | [`pages`](https://lana-20.github.io/vibium-docs/docs/commands/pages) | List all open browser pages |
| [ ] | [`viewport`](https://lana-20.github.io/vibium-docs/docs/commands/viewport) | Get or set the browser viewport size |
| [ ] | [`window`](https://lana-20.github.io/vibium-docs/docs/commands/window) | Get or set the OS browser window size, position, or state |
| [ ] | [`install`](https://lana-20.github.io/vibium-docs/docs/commands/install) | Download the selected browser (Chrome for Testing by default) |
| [ ] | [`is-installed`](https://lana-20.github.io/vibium-docs/docs/commands/is-installed) | Check if the selected browser is installed (exit 0 = yes, exit 1 = no) |
| [ ] | [`paths`](https://lana-20.github.io/vibium-docs/docs/commands/paths) | Print browser and cache paths |
| [ ] | [`storage`](https://lana-20.github.io/vibium-docs/docs/commands/storage) | Export or restore browser state (cookies, localStorage, sessionStorage) |
| [ ] | [`cookies`](https://lana-20.github.io/vibium-docs/docs/commands/cookies) | Manage browser cookies |
| [ ] | [`download`](https://lana-20.github.io/vibium-docs/docs/commands/download) | Manage browser downloads |
| [ ] | [`dialog`](https://lana-20.github.io/vibium-docs/docs/commands/dialog) | Handle browser dialogs (alert, confirm, prompt) |
| [ ] | [`geolocation`](https://lana-20.github.io/vibium-docs/docs/commands/geolocation) | Override the browser geolocation |
| [ ] | [`media`](https://lana-20.github.io/vibium-docs/docs/commands/media) | Override CSS media features |

</details>

<details>
<summary><strong>Agent integration</strong> — 0/4 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [ ] | [`mcp`](https://lana-20.github.io/vibium-docs/docs/commands/mcp) | Start the Model Context Protocol (MCP) server. |
| [ ] | [`add-skill`](https://lana-20.github.io/vibium-docs/docs/commands/add-skill) | Install Vibium browser skill for Claude Code |
| [ ] | [`pipe`](https://lana-20.github.io/vibium-docs/docs/commands/pipe) | Start vibium in pipe mode where protocol messages are exchanged |
| [ ] | [`serve`](https://lana-20.github.io/vibium-docs/docs/commands/serve) | Start WebSocket proxy server for browser automation |

</details>

<details>
<summary><strong>Diagnostics</strong> — 0/3 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [ ] | [`launch-test`](https://lana-20.github.io/vibium-docs/docs/commands/launch-test) | Launch the selected browser and print BiDi session info |
| [ ] | [`bidi-test`](https://lana-20.github.io/vibium-docs/docs/commands/bidi-test) | Launch browser, connect via BiDi, send session.status |
| [ ] | [`ws-test`](https://lana-20.github.io/vibium-docs/docs/commands/ws-test) | Test WebSocket connection (type messages, see echoes) |

</details>

<details>
<summary><strong>Meta</strong> — 0/3 verified</summary>

| | Command | Description |
| --- | --- | --- |
| [ ] | [`version`](https://lana-20.github.io/vibium-docs/docs/commands/version) | Print the version number |
| [ ] | [`help`](https://lana-20.github.io/vibium-docs/docs/commands/help) | Help provides help for any command in the application. |
| [ ] | [`completion`](https://lana-20.github.io/vibium-docs/docs/commands/completion) | Generate a shell completion script. |

</details>

<!-- END COMMAND STATUS -->

## Regenerating

`scripts/gen_pages.py` reads the **installed** `vibium` binary, so the reference
can be re-derived after any release:

```sh
python3 scripts/gen_pages.py            # uses `vibium` from PATH
python3 scripts/gen_pages.py --bin /path/to/vibium
```

It rewrites every non-curated page, `docs/commands/index.mdx`,
`docs/global-flags.mdx`, and the checklist above.

Two guards make silent drift impossible rather than merely unlikely:

- A command in the binary that is missing from `CATEGORIES` is a **hard error**,
  so a newly added command cannot quietly fail to appear in the sidebar.
- A category entry that no longer exists in the binary is likewise a hard error.

It shells out to `vibium help <cmd>` rather than `vibium <cmd> --help`, because
on v26.8.21 the latter is broken for `fill`, `type`, `geolocation` and `sleep` —
they set `DisableFlagParsing` and surface `--help` as an arity error
(upstream [#422](https://github.com/VibiumDev/vibium/issues/422),
[#423](https://github.com/VibiumDev/vibium/issues/423)). The generator also
fails loudly if any help invocation returns an error instead of help text.

## Developing

```sh
npm install
npm start          # dev server with hot reload
npm run build      # production build; fails on any broken link or anchor
npm run serve      # serve the production build
```

The build runs with `onBrokenLinks`, `onBrokenAnchors` and
`onBrokenMarkdownLinks` all set to `throw`, so a bad cross-reference fails CI
rather than shipping. Pushing to `main` deploys via GitHub Actions.

> Static files are not routes, so links to the fixture must use Docusaurus's
> `pathname://` prefix or the broken-link checker will reject them.

## Layout

| Path | What |
| --- | --- |
| `docs/intro.mdx` | landing page and orientation |
| `docs/global-flags.mdx` | generated from the root help |
| `docs/commands/index.mdx` | generated overview, all 67 grouped by purpose |
| `docs/commands/*.mdx` | one page per command, subcommands inline |
| `static/fixtures/` | the playground pages the verified examples run against |
| `scripts/gen_pages.py` | the generator, and the source of truth for categories |
| `.github/workflows/deploy.yml` | build and deploy to GitHub Pages |
