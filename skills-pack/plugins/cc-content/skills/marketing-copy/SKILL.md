---
name: marketing-copy
description: Write and review marketing assets - positioning, landing pages, homepage copy, email sequences, ads, pricing pages, case studies, and conversion-rate (CRO) reviews - built on a saved product context file. Use when the user asks for marketing copy, a value proposition, a launch plan, a cold or nurture email sequence, ad variations, A/B test ideas, or "why isn't this page converting".
---

# Marketing Copy

## Step 0: Product context (once per product)

Look for `.agents/product-marketing-context.md` or `marketing-context.md` in the project. If missing, interview the user and create it:

```markdown
# Product marketing context
Product: <name, one-line what it is>
Customer: <role, company type, size, region>
Pain: <the problem in the customer's words>
Current alternative: <what they do today>
Outcome: <measurable result, with real numbers if available>
Proof: <clients, certifications, case results, testimonials (real only)>
Differentiators: <max 3, each provable>
Objections: <top 3 and answers>
Voice: <3 adjectives, words to use, words to avoid>
Offer / CTA: <what the reader should do next>
```

All later tasks read this file. Never invent proof points. Mark gaps as `[NEED: client logo / metric]`.

## Frameworks (pick one per asset)

| Asset | Framework |
|---|---|
| Positioning | April Dunford: alternatives > unique attributes > value > target customer > market category |
| Landing page | Hero (outcome + for whom) > proof strip > problem > how it works (3 steps) > benefits with evidence > objections/FAQ > CTA |
| Email (cold) | Observation about them > problem > one-line proof > soft ask. Under 90 words. |
| Email sequence | Day 0 value, Day 2 story/case, Day 5 objection, Day 8 offer, Day 12 breakup |
| Ads | PAS (problem, agitate, solve) and a direct-benefit variant. 3 headlines x 2 descriptions. |
| Case study | Situation > challenge > approach > result (numbers) > quote |

## Procedure

1. Confirm the asset, audience, channel, and single goal (one CTA).
2. Draft 2 variants with different angles (e.g. risk reduction vs cost saving).
3. Score each against the checklist below. Revise.
4. Deliver with: the copy, the angle of each variant, and an A/B test suggestion with a success metric.

## Copy checklist

- [ ] Headline states an outcome for a specific reader, under 10 words.
- [ ] Every claim has proof or is marked `[NEED]`.
- [ ] Reader's words, not internal jargon.
- [ ] One CTA, repeated, action verb + outcome ("Book a 20-minute site risk review").
- [ ] Readable at grade 8 or below for general audiences.
- [ ] No hype words (revolutionary, world-class, best-in-class, seamless).
- [ ] UAE/GCC context where relevant: bilingual EN/AR needs, regulator names, local proof.

## CRO review mode

For an existing page, score 1 to 5 on: clarity of offer (5-second test), relevance to traffic source, proof, friction (form fields, load time), CTA visibility, mobile. Output the 5 highest-impact changes with a hypothesis each: "Changing X to Y will raise Z because ...".

## Compliance
- No fake testimonials, invented statistics, or competitor claims you cannot back.
- Email: include sender identity and an opt-out. Respect the UAE PDPL and the recipient country's rules.
