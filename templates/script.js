// API Base URL
const API_BASE_URL = "http://localhost:5000/api";

// DOM Elements
const stringCountInput = document.getElementById("stringCount");
const patternSelect = document.getElementById("pattern");
const conversionOptions = document.getElementById("conversionOptions");
const conversionDirection = document.getElementById("conversionDirection");
const algorithmSelect = document.getElementById("algorithm");
const generateButton = document.getElementById("generateButton");
const runButton = document.getElementById("runButton");
const stringPreview = document.getElementById("stringPreview");
const stringLength = document.getElementById("stringLength");
const stringPattern = document.getElementById("stringPattern");
const loading = document.getElementById("loading");
const results = document.getElementById("results");
const errorMessage = document.getElementById("errorMessage");
const algorithmBadge = document.getElementById("algorithmBadge");
const algorithmDescription = document.getElementById("algorithmDescription");
const timeResult = document.getElementById("timeResult");
const memoryResult = document.getElementById("memoryResult");
const resultStringPreview = document.getElementById("resultStringPreview");
const resultLength = document.getElementById("resultLength");
const timestamp = document.getElementById("timestamp");

// Current string data
let currentString = "";
let currentPattern = "mixed";
let currentLength = 0;

// Show/hide error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = "block";
}

function hideError() {
    errorMessage.style.display = "none";
}

// Show/hide loading
function showLoading() {
    loading.style.display = "block";
    runButton.disabled = true;
    hideError();
}

function hideLoading() {
    loading.style.display = "none";
    runButton.disabled = false;  // Keep enabled after first run to allow re-analysis
}

// Toggle conversion options based on pattern
function updateConversionOptions() {
    if (patternSelect.value === "mixed") {
        conversionOptions.style.display = "block";
    } else {
        conversionOptions.style.display = "none";
    }
}

// Generate string via API
async function generateString() {
    const n = parseInt(stringCountInput.value);
    const pattern = patternSelect.value;

    if (!n || n < 1) {
        showError("Masukkan jumlah karakter yang valid (minimal 1)");
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                n: n,
                pattern: pattern,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to generate string");
        }

        // Update UI
        currentString = data.string;
        currentLength = data.length;
        currentPattern = data.pattern;  // Store pattern for analysis

        stringPreview.textContent = currentString;
        stringLength.textContent = currentLength;
        stringPattern.textContent = currentPattern.charAt(0).toUpperCase() + currentPattern.slice(1);

        // Enable run button
        runButton.disabled = false;

        // Hide results if shown
        results.style.display = "none";

        hideLoading();
        hideError();

    } catch (error) {
        showError(error.message);
        hideLoading();
    }
}

// Run analysis via API
async function runAnalysis() {
    if (!currentString) {
        showError("Generate string terlebih dahulu");
        return;
    }

    const algorithm = algorithmSelect.value;
    const direction = conversionDirection.value;  // For mixed pattern

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text: currentString,
                algorithm: algorithm,
                pattern: currentPattern,  // Send stored pattern
                direction: direction,     // Send direction for mixed
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to analyze");
        }

        // Update results UI
        algorithmBadge.textContent = algorithm === "iterative" ? "Iteratif" : "Rekursif";
        algorithmBadge.className = `algorithm-badge ${algorithm}`;
        algorithmDescription.textContent = algorithm === "iterative" 
            ? "Menggunakan loop untuk konversi karakter per karakter" 
            : "Menggunakan fungsi rekursif untuk konversi";
        timeResult.textContent = data.execution_time_ms;
        memoryResult.textContent = data.memory_usage_kb;
        resultStringPreview.textContent = data.output;
        resultLength.textContent = data.output_length;
        timestamp.textContent = new Date(data.timestamp).toLocaleString();

        // Show results
        results.style.display = "block";

        hideLoading();
        hideError();

    } catch (error) {
        showError(error.message);
        hideLoading();
    }
}

// Event listeners
document.addEventListener("DOMContentLoaded", function() {
    // Initial setup
    updateConversionOptions();
    
    // Pattern change
    patternSelect.addEventListener("change", updateConversionOptions);
    
    // Generate button
    generateButton.addEventListener("click", generateString);
    
    // Run button
    runButton.addEventListener("click", runAnalysis);
});