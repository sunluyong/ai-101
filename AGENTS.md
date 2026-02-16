# AI Slide Generator Agent Guide

This document outlines the standard procedure for generating HTML slides from Markdown content.

## Goal
Intelligently synthesize Markdown documentation into a compelling, single-file HTML presentation. The Agent must read, understand, and refine the content—extracting key insights and restructuring them for a slide format—rather than mechanically converting Markdown to HTML.

## Constraints & Requirements
1.  **Format**: Single HTML file (no external local dependencies).
2.  **Styling**: Tailwind CSS (via CDN). **Use Tailwind utility classes directly for all styling. Do not write custom CSS in `<style>` blocks except for essential transition logic and `strong` tag highlighting.**
3.  **Theme (Supabase Inspired)**:
    -   **Background**: Dark Grey (`#121212`).
    -   **Primary Color**: Supabase Green (`#3ECF8E`).
    -   **Text**: Off-white (`#EDEDED`) for better readability.
    -   **Cards/Surfaces**: Darker Grey (`#1C1C1C`) with subtle borders.
    -   **Font**: Sans-serif (`Inter`), optimized for large projection screens.
4.  **Layout**: 16:9 aspect ratio.
5.  **Typography & Layout**:
    -   **Title Slide**: 
        -   Container: `absolute top-0 left-0 w-full h-full flex flex-col justify-center items-center text-center p-[3rem_8rem] bg-[radial-gradient(circle_at_center,#1a1a1a_0%,#121212_70%)]`
        -   H1: `text-[7rem] font-extrabold text-text mb-8 text-center [text-shadow:0_0_40px_rgba(62,207,142,0.1)] leading-[1.1]`
        -   Subtitle: `text-[3rem] text-muted text-center max-w-[80%] font-light leading-[1.5]`
    -   **Content Slides**: 
        -   Container: `absolute top-0 left-0 w-full h-full flex flex-col justify-start items-start text-left p-[3rem_8rem]`
        -   Title (H2): `text-[5rem] font-extrabold text-primary mb-6 text-left w-full leading-[1.2]`
        -   Content left-aligned.
    -   **Font Size**: Optimized for projection visibility.
        -   H3: `text-[2.5rem] font-semibold text-text mb-6 mt-0`
        -   P: `text-[2.4rem] leading-[1.5] text-[#D4D4D4] mb-8 max-w-full text-left`
        -   UL/OL: `text-[2.2rem] leading-[1.6] text-[#D4D4D4] mb-10 max-w-full list-inside text-left space-y-6` (Use `list-disc` or `list-decimal`)
        -   Blockquote: `border-l-[8px] border-primary p-[2rem_3rem] not-italic text-text text-[2.6rem] font-semibold my-12 bg-surface rounded-lg w-full shadow-md block`
        -   Card/Surface Title: `text-[2.5rem] font-semibold text-primary mb-6 mt-0`
        -   Card/Surface Body: `text-[2.4rem] leading-[1.4] mb-0`
6.  **Interactivity**:
    -   **Navigation**: Keyboard ONLY (Left/Right Arrows, Space, Enter).
    -   **Mouse**: Click navigation DISABLED.
    -   **State Management**: URL Hash based (`#1`, `#2`...).
    -   **Progress Bar**: Bottom of screen.
    -   **Page Number**: Bottom-right corner.
7.  **Content Strategy (Agent-Driven)**:
    -   **Understand**: Read the full text to grasp the core message before generating.
    -   **Summarize**: Do not copy-paste long blocks of text. Refine paragraphs into concise bullet points or short, punchy statements suitable for slides.
    -   **Restructure**: Use H2 headers as a guide, but intelligently split complex topics across multiple slides or combine related small points. Ensure a smooth narrative flow.
    -   **Math Formulas**: Use LaTeX syntax wrapped in `$$` for block math or `$` for inline math.
        -   Example: `$$ E = mc^2 $$`
    -   **Visual Hierarchy**: Use bolding, blockquotes, and layout adjustments to emphasize the most important information.
8.  **Git Operations**:
    -   **No Proactive Commits**: Do not proactively commit code unless explicitly requested by the user.

## Output File Naming
-   Save the generated HTML file in the `slides/` directory.
-   Filename should match the source markdown filename but with `.html` extension.

## Code Template

Use the following HTML structure as the base. Replace `<!-- SLIDES_CONTENT_HERE -->` with the generated HTML slides.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Course Slides</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#3ECF8E', // Supabase Green
                        bg: '#121212',      // Supabase Dark BG
                        surface: '#1C1C1C', // Darker Surface
                        text: '#EDEDED',    // Off-white text
                        muted: '#A1A1A1',   // Muted text
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <!-- MathJax Configuration -->
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            },
            svg: {
                fontCache: 'global'
            }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        /* Custom scrollbar hide */
        ::-webkit-scrollbar { display: none; }
        
        body {
            background-color: #121212;
            color: #EDEDED;
            overflow: hidden;
            font-size: 2.4em;
        }

        /* Slide Transition Logic */
        .slide-content {
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
            pointer-events: none;
        }
        
        .slide-content.active {
            opacity: 1;
            pointer-events: auto;
            z-index: 10;
        }

        /* Strong Highlight */
        strong {
            color: #3ECF8E;
            font-weight: 700;
        }
    </style>
