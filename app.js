function showTab(tab) {
    document.querySelectorAll(".tab-content").forEach(el => el.classList.add("hidden"));
    document.getElementById(tab).classList.remove("hidden");
}

function changeTheme() {
    const theme = document.getElementById("theme").value;
    document.body.className = theme;

    const prismTheme = document.getElementById("prism-theme");

    if (theme === "light") {
        prismTheme.href = "https://cdn.jsdelivr.net/npm/prismjs/themes/prism.css";
    } else {
        prismTheme.href = "https://cdn.jsdelivr.net/npm/prismjs/themes/prism-tomorrow.css";
    }
}

async function generate() {

    const problem = document.getElementById("problem").value;
    const language = document.getElementById("language").value;

    document.getElementById("terminalOutput").innerText = "$ Running AI agents...\n";

    const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            problem: problem,
            language: language
        })
    });

    const data = await response.json();

    // Code
    const codeBlock = document.getElementById("codeOutput");
    codeBlock.className = "language-" + language;
    codeBlock.textContent = data.code || "";
    Prism.highlightElement(codeBlock);

    // Plan
    document.getElementById("plan").innerText = data.plan || "";

    // Review
    document.getElementById("review").innerText = data.review || "";

    // Tests
    document.getElementById("tests").innerText = data.tests || "";

    // Explanation (simple: reuse review for now)
    document.getElementById("explanation").innerText = data.review || "";

    // Terminal
    document.getElementById("terminalOutput").innerText =
        "$ Execution Result:\n\n" + (data.sandbox || "No output");
}
