# Agent guidelines

- Respond in English unless the user asks for another language.
- Talk to a non-technical reader: lead with the product outcome, the effect on users, and the risks; add technical detail only when it helps.
- Start with the result or the next action. Remove preambles, repetition, closing pleasantries, and irrelevant digressions.
- When the user needs to do several things, give a short numbered sequence: one item, one action. End with the single nearest next step.
- Report an error concretely: what happened, where the cause is, and how to fix it.
- Never install, run, or recommend `ngrok` or any other traffic-tunnelling tool.
- Use [mishanaer/deslop/primitives](https://github.com/mishanaer/deslop/blob/main/primitives/README.md) as the design system. Look for existing components and tokens first; do not create local equivalents or add another design system without a direct request.
- After changes, verify the result and state what works now, which checks ran, what was not verified, and which risks remain.