</head>
<body class="bg-bg text-white h-screen w-screen overflow-hidden relative selection:bg-primary selection:text-black">

    <!-- Slides Container -->
    <main id="slides-container" class="w-full h-full relative">
        <!-- SLIDES_CONTENT_HERE -->
    </main>

    <!-- Progress Bar -->
    <div class="fixed bottom-0 left-0 w-full h-2 bg-gray-800 z-50">
        <div id="progress-bar" class="h-full bg-primary transition-all duration-300" style="width: 0%"></div>
    </div>

    <!-- Page Number -->
    <div id="page-number" class="fixed bottom-4 right-4 text-primary text-xl font-mono z-50 opacity-80">
        1 / 1
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const slides = document.querySelectorAll('.slide-content');
            const progressBar = document.getElementById('progress-bar');
            const pageNumber = document.getElementById('page-number');
            let currentIndex = 0;

            function updateSlide(index) {
                if (index < 0) index = 0;
                if (index >= slides.length) index = slides.length - 1;

                currentIndex = index;

                // Update visibility
                slides.forEach((slide, i) => {
                    if (i === currentIndex) {
                        slide.classList.add('active');
                    } else {
                        slide.classList.remove('active');
                    }
                });

                // Update progress bar
                const progress = ((currentIndex + 1) / slides.length) * 100;
                progressBar.style.width = `${progress}%`;

                // Update page number
                pageNumber.textContent = `${currentIndex + 1} / ${slides.length}`;
                
                // Update URL hash
                window.location.hash = `#${currentIndex + 1}`;
            }

            // Keyboard Navigation
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
                    updateSlide(currentIndex + 1);
                } else if (e.key === 'ArrowLeft') {
                    updateSlide(currentIndex - 1);
                }
            });

            // Initialize from URL hash
            const hash = window.location.hash;
            let initialIndex = 0;
            if (hash) {
                const page = parseInt(hash.substring(1), 10);
                if (!isNaN(page)) {
                    initialIndex = page - 1;
                }
            }
            updateSlide(initialIndex);
            
            // Handle hash change (e.g. browser back button)
            window.addEventListener('hashchange', () => {
                const hash = window.location.hash;
                if (hash) {
                    const page = parseInt(hash.substring(1), 10);
                    if (!isNaN(page)) {
                        updateSlide(page - 1);
                    }
                }
            });
        });
    </script>
</body>
</html>
```

## Generation Workflow (Agent Mental Model)
1.  **Analysis**: 
    -   Read the source Markdown completely.
    -   Identify the "Series" (e.g., AI 101) and "Module" (e.g., Machine Learning).
    -   Determine the best icon/visual theme based on the content.
2.  **Content Refinement**:
    -   **Title Slide**: Extract the main title and a compelling subtitle (summarizing the essence).
    -   **Section Slides**: For each section, ask: "What is the one key takeaway here?"
    -   **Simplification**: Turn "The model learns by minimizing the loss function..." into "Goal: Minimize Loss Function".
    -   **Formatting**: Use HTML tags manually (`<strong>`, `<ul>`, `<blockquote>`) to structure the refined content.
3.  **Slide Construction**:
    -   Create a new `<div class="slide-content ...">` for each logical unit of thought.
    -   **Constraint**: Ensure no slide is overcrowded. If a section is deep, break it into:
        -   Slide A: Concept Definition
        -   Slide B: Examples/Details
        -   Slide C: Key Takeaway
4.  **Direct Generation**: 
    -   Output the full HTML file directly. Do not rely on intermediate Python scripts for conversion.

## Example Title Slide Structure
```html
<div class="slide-content active absolute top-0 left-0 w-full h-full flex flex-col justify-center items-center text-center p-[3rem_8rem] bg-[radial-gradient(circle_at_center,#1a1a1a_0%,#121212_70%)]" data-index="0">
    <!-- Series Tag -->
    <div class="mb-10 flex items-center gap-6 text-5xl font-mono tracking-widest uppercase text-muted">
        <span class="text-primary font-bold">人工智能通识</span>
        <span class="w-2 h-2 rounded-full bg-gray-600"></span>
        <span class="text-gray-300">MODULE_NAME</span>
    </div>

    <!-- Icon -->
    <div class="mb-12 relative">
        <div class="absolute -inset-10 bg-primary/10 rounded-full blur-3xl"></div>
        <!-- ICON_SVG_HERE -->
        <svg class="w-48 h-48 text-primary relative z-10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <!-- Icon Path -->
        </svg>
    </div>

    <h1 class="text-[7rem] font-extrabold text-text mb-8 text-center [text-shadow:0_0_40px_rgba(62,207,142,0.1)] leading-[1.1]">TITLE</h1>
    <p class="text-[3rem] text-muted text-center max-w-[80%] font-light leading-[1.5]">SUBTITLE</p>
</div>
```
