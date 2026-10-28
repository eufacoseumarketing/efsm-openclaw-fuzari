## Description:

Best practices for Remotion - Video creation in React.

This skill is ready for commercial/non-commercial use.

## Publisher:

[am-will](https://clawhub.ai/user/am-will)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when working with Remotion code to apply domain-specific patterns for React-based video composition, animation, assets, audio, captions, media metadata, and rendering behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package-manager commands in the examples could change a project dependency graph if run without review.

Mitigation: Ask the agent to confirm before running install commands, prefer pinned package versions, and keep lockfiles under review.

Risk: Remote URLs used for media, captions, Lottie assets, or metadata extraction can introduce reliability and server-side rendering exposure.

Mitigation: Validate or allowlist remote URLs, confirm CORS behavior where relevant, and avoid untrusted inputs in rendering or metadata workflows.

Risk: The release is a Remotion reference skill rather than security-hardened production guidance.

Mitigation: Review generated code and configuration before deployment and scan project changes through the normal release process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/am-will/skills/remotion-best-practices)
- [Remotion Tailwind CSS Documentation](https://www.remotion.dev/docs/tailwind)
- [Remotion Whisper.cpp Documentation](https://remotion.dev/docs/install-whisper-cpp)
- [Remotion Whisper Web Documentation](https://remotion.dev/docs/whisper-web)
- [Remotion OpenAI Whisper Captions Documentation](https://remotion.dev/docs/openai-whisper/openai-whisper-api-to-captions)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript/TSX and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No hidden execution; examples require user review before applying package installs or remote URL workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-01-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
