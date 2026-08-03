---
title: OmniRoute
emoji: ⚡
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# OmniRoute on Hugging Face Spaces

This space runs [OmniRoute](https://www.npmjs.com/package/omniroute), a Smart AI Router with Auto Fallback.

## How to use

Once the space is running, you can access the OmniRoute dashboard directly from the Space's UI.

To connect your CLI tools (Cursor, Cline, Codex, etc.), point them to the API base URL of this space:
`https://<your-username>-<your-space-name>.hf.space/v1`

## Environment Variables

You may need to configure your API keys (like OpenAI, Anthropic, etc.) as **Secrets** in the Hugging Face Space settings. OmniRoute will read them from the environment.
