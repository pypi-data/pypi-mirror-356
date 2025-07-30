# AIRCHIEF

Placeholder - not published yet.

## Installation

```bash
# YOLO
curl -fsSL https://airchief.ai/install | bash

# Package managers
npm i -g airchief@latest                     # or bun/pnpm/yarn
brew install shaneholloman/tap/airchief      # macOS
```

> **Note:** Remove versions older than 0.1.x before installing

### Documentation

For more info on how to configure airchief [**head over to our docs**](https://airchief.ai/docs).

### Contributing

To run airchief locally you need.

- Bun
- Golang 1.24.x

And run.

```bash
bun install
bun run packages/airchief/src/index.ts
```

#### Development Notes

**API Client Generation**: After making changes to the TypeScript API endpoints in `packages/airchief/src/server/server.ts`, you need to regenerate the Go client and OpenAPI specification:

```bash
cd packages/tui
go generate ./pkg/client/
```

This updates the generated Go client code that the TUI uses to communicate with the backend server.

### FAQ

#### How is this different than Claude Code?

It's very similar to Claude Code in terms of capability. Here are the key differences:

- 100% open source
- Not coupled to any provider. Although Anthropic is recommended, airchief can be used with OpenAI, Google or even local models. As models evolve the gaps between them will close and pricing will drop so being provider agnostic is important.
- A focus on TUI. airchief is built by neovim users and the creators of [terminal.shop](https://terminal.shop); we are going to push the limits of what's possible in the terminal.
- A client/server architecture. This for example can allow airchief to run on your computer, while you can drive it remotely from a mobile app. Meaning that the TUI frontend is just one of the possible clients.
