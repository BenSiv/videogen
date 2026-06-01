# Video Script Draft: Open Source Projects Overview

## 1. Introduction
Hi everyone, my name is Ben. This is the first video in a series where I want to share some of my open source projects. I don't have a specific agenda for this—my main goal is simply to get the conversation going. If you find these projects interesting and want to contribute in any way, I'd absolutely love that.

## 2. Background
To give you a little background about myself: I am a data scientist and software engineer, with formal training in bioinformatics and biotechnology. I hold a master's degree in biotechnology, and my research was primarily focused on plant science and genetic engineering. 

My experience spans everything from the genetic editing of plants and crop breeding, all the way to cellular agriculture. Currently, I work for a company that produces cocoa ingredients, where we grow actual cocoa cells from seeds in bioreactors to produce cocoa mass for chocolate production.

## 3. Technology Philosophy
In terms of technology, I'm drawn to tools that are simple, highly composable, and act as atomic building blocks. This philosophy is the foundation for the projects I want to share with you today.

## 4. Project 1: Fossil-based Knowledge Management
The first space I am specifically interested in is knowledge management. I've been working on an adaptation of an established open source project called Fossil SCM. Fossil is a version control and knowledge management software originally created by Richard Hipp, the creator of SQLite. Unsurprisingly, it uses an SQLite database as its backbone. Many people call it "GitHub in a box" because it features a built-in server that you can deploy locally, complete with a web interface to interact with your repository.

My idea is to adapt Fossil to act as a general knowledge management system, rather than strictly for source control. The biggest hurdle with most knowledge management software today is the manual processing stage. Capturing and organizing knowledge is typically treated as a separate, tedious task. But it doesn't have to be. 

When we retrieve information from our memory during a conversation, we naturally process it and generate new thoughts on the fly. I want persisting knowledge management software that mimics this process using large language models. The concept is simple: as you write notes and interact with the model, it retrieves relevant information in the background, bubbling up context based on the conversation you're having. 

These notes are then automatically sorted into different processing tiers—from extremely raw, as-retrieved notes, to semi-processed connections, up to fully self-contained atomic wiki notes. As you use the vault more, it becomes smarter, more adaptive, and highly relevant to your workflow.

## 5. Project 2: Brain EX
This leads into another tool I call "Brain X"—a brain extension. I originally started using Obsidian as my notes vault because it has an excellent interface and offers the flexibility of a local, schema-less system. However, keeping the app open and needing to switch contexts to write a note disrupts my workflow. I am a terminal dweller; I work in the terminal all day long. 

So, I built a command-line interface that allows you to take notes exactly where you are. It can connect into an Obsidian vault and work in tandem with it, or be used completely independently. It also seamlessly combines note-taking with task management. Most of the time, I'm not writing long-form notes—I'm jotting down one-liners and reminders. Brain X captures those efficiently so I can return to them later. Then, using natural language processing, we can feed this information back into the Fossil repository while keeping the files accessible as readable markdown text.

## 6. Project 3: Filament
On a similar note, I want to share the "Filament" project. I'm a big fan of true crime podcasts and non-fiction detective shows. Filament is designed to draw information from open datasets regarding unidentified human remains and missing persons. Its goal is to connect loose threads and build a coherent narrative that can help explain what happened and bring closure. 

It uses Retrieval-Augmented Generation (RAG) and natural language processing to score, rank, and match different pieces of information. Naturally, the more data we have, the better the results. Because so much of this information is currently locked in law enforcement databases rather than open platforms, this is an area where open collaboration could make a massive difference.

## 7. Project 4: LuaM
Finally, I want to talk about a language project called Lua M. It is a minimalized and modernized dialect of the Lua programming language. I really appreciate Lua's simplicity, but in Lua M, I've removed certain features—like object-oriented metatables—to enforce a purely procedural and highly concise syntax. 

The philosophy behind Lua M is to provide a single, straightforward way to accomplish a task. For example, it uses standard syntax conventions like a double equals sign to denote equality. Several of my projects already use Lua M as their backbone.

## 8. Outro
Thank you for checking out the start of this series. I’m excited to share these tools with you all, and I welcome any thoughts, feedback, or potential contributions.
