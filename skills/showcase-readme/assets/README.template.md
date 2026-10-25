<!-- Placeholders in {{…}}. Badge colors ({{BG}}, {{ACCENT}}…) are palette hex codes without "#". Delete sections that do not apply. -->
<a id="top"></a>

<div align="center">

<img width="100%" alt="{{BANNER_ALT}}" src="docs/assets/banner-en.svg" />

<p><strong>{{ONE_LINE_PITCH}}</strong><br/>
{{CORE_ACTION_SENTENCE}}</p>

<p>
<a href="{{RELEASES_URL}}"><img src="https://img.shields.io/github/v/release/{{OWNER}}/{{REPO}}?style=for-the-badge&labelColor={{BG}}&color={{ACCENT}}" alt="Release"></a>
<a href="{{CI_URL}}"><img src="https://img.shields.io/github/actions/workflow/status/{{OWNER}}/{{REPO}}/{{CI_FILE}}?branch={{BRANCH}}&style=for-the-badge&labelColor={{BG}}&color={{ACCENT}}&label=CI" alt="CI"></a>
<img src="https://img.shields.io/badge/{{PLATFORM}}-{{ACCENT2}}?style=for-the-badge&labelColor={{BG}}" alt="{{PLATFORM_ALT}}">
<a href="LICENSE"><img src="https://img.shields.io/badge/license-{{LICENSE}}-{{MUTED}}?style=for-the-badge&labelColor={{BG}}" alt="License: {{LICENSE}}"></a>
</p>

<p>
<a href="#install"><strong>Install</strong></a> &bull;
<a href="#how-it-works"><strong>How it works</strong></a> &bull;
<a href="#{{REFERENCE_ANCHOR}}"><strong>{{REFERENCE_TITLE}}</strong></a> &bull;
<a href="#build-from-source"><strong>Build</strong></a>
</p>

<p><strong>English</strong> &bull; <a href="README.{{LANG}}.md">{{LANG_NAME}}</a></p>

</div>

---

{{PITCH: the pain in one sentence, then what this project does about it.}}

<div align="center">
<img width="720" alt="{{DEMO_ALT}}" src="docs/assets/demo-en.gif" />
<br/><sub>{{DEMO_CAPTION: say it is a real run}}</sub>
</div>

## Features

- **{{Lead phrase}}.** {{One sentence.}}

<table>
<tr>
<td width="50%"><img alt="{{SHOT_1_ALT}}" src="docs/assets/{{shot-1}}.png" /></td>
<td width="50%"><img alt="{{SHOT_2_ALT}}" src="docs/assets/{{shot-2}}.png" /></td>
</tr>
<tr>
<td align="center"><sub><strong>{{Verb}}.</strong> {{caption}}</sub></td>
<td align="center"><sub><strong>{{Verb}}.</strong> {{caption}}</sub></td>
</tr>
</table>

## Install

```sh
{{FASTEST_INSTALL_COMMAND}}
```

<details>
<summary><b>{{Alternative install}}</b></summary>

{{steps}}

</details>

## How it works

| | |
|---|---|
| **{{Term}}** | {{One-line definition.}} |

## {{REFERENCE_TITLE}}

{{Commands, shortcuts, config or formats as tables and code blocks.}}

## Build from source

```sh
{{BUILD_AND_TEST_COMMANDS}}
```

{{Where contributor docs live; how to regenerate docs/assets.}}

## License

[{{LICENSE}}](LICENSE).

<div align="center">
<br/>
<img src="docs/assets/logo.svg" width="48" alt="{{NAME}} logo" />
<br/>
<sub>{{TAGLINE}} · <a href="#top">back to top ↑</a></sub>
</div>
