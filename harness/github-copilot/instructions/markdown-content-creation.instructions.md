---
applyTo: "**/*.md"
description: "Enforces Markdown content creation conventions for blog post structure, YAML front matter, headings, lists, code blocks, links, images, tables, line length, and validation."
name: "Markdown Content Creation Conventions"
---

# Markdown Content Creation Conventions — Blog Post Readiness

These instructions apply to Markdown content files for blog posts and similar authored pages. They are authoritative for content structure, YAML front matter metadata, editorial formatting, images, tables, line length, and publication validation in matched files; the CommonMark Markdown Conventions instruction remains authoritative for low-level Markdown parsing rules when syntax details conflict.

## Responsibility Split

This file owns blog and content readiness: metadata fields, no-authored-H1 policy, section hierarchy, accessibility-friendly images, content validation, and publication hygiene. CommonMark Markdown Conventions owns the CommonMark syntax model for headings, blocks, lists, fenced code, links, images, autolinks, HTML, and inline parsing.

## Front Matter and Metadata

Start content files with YAML front matter when the publishing system requires metadata. Include the required fields and keep values accurate before publication.

| Field | Requirement |
| --- | --- |
| `post_title` | The displayed title of the post. |
| `author1` | The primary author of the post. |
| `post_slug` | The URL slug for the post. |
| `microsoft_alias` | The Microsoft alias of the author. |
| `featured_image` | The URL of the featured image. |
| `categories` | Categories for the post; choose values from `/categories.txt`. |
| `tags` | Searchable tags for the post. |
| `ai_note` | Indicates whether AI was used in creating the post. |
| `summary` | A brief summary of the post; recommend a concise summary from the content when possible. |
| `post_date` | The publication date of the post. |

Do not invent category names outside `/categories.txt`. Keep slugs stable once a post is published unless the publishing owner approves a redirect or migration.

## Headings and Structure

Use headings to describe the content hierarchy without conflicting with the generated page title.

- Do not write an H1 heading in the Markdown body; the publishing system generates it from the title.
- Use `##` for H2 sections and `###` for H3 subsections.
- Keep headings hierarchical; do not jump from H2 to H4.
- Recommend restructuring when content needs H4, and more strongly recommend restructuring when it needs H5.
- Separate sections with blank lines and keep whitespace intentional.

## Lists, Code Blocks, Links, Images, and Tables

| Element | Convention |
| --- | --- |
| Lists | Use `-` for bullet points and `1.` for numbered lists; indent nested lists with two spaces. |
| Code blocks | Use fenced code blocks with a language identifier such as `csharp` after the opening backticks. |
| Links | Use `[link text](URL)` with descriptive link text and a valid, accessible URL. |
| Images | Use `![alt text](image URL)` and include a brief useful description in the alt text. |
| Tables | Use Markdown tables with `|`, a header row, and aligned columns. |
| Whitespace | Use blank lines to separate sections and avoid excessive whitespace. |

Use numbered lists for ordered processes and bullet lists for unordered collections. Keep code snippets focused on the concept being taught.

## Readability and Validation

Limit authored lines to 400 characters for validator compliance and prefer wrapping prose near 80 characters when it improves readability. Use soft line breaks for long paragraphs rather than forced hard breaks unless the publishing format requires them. Run the repository's Markdown content validation tools when available and fix warnings before publication.

## Good / Bad Examples

The examples below illustrate blog-ready metadata and body structure.

**Good:**

```markdown
---
post_title: "Build reliable widgets"
author1: "A. Author"
post_slug: "build-reliable-widgets"
microsoft_alias: "aauthor"
featured_image: "featured-image-url"
categories: ["Developer"]
tags: ["widgets"]
ai_note: "AI assisted draft reviewed by the author."
summary: "Practical patterns for reliable widgets."
post_date: "2026-08-17"
---

## Overview

Introduce the topic with a short paragraph.

### Implementation

```csharp
Console.WriteLine("Hello");
```
```

Why: The post has required metadata, no body H1, hierarchical headings, and a fenced code block with a language identifier.

**Bad:**

```markdown
# Build reliable widgets

#### Random details

```
Console.WriteLine("Hello");
```
```

Why: The body duplicates the generated H1, jumps heading levels, and omits the code block language identifier.

## Conventions

| Rule | Rationale |
| --- | --- |
| Include required YAML front matter fields before content | Publishing systems need metadata for routing, attribution, taxonomy, and display. |
| Use categories from `/categories.txt` | Category validation fails on unsupported taxonomy values. |
| Do not include an H1 in the Markdown body | The page title is generated from `post_title`. |
| Use H2 and H3 headings hierarchically | Readers and assistive technologies can navigate the document. |
| Use fenced code blocks with language identifiers | Code is readable and syntax highlighting works. |
| Use descriptive links and image alt text | Content remains accessible and meaningful out of context. |
| Keep lines within 400 characters and wrap near 80 characters when practical | Validators pass while prose remains reviewable. |
| Use Markdown tables only for true tabular data | Tables stay readable and accessible. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Put `post_title`, `author1`, `post_slug`, `microsoft_alias`, `featured_image`, `categories`, `tags`, `ai_note`, `summary`, and `post_date` in front matter | Publish content with missing required metadata. |
| Use `##` and `###` for body sections | Add a body `#` heading. |
| Indent nested lists with two spaces | Mix arbitrary indentation in lists. |
| Label code fences with `csharp` or the correct language | Use unlabeled code fences for snippets. |
| Write descriptive `[link text](URL)` | Use vague link text such as "click here". |
| Add meaningful image alt text | Use empty or decorative alt text for informative images. |
| Run validation tools before publication | Treat validator failures as editorial preferences. |

## Checklist Before Opening a PR

- [ ] YAML front matter is present when the content type requires it.
- [ ] `post_title`, `author1`, `post_slug`, `microsoft_alias`, `featured_image`, `categories`, `tags`, `ai_note`, `summary`, and `post_date` are populated.
- [ ] Categories match entries in `/categories.txt`.
- [ ] The Markdown body does not contain an H1 heading.
- [ ] Headings use `##` and `###` hierarchically; H4 or H5 usage has been restructured or justified.
- [ ] Lists use `-` or `1.` with two-space nested indentation.
- [ ] Code blocks are fenced and specify a language identifier.
- [ ] Links are descriptive and valid.
- [ ] Images use Markdown image syntax with meaningful alt text.
- [ ] Tables have headers and aligned columns.
- [ ] Lines stay within 400 characters and long prose is wrapped for readability where practical.
- [ ] Available Markdown validation tools have been run and issues resolved.
