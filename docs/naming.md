<!--
SPDX-FileCopyrightText: 2026 Paul Bunch

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Project Name Selection

This document explains the choice of the project name, its semantic etymology, namespace system, and accepted architectural trade-offs.

## 1. Etymology and Semantic Layers

The name **`sint`** (pronounced as *"sint"*) is a concise system root located at the intersection of programming, artificial intelligence, and physical robotics:

* **Synt**hetic (Synthetic morphology) — the transition of digital AI from a virtual environment to an embodied synthetic form.
* **Int**erface (Physical interface) — a gateway for direct autonomous interaction of LLM/VLA models with the real world.
* **Int**elligence (Distributed intelligence) — autonomy of joints and computation at every level of the physical structure.

## 2. Comparative Analysis (Pros & Cons)

### Benefits
* **Ergonomics and CLI:** 4 characters, typed in a single pass on the keyboard. Ideal for command-line utilities (`sintctl`), package managers, and repositories.
* **Avoiding Clichés:** Does not contain outdated constructs (`Robot`, `Arm`, `Bot`, `Evo`), emphasizing the shift from human-centric robotics toward DFAA (Design for Autonomous Assembly).
* **System Scalability:** The name forms concise namespaces without visual noise.

### Trade-offs
* **High Abstraction:** Without reading the specification, an outside observer might not immediately understand that this refers to a physical manipulator.
* **Semantic Dependency:** In English, `sint` is not a standalone word — the semantic load relies entirely on the project documentation.
* **Phonetic Similarity:** Risk of confusion with the word *synth* (musical synthesizer) or with the mathematical function `sin(t)`.
